/**
 * SDLC Structure Generator Service
 *
 * Generates SDLC 5.0.0 compliant folder structures based on tier selection.
 * Supports offline mode with local-first approach.
 *
 * Sprint 32 - SDLC 5.0.0 Onboarding
 * @version 0.2.0
 */
/**
 * SDLC 5.0.0 Tier Classification
 */
export type SDLCTier = 'LITE' | 'STANDARD' | 'PROFESSIONAL' | 'ENTERPRISE';
/**
 * SDLC 5.0.0 Stage definitions
 */
export interface SDLCStage {
    number: string;
    name: string;
    displayName: string;
    description: string;
    folder: string;
    requiredTiers: SDLCTier[];
}
/**
 * SDLC Config file schema (.sdlc-config.json)
 */
export interface SDLCConfig {
    $schema: string;
    version: string;
    project: {
        id: string;
        name: string;
        slug: string;
    };
    sdlc: {
        frameworkVersion: string;
        tier: SDLCTier;
        stages: Record<string, string>;
    };
    server: {
        url: string;
        connected: boolean;
    };
    gates: {
        current: string;
        passed: string[];
    };
}
/**
 * Gap analysis result
 */
export interface GapAnalysisResult {
    existingFolders: string[];
    missingFolders: string[];
    suggestedMappings: Record<string, string>;
    recommendations: string[];
}
/**
 * Tier descriptions for UI
 */
export declare const TIER_DESCRIPTIONS: Record<SDLCTier, {
    label: string;
    description: string;
    teamSize: string;
}>;
/**
 * SDLC Structure Generator Service
 */
export declare class SDLCStructureService {
    private readonly configFileName;
    private readonly schemaUrl;
    /**
     * Check if current workspace has an SDLC config file
     */
    hasSDLCConfig(workspaceRoot: string): boolean;
    /**
     * Check if workspace folder is empty or has minimal files
     */
    isEmptyOrMinimalFolder(workspaceRoot: string): boolean;
    /**
     * Get stages for a specific tier
     */
    getStagesForTier(tier: SDLCTier): SDLCStage[];
    /**
     * Generate SDLC config object
     */
    generateConfig(projectName: string, tier: SDLCTier, serverUrl?: string): SDLCConfig;
    /**
     * Generate folder structure for a tier
     */
    generateStructure(workspaceRoot: string, projectName: string, tier: SDLCTier, options?: {
        createTemplates?: boolean;
        serverUrl?: string;
    }): {
        success: boolean;
        createdFolders: string[];
        createdFiles: string[];
    };
    /**
     * Generate template files based on tier
     */
    private generateTemplateFiles;
    /**
     * Generate recommended VS Code settings
     */
    private generateVSCodeSettings;
    /**
     * Perform gap analysis on existing folder structure
     */
    analyzeExistingStructure(workspaceRoot: string, targetTier: SDLCTier): GapAnalysisResult;
    /**
     * Read existing SDLC config
     */
    readConfig(workspaceRoot: string): SDLCConfig | null;
    /**
     * Update existing SDLC config
     */
    updateConfig(workspaceRoot: string, updates: Partial<SDLCConfig>): boolean;
}
//# sourceMappingURL=sdlcStructureService.d.ts.map