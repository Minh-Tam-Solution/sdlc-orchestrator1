/**
 * CLI Token Types - SDLC Orchestrator
 *
 * @module frontend/src/lib/types/cli-token
 * @description TypeScript interfaces for CLI Authentication (Sprint 85)
 * @sdlc SDLC 5.1.3 Framework - Sprint 85 (CLI Authentication)
 * @status Sprint 85 - CTO APPROVED (January 20, 2026)
 */

// =============================================================================
// Core CLI Token Types
// =============================================================================

/**
 * CLI Token represents a token issued for CLI/terminal access
 * Distinct from API Keys - designed for interactive CLI sessions
 */
export interface CliToken {
  id: string;
  user_id: string;
  name: string;
  token_prefix: string;
  device_name: string | null;
  device_id: string | null;
  ip_address: string | null;
  user_agent: string | null;
  scopes: CliTokenScope[];
  is_active: boolean;
  last_used_at: string | null;
  expires_at: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * CLI Token scopes define what operations the token can perform
 */
export type CliTokenScope =
  | "cli:read"           // Read project/gate/evidence data
  | "cli:write"          // Create/update evidence, run gates
  | "cli:admin"          // Admin operations (manage tokens)
  | "agents:read"        // Read AGENTS.md files
  | "agents:write"       // Generate/regenerate AGENTS.md
  | "gates:evaluate"     // Evaluate gates
  | "evidence:submit"    // Submit evidence
  | "projects:read"      // Read projects
  | "projects:write";    // Create/update projects

/**
 * Response when creating a new CLI token
 * Includes the full token (only shown once)
 */
export interface CliTokenCreatedResponse {
  id: string;
  name: string;
  token: string;  // Full token - only returned on creation
  token_prefix: string;
  device_name: string | null;
  scopes: CliTokenScope[];
  expires_at: string | null;
  created_at: string;
}

/**
 * Request to create a new CLI token
 */
export interface CreateCliTokenRequest {
  name: string;
  device_name?: string;
  scopes?: CliTokenScope[];
  expires_in_days?: number | null;  // null = never expires
}

/**
 * Request to refresh/rotate a CLI token
 */
export interface RefreshCliTokenRequest {
  token_id: string;
  extend_days?: number;  // Extend expiry by N days
}

/**
 * Response when refreshing a CLI token
 */
export interface RefreshCliTokenResponse {
  id: string;
  new_token: string;
  token_prefix: string;
  expires_at: string | null;
}

// =============================================================================
// CLI Session Types
// =============================================================================

/**
 * CLI Session represents an active CLI session
 */
export interface CliSession {
  id: string;
  token_id: string;
  device_name: string | null;
  ip_address: string;
  started_at: string;
  last_activity_at: string;
  is_active: boolean;
  commands_executed: number;
}

/**
 * CLI Login flow state
 */
export type CliLoginState =
  | "pending"       // Waiting for user to authenticate
  | "authenticated" // User authenticated, token ready
  | "expired"       // Login request expired
  | "cancelled";    // User cancelled login

/**
 * CLI Login request (device flow)
 */
export interface CliLoginRequest {
  device_code: string;
  user_code: string;
  verification_url: string;
  expires_in: number;
  interval: number;
  state: CliLoginState;
}

/**
 * CLI Login verification response
 */
export interface CliLoginVerification {
  state: CliLoginState;
  token?: CliTokenCreatedResponse;
  error?: string;
}

// =============================================================================
// CLI Token List/Query Types
// =============================================================================

/**
 * Parameters for listing CLI tokens
 */
export interface CliTokenListParams {
  page?: number;
  page_size?: number;
  is_active?: boolean;
  include_expired?: boolean;
}

/**
 * Paginated response for CLI tokens
 */
export interface CliTokensResponse {
  items: CliToken[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

/**
 * CLI Token usage statistics
 */
export interface CliTokenStats {
  total_tokens: number;
  active_tokens: number;
  expired_tokens: number;
  revoked_tokens: number;
  total_sessions: number;
  active_sessions: number;
  commands_last_24h: number;
  commands_last_7d: number;
  most_used_token_id: string | null;
  last_activity_at: string | null;
}

// =============================================================================
// CLI Device Types
// =============================================================================

/**
 * Registered CLI device
 */
export interface CliDevice {
  id: string;
  name: string;
  device_id: string;
  os_type: "windows" | "macos" | "linux" | "unknown";
  cli_version: string | null;
  last_seen_at: string | null;
  is_trusted: boolean;
  created_at: string;
}

// =============================================================================
// Scope Metadata
// =============================================================================

/**
 * Metadata for CLI token scopes
 */
export interface ScopeMetadata {
  scope: CliTokenScope;
  label: string;
  description: string;
  category: "core" | "agents" | "gates" | "evidence" | "projects";
  is_dangerous: boolean;
}

/**
 * All available CLI scopes with metadata
 */
export const CLI_SCOPES: ScopeMetadata[] = [
  {
    scope: "cli:read",
    label: "CLI Read",
    description: "Read project, gate, and evidence data via CLI",
    category: "core",
    is_dangerous: false,
  },
  {
    scope: "cli:write",
    label: "CLI Write",
    description: "Create and update evidence, run gates via CLI",
    category: "core",
    is_dangerous: false,
  },
  {
    scope: "cli:admin",
    label: "CLI Admin",
    description: "Manage CLI tokens and sessions",
    category: "core",
    is_dangerous: true,
  },
  {
    scope: "agents:read",
    label: "Read AGENTS.md",
    description: "Read AGENTS.md files and context overlays",
    category: "agents",
    is_dangerous: false,
  },
  {
    scope: "agents:write",
    label: "Write AGENTS.md",
    description: "Generate and regenerate AGENTS.md files",
    category: "agents",
    is_dangerous: false,
  },
  {
    scope: "gates:evaluate",
    label: "Evaluate Gates",
    description: "Run gate evaluations and view results",
    category: "gates",
    is_dangerous: false,
  },
  {
    scope: "evidence:submit",
    label: "Submit Evidence",
    description: "Upload and submit evidence artifacts",
    category: "evidence",
    is_dangerous: false,
  },
  {
    scope: "projects:read",
    label: "Read Projects",
    description: "View project details and configurations",
    category: "projects",
    is_dangerous: false,
  },
  {
    scope: "projects:write",
    label: "Write Projects",
    description: "Create and update project settings",
    category: "projects",
    is_dangerous: false,
  },
];

/**
 * Default scopes for new CLI tokens
 */
export const DEFAULT_CLI_SCOPES: CliTokenScope[] = [
  "cli:read",
  "cli:write",
  "agents:read",
  "agents:write",
  "gates:evaluate",
  "evidence:submit",
  "projects:read",
];

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Get scope metadata by scope name
 */
export function getScopeMetadata(scope: CliTokenScope): ScopeMetadata | undefined {
  return CLI_SCOPES.find((s) => s.scope === scope);
}

/**
 * Get scopes grouped by category
 */
export function getScopesByCategory(): Record<string, ScopeMetadata[]> {
  return CLI_SCOPES.reduce((acc, scope) => {
    if (!acc[scope.category]) {
      acc[scope.category] = [];
    }
    acc[scope.category].push(scope);
    return acc;
  }, {} as Record<string, ScopeMetadata[]>);
}

/**
 * Check if a token is expired
 */
export function isTokenExpired(token: CliToken): boolean {
  if (!token.expires_at) return false;
  return new Date(token.expires_at) < new Date();
}

/**
 * Get token status
 */
export function getTokenStatus(
  token: CliToken
): "active" | "expired" | "revoked" {
  if (!token.is_active) return "revoked";
  if (isTokenExpired(token)) return "expired";
  return "active";
}

/**
 * Get token status display config
 */
export function getTokenStatusConfig(status: "active" | "expired" | "revoked"): {
  label: string;
  bgColor: string;
  textColor: string;
  icon: string;
} {
  const configs = {
    active: {
      label: "Active",
      bgColor: "bg-green-100",
      textColor: "text-green-800",
      icon: "✓",
    },
    expired: {
      label: "Expired",
      bgColor: "bg-yellow-100",
      textColor: "text-yellow-800",
      icon: "⏰",
    },
    revoked: {
      label: "Revoked",
      bgColor: "bg-red-100",
      textColor: "text-red-800",
      icon: "✗",
    },
  };
  return configs[status];
}

/**
 * Format token expiry
 */
export function formatTokenExpiry(expiresAt: string | null): string {
  if (!expiresAt) return "Never";
  const date = new Date(expiresAt);
  const now = new Date();
  const diffMs = date.getTime() - now.getTime();
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffDays < 0) return "Expired";
  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "Tomorrow";
  if (diffDays < 7) return `${diffDays} days`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks`;
  return date.toLocaleDateString();
}

/**
 * Format last used time
 */
export function formatLastUsed(lastUsedAt: string | null): string {
  if (!lastUsedAt) return "Never used";
  const date = new Date(lastUsedAt);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

/**
 * Get OS icon for device
 */
export function getOsIcon(osType: CliDevice["os_type"]): string {
  const icons = {
    windows: "🪟",
    macos: "🍎",
    linux: "🐧",
    unknown: "💻",
  };
  return icons[osType];
}

/**
 * Mask token for display (show only prefix)
 */
export function maskToken(tokenPrefix: string): string {
  return `${tokenPrefix}${"•".repeat(32)}`;
}

/**
 * Calculate token stats summary
 */
export function calculateTokenStatsSummary(tokens: CliToken[]): {
  active: number;
  expired: number;
  revoked: number;
  total: number;
} {
  return tokens.reduce(
    (acc, token) => {
      const status = getTokenStatus(token);
      acc[status]++;
      acc.total++;
      return acc;
    },
    { active: 0, expired: 0, revoked: 0, total: 0 }
  );
}
