/**
 * SDLC Orchestrator Telemetry Service - VSCode Extension
 *
 * Sprint 147 - Product Truth Layer
 * Tracks extension usage events for activation funnels.
 * Interface: "extension" for all events tracked through this module.
 *
 * Core Events Tracked:
 * - extension_command_executed (all commands)
 * - project_created (sdlc.init)
 * - first_validation_run (sdlc.validateSpec)
 * - spec_validated (sdlc.specValidation)
 * - first_evidence_uploaded (sdlc.uploadEvidence)
 *
 * @version 1.0.0
 * @author SDLC Orchestrator Team
 */

import * as vscode from 'vscode';
import { Logger } from '../utils/logger';
import { ConfigManager } from '../utils/config';

/**
 * Extension telemetry event names (snake_case past tense convention).
 */
export const ExtensionEvents = {
    // General extension events
    COMMAND_EXECUTED: 'extension_command_executed',
    EXTENSION_ACTIVATED: 'extension_activated',
    EXTENSION_DEACTIVATED: 'extension_deactivated',

    // Activation funnel events
    PROJECT_CREATED: 'project_created',
    PROJECT_CONNECTED_GITHUB: 'project_connected_github',
    FIRST_VALIDATION_RUN: 'first_validation_run',
    SPEC_VALIDATED: 'spec_validated',
    FIRST_EVIDENCE_UPLOADED: 'first_evidence_uploaded',
    FIRST_GATE_PASSED: 'first_gate_passed',

    // Engagement events
    AI_COUNCIL_USED: 'ai_council_used',
    CODE_GENERATED: 'code_generated',
    MAGIC_MODE_USED: 'magic_mode_used',
} as const;

export type ExtensionEventName = (typeof ExtensionEvents)[keyof typeof ExtensionEvents];

/**
 * Telemetry event properties
 */
interface TelemetryEventProperties {
    [key: string]: string | number | boolean | undefined | null;
}

/**
 * Telemetry event request payload
 */
interface TrackEventRequest {
    event_name: string;
    user_id?: string;
    project_id?: string;
    organization_id?: string;
    properties?: TelemetryEventProperties;
    session_id?: string;
    interface: 'extension';
}

/**
 * Telemetry Service for VSCode Extension
 *
 * Sends telemetry events to the SDLC Orchestrator backend.
 * Events are sent asynchronously and failures are silently logged.
 * Telemetry should never break the extension operation.
 */
export class TelemetryService {
    private static instance: TelemetryService | undefined;
    private enabled: boolean = true;
    private sessionId: string;
    private apiUrl: string;

    private constructor() {
        this.sessionId = this.generateSessionId();
        const config = ConfigManager.getInstance();
        this.apiUrl = config.apiUrl;

        // Check if telemetry is disabled via settings
        const disableConfig = vscode.workspace
            .getConfiguration('sdlc')
            .get<boolean>('telemetry.disabled');
        this.enabled = !disableConfig;

        Logger.debug(`[Telemetry] Initialized, enabled: ${this.enabled}`);
    }

    /**
     * Get singleton instance
     */
    static getInstance(): TelemetryService {
        if (!TelemetryService.instance) {
            TelemetryService.instance = new TelemetryService();
        }
        return TelemetryService.instance;
    }

