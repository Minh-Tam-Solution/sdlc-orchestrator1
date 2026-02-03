/**
 * SSOT Validator for VS Code Extension
 *
 * Sprint 141: Full Workflow Integration
 * RFC-SDLC-602: E2E API Testing Enhancement
 *
 * Validates Single Source of Truth (SSOT) compliance for OpenAPI files.
 * Detects duplicate openapi.json files and provides auto-fix with symlinks.
 *
 * @version 1.0.0
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { Logger } from '../utils/logger';

/**
 * SSOT Violation detected in the project
 */
export interface SSOTViolation {
    /** Type of violation */
    type: 'DUPLICATE_OPENAPI' | 'MISSING_SSOT' | 'INVALID_SYMLINK' | 'OUTDATED_COPY';
    /** Path to the violating file */
    filePath: string;
    /** Expected canonical path */
    canonicalPath: string;
    /** Human-readable description */
    description: string;
    /** Severity level */
    severity: 'error' | 'warning';
    /** Whether this can be auto-fixed */
    autoFixable: boolean;
}

/**
 * Result of SSOT validation
 */
export interface SSOTValidationResult {
    /** Whether SSOT is compliant */
    isCompliant: boolean;
    /** List of violations found */
    violations: SSOTViolation[];
    /** Path to the canonical openapi.json (SSOT) */
    canonicalPath: string | null;
    /** Count of openapi.json files found */
    openapiFileCount: number;
    /** Timestamp of validation */
    validatedAt: string;
}

/**
 * Result of SSOT fix operation
 */
export interface SSOTFixResult {
    /** Whether the fix was successful */
    success: boolean;
    /** Number of files fixed */
    fixedCount: number;
    /** Files that were fixed */
    fixedFiles: string[];
    /** Backup files created */
    backupFiles: string[];
    /** Errors encountered */
    errors: string[];
}

/**
 * SSOT Validator Service
 *
 * Validates that openapi.json follows Single Source of Truth principle.
 * The canonical location is: docs/03-Integration-APIs/02-API-Specifications/openapi.json
 */
export class SSOTValidator {
    /** Canonical path pattern for OpenAPI spec */
    private readonly canonicalPathPattern = 'docs/03-Integration-APIs/02-API-Specifications/openapi.json';

    /** Alternative canonical paths (legacy support) */
    private readonly alternativeCanonicalPaths = [
        'docs/03-integrate/01-api-contracts/openapi.json',
        'docs/03-integrate/02-API-Specifications/openapi.json',
    ];

    /** Diagnostic collection for VS Code problems panel */
    private diagnosticCollection: vscode.DiagnosticCollection;

