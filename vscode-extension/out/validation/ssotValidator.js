"use strict";
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
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.SSOTValidator = void 0;
exports.registerSSOTCommands = registerSSOTCommands;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const logger_1 = require("../utils/logger");
/**
 * SSOT Validator Service
 *
 * Validates that openapi.json follows Single Source of Truth principle.
 * The canonical location is: docs/03-Integration-APIs/02-API-Specifications/openapi.json
 */
class SSOTValidator {
    /** Canonical path pattern for OpenAPI spec */
    canonicalPathPattern = 'docs/03-Integration-APIs/02-API-Specifications/openapi.json';
    /** Alternative canonical paths (legacy support) */
    alternativeCanonicalPaths = [
        'docs/03-integrate/01-api-contracts/openapi.json',
        'docs/03-integrate/02-API-Specifications/openapi.json',
    ];
    /** Diagnostic collection for VS Code problems panel */
    diagnosticCollection;
    /** File watcher for openapi.json changes */
    fileWatcher;
    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('sdlc-ssot');
    }
    /**
     * Validate SSOT compliance in the workspace
     *
     * @param workspaceRoot - Root path of the workspace
     * @returns Validation result with violations
     */
    async validate(workspaceRoot) {
        logger_1.Logger.info(`Validating SSOT compliance in ${workspaceRoot}`);
        const violations = [];
        let canonicalPath = null;
        // Find all openapi.json files
        const openapiFiles = await this.findOpenapiFiles(workspaceRoot);
        logger_1.Logger.info(`Found ${openapiFiles.length} openapi.json files`);
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
                }
                catch (error) {
                    violations.push({
                        type: 'INVALID_SYMLINK',
                        filePath,
                        canonicalPath: canonicalPath || '',
                        description: `Broken symlink at ${filePath}`,
                        severity: 'error',
                        autoFixable: true,
                    });
                }
            }
            else {
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
        const result = {
            isCompliant: violations.length === 0,
            violations,
            canonicalPath,
            openapiFileCount: openapiFiles.length,
            validatedAt: new Date().toISOString(),
        };
        logger_1.Logger.info(`SSOT validation complete: ${result.isCompliant ? 'COMPLIANT' : `${violations.length} violations`}`);
        return result;
    }
    /**
     * Auto-fix SSOT violations by creating symlinks
     *
     * @param workspaceRoot - Root path of the workspace
     * @param violations - Violations to fix
     * @returns Fix result with details
     */
    async fix(workspaceRoot, violations) {
        logger_1.Logger.info(`Attempting to fix ${violations.length} SSOT violations`);
        const fixedFiles = [];
        const backupFiles = [];
        const errors = [];
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
                }
                catch (error) {
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
        const fixableViolations = violations.filter(v => v.autoFixable && (v.type === 'DUPLICATE_OPENAPI' || v.type === 'INVALID_SYMLINK'));
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
                logger_1.Logger.info(`Fixed SSOT violation: ${filePath} → ${relativePath}`);
            }
            catch (error) {
                const errorMessage = error instanceof Error ? error.message : String(error);
                errors.push(`Failed to fix ${violation.filePath}: ${errorMessage}`);
                logger_1.Logger.error(`Failed to fix SSOT violation: ${errorMessage}`);
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
    startWatching(workspaceRoot) {
        if (this.fileWatcher) {
            this.fileWatcher.dispose();
        }
        const pattern = new vscode.RelativePattern(workspaceRoot, '**/openapi.json');
        this.fileWatcher = vscode.workspace.createFileSystemWatcher(pattern);
        this.fileWatcher.onDidCreate(() => this.onOpenapiChange(workspaceRoot));
        this.fileWatcher.onDidChange(() => this.onOpenapiChange(workspaceRoot));
        this.fileWatcher.onDidDelete(() => this.onOpenapiChange(workspaceRoot));
        logger_1.Logger.info('SSOT file watcher started');
    }
    /**
     * Stop watching for changes
     */
    stopWatching() {
        if (this.fileWatcher) {
            this.fileWatcher.dispose();
            this.fileWatcher = undefined;
        }
    }
    /**
     * Dispose resources
     */
    dispose() {
        this.stopWatching();
        this.diagnosticCollection.dispose();
    }
    /**
     * Find all openapi.json files in workspace
     */
    async findOpenapiFiles(workspaceRoot) {
        const files = [];
        const searchDir = async (dir) => {
            const entries = fs.readdirSync(dir, { withFileTypes: true });
            for (const entry of entries) {
                const fullPath = path.join(dir, entry.name);
                // Skip node_modules, .git, etc.
                if (entry.isDirectory()) {
                    if (['node_modules', '.git', '__pycache__', '.venv', 'dist', 'build'].includes(entry.name)) {
                        continue;
                    }
                    await searchDir(fullPath);
                }
                else if (entry.name === 'openapi.json') {
                    files.push(fullPath);
                }
            }
        };
        try {
            await searchDir(workspaceRoot);
        }
        catch (error) {
            logger_1.Logger.error(`Error searching for openapi.json files: ${error}`);
        }
        return files;
    }
    /**
     * Find canonical openapi.json path
     */
    findCanonicalPath(workspaceRoot) {
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
    async getFileStats(filePath) {
        try {
            const stats = fs.lstatSync(filePath);
            return {
                isSymbolicLink: stats.isSymbolicLink(),
            };
        }
        catch {
            return null;
        }
    }
    /**
     * Handle openapi.json file changes
     */
    async onOpenapiChange(workspaceRoot) {
        logger_1.Logger.info('OpenAPI file change detected, re-validating SSOT');
        await this.validate(workspaceRoot);
    }
    /**
     * Update VS Code diagnostics panel with violations
     */
    updateDiagnostics(violations) {
        this.diagnosticCollection.clear();
        const diagnosticMap = new Map();
        for (const violation of violations) {
            const uri = vscode.Uri.file(violation.filePath);
            const diagnostics = diagnosticMap.get(uri.toString()) || [];
            const diagnostic = new vscode.Diagnostic(new vscode.Range(0, 0, 0, 0), violation.description, violation.severity === 'error'
                ? vscode.DiagnosticSeverity.Error
                : vscode.DiagnosticSeverity.Warning);
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
exports.SSOTValidator = SSOTValidator;
/**
 * Register SSOT validation commands
 *
 * @param context - VS Code extension context
 * @returns SSOTValidator instance
 */
function registerSSOTCommands(context) {
    const validator = new SSOTValidator();
    // Start watching in the first workspace folder
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (workspaceRoot) {
        validator.startWatching(workspaceRoot);
    }
    // Register Check SSOT Compliance command
    context.subscriptions.push(vscode.commands.registerCommand('sdlc.checkSSOT', async () => {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) {
            void vscode.window.showErrorMessage('No workspace folder open');
            return;
        }
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Checking SSOT Compliance...',
            cancellable: false,
        }, async () => {
            const result = await validator.validate(workspaceRoot);
            if (result.isCompliant) {
                void vscode.window.showInformationMessage(`✓ SSOT Compliant: openapi.json found at canonical location`);
            }
            else {
                const message = `SSOT Violations: ${result.violations.length} found`;
                const action = await vscode.window.showWarningMessage(message, 'Fix All', 'View Details');
                if (action === 'Fix All') {
                    await vscode.commands.executeCommand('sdlc.fixSSOT');
                }
                else if (action === 'View Details') {
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
        });
    }));
    // Register Fix SSOT Violations command
    context.subscriptions.push(vscode.commands.registerCommand('sdlc.fixSSOT', async () => {
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
        const confirm = await vscode.window.showWarningMessage(`Found ${autoFixable.length} auto-fixable violations. This will create symlinks to the canonical openapi.json. Backups will be created.`, 'Fix Now', 'Cancel');
        if (confirm !== 'Fix Now') {
            return;
        }
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Fixing SSOT Violations...',
            cancellable: false,
        }, async () => {
            const result = await validator.fix(workspaceRoot, validation.violations);
            if (result.success) {
                void vscode.window.showInformationMessage(`✓ Fixed ${result.fixedCount} SSOT violations. Backups created.`);
            }
            else {
                void vscode.window.showErrorMessage(`Fixed ${result.fixedCount} violations with ${result.errors.length} errors`);
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
        });
    }));
    // Cleanup on deactivation
    context.subscriptions.push({
        dispose: () => validator.dispose(),
    });
    logger_1.Logger.info('SSOT validation commands registered');
    return validator;
}
//# sourceMappingURL=ssotValidator.js.map