    /**
     * Generate a unique session ID for correlating events
     */
    private generateSessionId(): string {
        return `ext-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;
    }

    /**
     * Get extension version from package.json
     */
    private getExtensionVersion(): string {
        try {
            const extension = vscode.extensions.getExtension('sdlc-orchestrator.sdlc-orchestrator');
            return extension?.packageJSON?.version ?? 'unknown';
        } catch {
            return 'unknown';
        }
    }

    /**
     * Track a telemetry event
     *
     * @param eventName - Event name (use ExtensionEvents constants)
     * @param properties - Optional event properties
     * @param projectId - Optional project ID for project-scoped events
     * @returns Promise<boolean> - True if event was tracked successfully
     */
    async trackEvent(
        eventName: ExtensionEventName | string,
        properties?: TelemetryEventProperties,
        projectId?: string
    ): Promise<boolean> {
        if (!this.enabled) {
            return false;
        }

        try {
            const payload: TrackEventRequest = {
                event_name: eventName,
                properties: {
                    ...properties,
                    timestamp: new Date().toISOString(),
                    extension_version: this.getExtensionVersion(),
                    vscode_version: vscode.version,
                },
                session_id: this.sessionId,
                interface: 'extension',
                ...(projectId ? { project_id: projectId } : {}),
            };

            // Get auth token if available
            const token = await this.getAuthToken();
            const headers: Record<string, string> = {
                'Content-Type': 'application/json',
            };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            // Use fetch API for HTTP request
            const response = await fetch(`${this.apiUrl}/telemetry/events`, {
                method: 'POST',
                headers,
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                Logger.debug(`[Telemetry] Failed to track event: ${eventName}, status: ${response.status}`);
                return false;
            }

            Logger.debug(`[Telemetry] Event tracked: ${eventName}`);
            return true;
        } catch (error) {
            // Silently log - telemetry should never break the extension
            Logger.debug(`[Telemetry] Error tracking event ${eventName}: ${error}`);
            return false;
        }
    }

    /**
     * Get auth token from SecretStorage
     */
    private async getAuthToken(): Promise<string | undefined> {
        try {
            // Access the secret storage through the extension context
            // This is a simplified version - in production, use AuthService
            // For now, return undefined if not authenticated
            // The AuthService handles token retrieval properly
            return undefined;
        } catch {
            return undefined;
        }
    }

    /**
     * Track command execution
     */
    async trackCommand(
        command: string,
        success: boolean = true,
        durationMs?: number,
        projectId?: string
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.COMMAND_EXECUTED,
            {
                command,
                success,
                duration_ms: durationMs,
            },
            projectId
        );
    }

    /**
     * Track extension activation
     */
    async trackActivation(): Promise<boolean> {
        return this.trackEvent(ExtensionEvents.EXTENSION_ACTIVATED, {
            vscode_version: vscode.version,
            platform: process.platform,
        });
    }

    /**
     * Track extension deactivation
     */
    async trackDeactivation(): Promise<boolean> {
        return this.trackEvent(ExtensionEvents.EXTENSION_DEACTIVATED);
    }

    /**
     * Track project initialization via extension
     */
    async trackProjectCreated(
        projectId: string,
        tier: string,
        template?: string
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.PROJECT_CREATED,
            {
                tier,
                template_used: template,
                source: 'extension',
            },
            projectId
        );
    }

    /**
     * Track GitHub connection
     */
    async trackGitHubConnected(
        projectId: string,
        githubRepo: string
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.PROJECT_CONNECTED_GITHUB,
            { github_repo: githubRepo },
            projectId
        );
    }

    /**
     * Track validation run
     */
    async trackValidationRun(
        projectId: string,
        validationType: string,
        result: 'pass' | 'fail',
        errorsCount: number
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.FIRST_VALIDATION_RUN,
            {
                validation_type: validationType,
                result,
                errors_count: errorsCount,
            },
            projectId
        );
    }

    /**
     * Track spec validation
     */
    async trackSpecValidation(
        specCount: number,
        validCount: number,
        invalidCount: number,
        projectId?: string
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.SPEC_VALIDATED,
            {
                spec_count: specCount,
                valid_count: validCount,
                invalid_count: invalidCount,
                pass_rate: specCount > 0 ? (validCount / specCount) * 100 : 0,
            },
            projectId
        );
    }

    /**
     * Track evidence upload
     */
    async trackEvidenceUploaded(
        projectId: string,
        evidenceType: string,
        fileSizeBytes: number
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.FIRST_EVIDENCE_UPLOADED,
            {
                evidence_type: evidenceType,
                file_size_bytes: fileSizeBytes,
            },
            projectId
        );
    }

    /**
     * Track AI Council usage
     */
    async trackAICouncilUsed(
        projectId: string,
        queryType: string,
        responseTimeMs: number
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.AI_COUNCIL_USED,
            {
                query_type: queryType,
                response_time_ms: responseTimeMs,
            },
            projectId
        );
    }

    /**
     * Track code generation via Magic Mode
     */
    async trackMagicModeUsed(
        projectId: string,
        filesGenerated: number,
        durationMs: number
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.MAGIC_MODE_USED,
            {
                files_generated: filesGenerated,
                duration_ms: durationMs,
            },
            projectId
        );
    }

    /**
     * Track code generation
     */
    async trackCodeGenerated(
        projectId: string,
        language: string,
        linesGenerated: number
    ): Promise<boolean> {
        return this.trackEvent(
            ExtensionEvents.CODE_GENERATED,
            {
                language,
                lines_generated: linesGenerated,
            },
            projectId
        );
    }
}

// Export singleton getter
export function getTelemetry(): TelemetryService {
    return TelemetryService.getInstance();
}

// Convenience functions for quick access
export const trackCommand = (
    command: string,
    success?: boolean,
    durationMs?: number,
    projectId?: string
): Promise<boolean> => getTelemetry().trackCommand(command, success, durationMs, projectId);

export const trackActivation = (): Promise<boolean> => getTelemetry().trackActivation();

export const trackDeactivation = (): Promise<boolean> => getTelemetry().trackDeactivation();

export const trackProjectCreated = (
    projectId: string,
    tier: string,
    template?: string
): Promise<boolean> => getTelemetry().trackProjectCreated(projectId, tier, template);

export const trackValidationRun = (
    projectId: string,
    validationType: string,
    result: 'pass' | 'fail',
    errorsCount: number
): Promise<boolean> => getTelemetry().trackValidationRun(projectId, validationType, result, errorsCount);

export const trackSpecValidation = (
    specCount: number,
    validCount: number,
    invalidCount: number,
    projectId?: string
): Promise<boolean> => getTelemetry().trackSpecValidation(specCount, validCount, invalidCount, projectId);