    /** File watcher for openapi.json changes */
    private fileWatcher: vscode.FileSystemWatcher | undefined;

    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('sdlc-ssot');
    }

    /**
     * Validate SSOT compliance in the workspace
     *
     * @param workspaceRoot - Root path of the workspace
     * @returns Validation result with violations
     */
    async validate(workspaceRoot: string): Promise<SSOTValidationResult> {
        Logger.info(`Validating SSOT compliance in ${workspaceRoot}`);

        const violations: SSOTViolation[] = [];
        let canonicalPath: string | null = null;

        // Find all openapi.json files
        const openapiFiles = await this.findOpenapiFiles(workspaceRoot);
        Logger.info(`Found ${openapiFiles.length} openapi.json files`);

        // Determine canonical path
        canonicalPath = this.findCanonicalPath(workspaceRoot);

        if (!canonicalPath) {
            // Check if any openapi.json exists
            if (openapiFiles.length > 0) {
                // Canonical location missing but files exist elsewhere
                violations.push({
                    type: 'MISSING_SSOT',
                    filePath: path.join(workspaceRoot, this.canonicalPathPattern),
                    canonicalPath: path.join(workspaceRoot, this.canonicalPathPattern),
                    description: `OpenAPI spec not found at canonical location: ${this.canonicalPathPattern}`,
                    severity: 'error',
                    autoFixable: openapiFiles.length === 1, // Can auto-fix if only one file exists
                });
            }
        }

        // Check for duplicates (files that are not symlinks to canonical)
        for (const filePath of openapiFiles) {
            if (canonicalPath && path.resolve(filePath) === path.resolve(canonicalPath)) {
                continue; // Skip the canonical file itself
            }

            const stats = await this.getFileStats(filePath);

            if (stats?.isSymbolicLink) {
                // Check if symlink points to canonical
                try {
                    const target = fs.readlinkSync(filePath);
                    const resolvedTarget = path.resolve(path.dirname(filePath), target);

                    if (canonicalPath && path.resolve(resolvedTarget) !== path.resolve(canonicalPath)) {
                        violations.push({
                            type: 'INVALID_SYMLINK',
                            filePath,
                            canonicalPath: canonicalPath || '',
                            description: `Symlink points to ${resolvedTarget} instead of canonical location`,
                            severity: 'warning',
                            autoFixable: true,
                        });
                    }
                } catch (error) {
                    violations.push({
                        type: 'INVALID_SYMLINK',
                        filePath,
                        canonicalPath: canonicalPath || '',
                        description: `Broken symlink at ${filePath}`,
                        severity: 'error',
                        autoFixable: true,
                    });
                }
            } else {
                // Regular file - duplicate violation
                violations.push({
                    type: 'DUPLICATE_OPENAPI',
                    filePath,
                    canonicalPath: canonicalPath || path.join(workspaceRoot, this.canonicalPathPattern),
                    description: `Duplicate openapi.json found. SSOT location: ${this.canonicalPathPattern}`,
                    severity: 'error',
                    autoFixable: true,
                });
            }
        }

        // Update diagnostics for VS Code problems panel
        this.updateDiagnostics(violations);

        const result: SSOTValidationResult = {
            isCompliant: violations.length === 0,
            violations,
            canonicalPath,
            openapiFileCount: openapiFiles.length,
            validatedAt: new Date().toISOString(),
        };

        Logger.info(`SSOT validation complete: ${result.isCompliant ? 'COMPLIANT' : `${violations.length} violations`}`);

        return result;
    }

    /**
     * Auto-fix SSOT violations by creating symlinks
     *
     * @param workspaceRoot - Root path of the workspace
     * @param violations - Violations to fix
     * @returns Fix result with details
     */
    async fix(workspaceRoot: string, violations: SSOTViolation[]): Promise<SSOTFixResult> {
        Logger.info(`Attempting to fix ${violations.length} SSOT violations`);

        const fixedFiles: string[] = [];
        const backupFiles: string[] = [];
        const errors: string[] = [];

        // Find canonical path
        let canonicalPath = this.findCanonicalPath(workspaceRoot);

        // Handle MISSING_SSOT - move first duplicate to canonical location
        const missingViolation = violations.find(v => v.type === 'MISSING_SSOT');
        if (missingViolation && !canonicalPath) {
            const duplicates = violations.filter(v => v.type === 'DUPLICATE_OPENAPI');
            if (duplicates.length > 0 && duplicates[0]) {
                const firstDuplicate = duplicates[0].filePath;
                const targetPath = path.join(workspaceRoot, this.canonicalPathPattern);

                try {
                    // Ensure directory exists
                    const targetDir = path.dirname(targetPath);
                    if (!fs.existsSync(targetDir)) {
                        fs.mkdirSync(targetDir, { recursive: true });
                    }

                    // Move file to canonical location
                    fs.copyFileSync(firstDuplicate, targetPath);
                    canonicalPath = targetPath;
                    fixedFiles.push(`Moved ${firstDuplicate} → ${targetPath}`);

                    // Remove the duplicate since it's now moved
                    const backupPath = `${firstDuplicate}.backup`;
                    fs.renameSync(firstDuplicate, backupPath);
                    backupFiles.push(backupPath);
                } catch (error) {
                    const errorMessage = error instanceof Error ? error.message : String(error);
                    errors.push(`Failed to create canonical file: ${errorMessage}`);
                }
            }
        }

        if (!canonicalPath) {
            errors.push('Canonical openapi.json not found. Cannot create symlinks.');
            return {
                success: false,
                fixedCount: 0,
                fixedFiles,
                backupFiles,
                errors,
            };
        }

        // Fix duplicates by replacing with symlinks
        const fixableViolations = violations.filter(
            v => v.autoFixable && (v.type === 'DUPLICATE_OPENAPI' || v.type === 'INVALID_SYMLINK')
        );

        for (const violation of fixableViolations) {
            try {
                const filePath = violation.filePath;

                // Skip if file no longer exists (might have been handled above)
                if (!fs.existsSync(filePath)) {
                    continue;
                }

                // Create backup
                const backupPath = `${filePath}.backup`;
                if (!fs.existsSync(backupPath)) {
                    fs.copyFileSync(filePath, backupPath);
                    backupFiles.push(backupPath);
                }

                // Remove duplicate file
                fs.unlinkSync(filePath);

                // Create relative symlink
                const relativePath = path.relative(path.dirname(filePath), canonicalPath);
                fs.symlinkSync(relativePath, filePath);

                fixedFiles.push(`${filePath} → ${relativePath}`);
                Logger.info(`Fixed SSOT violation: ${filePath} → ${relativePath}`);
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : String(error);
                errors.push(`Failed to fix ${violation.filePath}: ${errorMessage}`);
                Logger.error(`Failed to fix SSOT violation: ${errorMessage}`);
            }
        }

        // Clear diagnostics for fixed violations
        this.diagnosticCollection.clear();

        // Re-validate to update remaining diagnostics
        const newResult = await this.validate(workspaceRoot);
        this.updateDiagnostics(newResult.violations);

        return {
            success: errors.length === 0,
            fixedCount: fixedFiles.length,
            fixedFiles,
            backupFiles,
            errors,
        };
    }

    /**
     * Start watching for openapi.json changes
     *
     * @param workspaceRoot - Root path of the workspace
     */
    startWatching(workspaceRoot: string): void {
        if (this.fileWatcher) {
            this.fileWatcher.dispose();
        }

        const pattern = new vscode.RelativePattern(workspaceRoot, '**/openapi.json');
        this.fileWatcher = vscode.workspace.createFileSystemWatcher(pattern);

        this.fileWatcher.onDidCreate(() => this.onOpenapiChange(workspaceRoot));
        this.fileWatcher.onDidChange(() => this.onOpenapiChange(workspaceRoot));
        this.fileWatcher.onDidDelete(() => this.onOpenapiChange(workspaceRoot));

        Logger.info('SSOT file watcher started');
    }

    /**
     * Stop watching for changes
     */
    stopWatching(): void {
        if (this.fileWatcher) {
            this.fileWatcher.dispose();
            this.fileWatcher = undefined;
        }
    }

    /**
     * Dispose resources
     */
    dispose(): void {
        this.stopWatching();
        this.diagnosticCollection.dispose();
    }

    /**
     * Find all openapi.json files in workspace
     */
    private async findOpenapiFiles(workspaceRoot: string): Promise<string[]> {
        const files: string[] = [];

        const searchDir = async (dir: string): Promise<void> => {
            const entries = fs.readdirSync(dir, { withFileTypes: true });

            for (const entry of entries) {
                const fullPath = path.join(dir, entry.name);

                // Skip node_modules, .git, etc.
                if (entry.isDirectory()) {
                    if (['node_modules', '.git', '__pycache__', '.venv', 'dist', 'build'].includes(entry.name)) {
                        continue;
                    }
                    await searchDir(fullPath);
                } else if (entry.name === 'openapi.json') {
                    files.push(fullPath);
                }
            }
        };

        try {
            await searchDir(workspaceRoot);
        } catch (error) {
            Logger.error(`Error searching for openapi.json files: ${error}`);
        }

        return files;
    }

    /**
     * Find canonical openapi.json path
     */
    private findCanonicalPath(workspaceRoot: string): string | null {
        // Check primary canonical path
        const primaryPath = path.join(workspaceRoot, this.canonicalPathPattern);
        if (fs.existsSync(primaryPath)) {
            return primaryPath;
        }

        // Check alternative paths
        for (const altPath of this.alternativeCanonicalPaths) {
            const fullPath = path.join(workspaceRoot, altPath);
            if (fs.existsSync(fullPath)) {
                return fullPath;
            }
        }

        return null;
    }

    /**
     * Get file stats with symlink detection
     */
    private async getFileStats(filePath: string): Promise<{ isSymbolicLink: boolean } | null> {
        try {
            const stats = fs.lstatSync(filePath);
            return {
                isSymbolicLink: stats.isSymbolicLink(),
            };
        } catch {
            return null;
        }
    }

    /**
     * Handle openapi.json file changes
     */
    private async onOpenapiChange(workspaceRoot: string): Promise<void> {
        Logger.info('OpenAPI file change detected, re-validating SSOT');
        await this.validate(workspaceRoot);
    }

    /**
     * Update VS Code diagnostics panel with violations
     */
    private updateDiagnostics(violations: SSOTViolation[]): void {
        this.diagnosticCollection.clear();

        const diagnosticMap = new Map<string, vscode.Diagnostic[]>();

        for (const violation of violations) {
            const uri = vscode.Uri.file(violation.filePath);
            const diagnostics = diagnosticMap.get(uri.toString()) || [];

            const diagnostic = new vscode.Diagnostic(
                new vscode.Range(0, 0, 0, 0),
                violation.description,
                violation.severity === 'error'
                    ? vscode.DiagnosticSeverity.Error
                    : vscode.DiagnosticSeverity.Warning
            );

            diagnostic.source = 'SDLC SSOT';
            diagnostic.code = violation.type;

            diagnostics.push(diagnostic);
            diagnosticMap.set(uri.toString(), diagnostics);
        }

        for (const [uriString, diagnostics] of diagnosticMap) {
            this.diagnosticCollection.set(vscode.Uri.parse(uriString), diagnostics);
        }
    }
}

