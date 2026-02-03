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
export declare class SSOTValidator {
    /** Canonical path pattern for OpenAPI spec */
    private readonly canonicalPathPattern;
    /** Alternative canonical paths (legacy support) */
    private readonly alternativeCanonicalPaths;
    /** Diagnostic collection for VS Code problems panel */
    private diagnosticCollection;
    /** File watcher for openapi.json changes */
    private fileWatcher;
    constructor();
    /**
     * Validate SSOT compliance in the workspace
     *
     * @param workspaceRoot - Root path of the workspace
     * @returns Validation result with violations
     */
    validate(workspaceRoot: string): Promise<SSOTValidationResult>;
    /**
     * Auto-fix SSOT violations by creating symlinks
     *
     * @param workspaceRoot - Root path of the workspace
     * @param violations - Violations to fix
     * @returns Fix result with details
     */
    fix(workspaceRoot: string, violations: SSOTViolation[]): Promise<SSOTFixResult>;
    /**
     * Start watching for openapi.json changes
     *
     * @param workspaceRoot - Root path of the workspace
     */
    startWatching(workspaceRoot: string): void;
    /**
     * Stop watching for changes
     */
    stopWatching(): void;
    /**
     * Dispose resources
     */
    dispose(): void;
    /**
     * Find all openapi.json files in workspace
     */
    private findOpenapiFiles;
    /**
     * Find canonical openapi.json path
     */
    private findCanonicalPath;
    /**
     * Get file stats with symlink detection
     */
    private getFileStats;
    /**
     * Handle openapi.json file changes
     */
    private onOpenapiChange;
    /**
     * Update VS Code diagnostics panel with violations
     */
    private updateDiagnostics;
}
/**
 * Register SSOT validation commands
 *
 * @param context - VS Code extension context
 * @returns SSOTValidator instance
 */
export declare function registerSSOTCommands(context: vscode.ExtensionContext): SSOTValidator;
//# sourceMappingURL=ssotValidator.d.ts.map