/**
 * Register SSOT validation commands
 *
 * @param context - VS Code extension context
 * @returns SSOTValidator instance
 */
export function registerSSOTCommands(context: vscode.ExtensionContext): SSOTValidator {
    const validator = new SSOTValidator();

    // Start watching in the first workspace folder
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (workspaceRoot) {
        validator.startWatching(workspaceRoot);
    }

    // Register Check SSOT Compliance command
    context.subscriptions.push(
        vscode.commands.registerCommand('sdlc.checkSSOT', async () => {
            const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
            if (!workspaceRoot) {
                void vscode.window.showErrorMessage('No workspace folder open');
                return;
            }

            await vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Checking SSOT Compliance...',
                    cancellable: false,
                },
                async () => {
                    const result = await validator.validate(workspaceRoot);

                    if (result.isCompliant) {
                        void vscode.window.showInformationMessage(
                            `✓ SSOT Compliant: openapi.json found at canonical location`
                        );
                    } else {
                        const message = `SSOT Violations: ${result.violations.length} found`;
                        const action = await vscode.window.showWarningMessage(
                            message,
                            'Fix All',
                            'View Details'
                        );

                        if (action === 'Fix All') {
                            await vscode.commands.executeCommand('sdlc.fixSSOT');
                        } else if (action === 'View Details') {
                            // Show violations in output channel
                            const channel = vscode.window.createOutputChannel('SDLC SSOT Validation');
                            channel.clear();
                            channel.appendLine('='.repeat(60));
                            channel.appendLine('SSOT Validation Report');
                            channel.appendLine('='.repeat(60));
                            channel.appendLine('');
                            channel.appendLine(`Status: ${result.isCompliant ? 'COMPLIANT' : 'VIOLATIONS FOUND'}`);
                            channel.appendLine(`OpenAPI files found: ${result.openapiFileCount}`);
                            channel.appendLine(`Canonical path: ${result.canonicalPath || 'NOT FOUND'}`);
                            channel.appendLine('');

                            if (result.violations.length > 0) {
                                channel.appendLine('-'.repeat(60));
                                channel.appendLine('Violations:');
                                channel.appendLine('-'.repeat(60));
                                for (const v of result.violations) {
                                    channel.appendLine('');
                                    channel.appendLine(`Type: ${v.type}`);
                                    channel.appendLine(`Severity: ${v.severity.toUpperCase()}`);
                                    channel.appendLine(`File: ${v.filePath}`);
                                    channel.appendLine(`Description: ${v.description}`);
                                    channel.appendLine(`Auto-fixable: ${v.autoFixable ? 'Yes' : 'No'}`);
                                }
                            }

                            channel.show();
                        }
                    }
                }
            );
        })
    );

    // Register Fix SSOT Violations command
    context.subscriptions.push(
        vscode.commands.registerCommand('sdlc.fixSSOT', async () => {
            const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
            if (!workspaceRoot) {
                void vscode.window.showErrorMessage('No workspace folder open');
                return;
            }

            // First validate to get violations
            const validation = await validator.validate(workspaceRoot);

            if (validation.isCompliant) {
                void vscode.window.showInformationMessage('No SSOT violations to fix');
                return;
            }

            // Confirm fix
            const autoFixable = validation.violations.filter(v => v.autoFixable);
            if (autoFixable.length === 0) {
                void vscode.window.showWarningMessage('No auto-fixable violations found');
                return;
            }

            const confirm = await vscode.window.showWarningMessage(
                `Found ${autoFixable.length} auto-fixable violations. This will create symlinks to the canonical openapi.json. Backups will be created.`,
                'Fix Now',
                'Cancel'
            );

            if (confirm !== 'Fix Now') {
                return;
            }

            await vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Fixing SSOT Violations...',
                    cancellable: false,
                },
                async () => {
                    const result = await validator.fix(workspaceRoot, validation.violations);

                    if (result.success) {
                        void vscode.window.showInformationMessage(
                            `✓ Fixed ${result.fixedCount} SSOT violations. Backups created.`
                        );
                    } else {
                        void vscode.window.showErrorMessage(
                            `Fixed ${result.fixedCount} violations with ${result.errors.length} errors`
                        );

                        // Show errors in output
                        if (result.errors.length > 0) {
                            const channel = vscode.window.createOutputChannel('SDLC SSOT Fix');
                            channel.clear();
                            channel.appendLine('SSOT Fix Errors:');
                            for (const error of result.errors) {
                                channel.appendLine(`  - ${error}`);
                            }
                            channel.show();
                        }
                    }
                }
            );
        })
    );

    // Cleanup on deactivation
    context.subscriptions.push({
        dispose: () => validator.dispose(),
    });

    Logger.info('SSOT validation commands registered');

    return validator;
}
