/**
 * CLI Tokens Management Page - SDLC Orchestrator
 *
 * @module frontend/src/app/app/cli-tokens/page
 * @description CLI token management for terminal/CLI authentication (Sprint 85)
 * @sdlc SDLC 6.0.6 Framework - Sprint 85 (CLI Authentication)
 * @status Sprint 85 - CTO APPROVED (January 20, 2026)
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import {
  useCliTokensDashboard,
  useCreateCliToken,
  useRevokeCliToken,
  useRevokeCliSession,
} from "@/hooks/useCliTokens";
import {
  getTokenStatus,
  getTokenStatusConfig,
  formatTokenExpiry,
  formatLastUsed,
  maskToken,
  CLI_SCOPES,
  DEFAULT_CLI_SCOPES,
  type CliTokenScope,
} from "@/lib/types/cli-token";

// =============================================================================
// Icon Components
// =============================================================================

function KeyIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z" />
    </svg>
  );
}

function PlusIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
  );
}

function ClipboardIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0 0 13.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 0 1-.75.75H9a.75.75 0 0 1-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 0 1-2.25 2.25H6.75A2.25 2.25 0 0 1 4.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 0 1 1.927-.184" />
    </svg>
  );
}

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
    </svg>
  );
}

function XMarkIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
    </svg>
  );
}

function ExclamationTriangleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
    </svg>
  );
}

function CommandLineIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m6.75 7.5 3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0 0 21 18V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v12a2.25 2.25 0 0 0 2.25 2.25Z" />
    </svg>
  );
}

function ComputerDesktopIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0V12a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 12V5.25" />
    </svg>
  );
}

function ArrowPathIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
    </svg>
  );
}

// =============================================================================
// Stats Card Component
// =============================================================================

function StatsCard({
  title,
  value,
  subtitle,
  icon: Icon,
  iconBg,
  iconColor,
}: {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ComponentType<{ className?: string }>;
  iconBg: string;
  iconColor: string;
}) {
  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="flex items-center gap-3">
        <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${iconBg}`}>
          <Icon className={`h-5 w-5 ${iconColor}`} />
        </div>
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {subtitle && <p className="text-xs text-gray-500">{subtitle}</p>}
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Token Row Component
// =============================================================================

function TokenRow({
  token,
  onRevoke,
}: {
  token: {
    id: string;
    name: string;
    token_prefix: string;
    device_name: string | null;
    scopes: CliTokenScope[];
    is_active: boolean;
    last_used_at: string | null;
    expires_at: string | null;
    created_at: string;
  };
  onRevoke: () => void;
}) {
  const status = getTokenStatus(token as Parameters<typeof getTokenStatus>[0]);
  const statusConfig = getTokenStatusConfig(status);

  return (
    <div className="flex items-center justify-between rounded-lg border bg-white p-4">
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <span className="font-medium text-gray-900">{token.name}</span>
          <span
            className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${statusConfig.bgColor} ${statusConfig.textColor}`}
          >
            {statusConfig.icon} {statusConfig.label}
          </span>
        </div>
        <div className="flex items-center gap-3 text-sm text-gray-500">
          <code className="rounded bg-gray-100 px-2 py-0.5 text-xs font-mono">
            {maskToken(token.token_prefix)}
          </code>
          <span>•</span>
          <span>Last used: {formatLastUsed(token.last_used_at)}</span>
          <span>•</span>
          <span>Expires: {formatTokenExpiry(token.expires_at)}</span>
        </div>
        {token.device_name && (
          <div className="flex items-center gap-1 text-sm text-gray-500">
            <ComputerDesktopIcon className="h-4 w-4" />
            {token.device_name}
          </div>
        )}
        <div className="flex flex-wrap gap-1 mt-1">
          {token.scopes.slice(0, 3).map((scope) => (
            <span
              key={scope}
              className="rounded bg-blue-50 px-1.5 py-0.5 text-xs text-blue-700"
            >
              {scope}
            </span>
          ))}
          {token.scopes.length > 3 && (
            <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-600">
              +{token.scopes.length - 3} more
            </span>
          )}
        </div>
      </div>
      <button
        onClick={onRevoke}
        disabled={!token.is_active}
        className="text-red-600 hover:text-red-700 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Revoke
      </button>
    </div>
  );
}

// =============================================================================
// Session Row Component
// =============================================================================

function SessionRow({
  session,
  onRevoke,
}: {
  session: {
    id: string;
    device_name: string | null;
    ip_address: string;
    started_at: string;
    last_activity_at: string;
    is_active: boolean;
    commands_executed: number;
  };
  onRevoke: () => void;
}) {
  return (
    <div className="flex items-center justify-between rounded-lg border bg-white p-4">
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <CommandLineIcon className="h-5 w-5 text-gray-400" />
          <span className="font-medium text-gray-900">
            {session.device_name || "Unknown Device"}
          </span>
          {session.is_active && (
            <span className="rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-800">
              Active
            </span>
          )}
        </div>
        <div className="flex items-center gap-3 text-sm text-gray-500">
          <span>IP: {session.ip_address}</span>
          <span>•</span>
          <span>{session.commands_executed} commands</span>
          <span>•</span>
          <span>Last activity: {formatLastUsed(session.last_activity_at)}</span>
        </div>
      </div>
      <button
        onClick={onRevoke}
        disabled={!session.is_active}
        className="text-red-600 hover:text-red-700 text-sm font-medium disabled:opacity-50"
      >
        End Session
      </button>
    </div>
  );
}

// =============================================================================
// Create Token Modal
// =============================================================================

function CreateTokenModal({
  isOpen,
  onClose,
  onCreate,
  isCreating,
  createdToken,
}: {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (data: {
    name: string;
    device_name?: string;
    scopes: CliTokenScope[];
    expires_in_days?: number | null;
  }) => void;
  isCreating: boolean;
  createdToken: { token: string; name: string } | null;
}) {
  const [name, setName] = useState("CLI Token");
  const [deviceName, setDeviceName] = useState("");
  const [expiry, setExpiry] = useState("90");
  const [selectedScopes, setSelectedScopes] = useState<CliTokenScope[]>(DEFAULT_CLI_SCOPES);
  const [copied, setCopied] = useState(false);

  const handleSubmit = () => {
    onCreate({
      name,
      device_name: deviceName || undefined,
      scopes: selectedScopes,
      expires_in_days: expiry === "never" ? null : parseInt(expiry),
    });
  };

  const handleCopy = async () => {
    if (createdToken?.token) {
      await navigator.clipboard.writeText(createdToken.token);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClose = () => {
    setName("CLI Token");
    setDeviceName("");
    setExpiry("90");
    setSelectedScopes(DEFAULT_CLI_SCOPES);
    setCopied(false);
    onClose();
  };

  const toggleScope = (scope: CliTokenScope) => {
    setSelectedScopes((prev) =>
      prev.includes(scope)
        ? prev.filter((s) => s !== scope)
        : [...prev, scope]
    );
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-lg shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
        {createdToken ? (
          // Show created token
          <div className="p-6">
            <div className="flex items-center gap-2 text-green-600 mb-4">
              <CheckIcon className="h-5 w-5" />
              <h3 className="text-lg font-semibold">CLI Token Created</h3>
            </div>
            <p className="text-sm text-gray-500 mb-4">
              Copy your CLI token now. You won&apos;t be able to see it again!
            </p>
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-4">
              <div className="flex items-start gap-3">
                <ExclamationTriangleIcon className="h-5 w-5 text-amber-600 mt-0.5" />
                <p className="text-sm text-amber-800">
                  Store this token securely. It provides access to your account via CLI.
                </p>
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Your CLI Token
              </label>
              <div className="flex gap-2">
                <code className="flex-1 rounded-lg border bg-gray-100 p-3 text-sm font-mono break-all">
                  {createdToken.token}
                </code>
                <button
                  onClick={handleCopy}
                  className="p-3 border rounded-lg hover:bg-gray-50"
                >
                  {copied ? (
                    <CheckIcon className="h-4 w-4 text-green-600" />
                  ) : (
                    <ClipboardIcon className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">
                Use this token to authenticate:
              </p>
              <code className="block text-sm bg-gray-800 text-green-400 p-3 rounded font-mono">
                sdlc login --token {createdToken.token.substring(0, 20)}...
              </code>
            </div>
            <button
              onClick={handleClose}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Done, I&apos;ve saved my token
            </button>
          </div>
        ) : (
          // Create token form
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Create CLI Token</h3>
              <button onClick={handleClose} className="text-gray-400 hover:text-gray-600">
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>
            <p className="text-sm text-gray-500 mb-4">
              Create a token for CLI authentication. Select the permissions this token should have.
            </p>

            <div className="space-y-4">
              {/* Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Token Name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="CLI Token"
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Device Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Device Name (optional)
                </label>
                <input
                  type="text"
                  value={deviceName}
                  onChange={(e) => setDeviceName(e.target.value)}
                  placeholder="MacBook Pro, Work Laptop, etc."
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Expiry */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Expiration
                </label>
                <select
                  value={expiry}
                  onChange={(e) => setExpiry(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="30">30 days</option>
                  <option value="90">90 days (Recommended)</option>
                  <option value="365">1 year</option>
                  <option value="never">Never expires</option>
                </select>
              </div>

              {/* Scopes */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Permissions
                </label>
                <div className="space-y-2 max-h-48 overflow-y-auto border rounded-lg p-3">
                  {CLI_SCOPES.map((scopeMeta) => (
                    <label
                      key={scopeMeta.scope}
                      className="flex items-start gap-3 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={selectedScopes.includes(scopeMeta.scope)}
                        onChange={() => toggleScope(scopeMeta.scope)}
                        className="mt-1 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-medium text-gray-900">
                            {scopeMeta.label}
                          </span>
                          {scopeMeta.is_dangerous && (
                            <span className="rounded bg-red-100 px-1.5 py-0.5 text-xs text-red-700">
                              Elevated
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500">{scopeMeta.description}</p>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleClose}
                className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSubmit}
                disabled={isCreating || !name.trim() || selectedScopes.length === 0}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {isCreating ? "Creating..." : "Create Token"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// =============================================================================
// Revoke Confirmation Modal
// =============================================================================

function RevokeModal({
  isOpen,
  onClose,
  onConfirm,
  isRevoking,
  itemName,
  itemType,
}: {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  isRevoking: boolean;
  itemName: string;
  itemType: "token" | "session";
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <h3 className="text-lg font-semibold mb-2">
          Revoke {itemType === "token" ? "CLI Token" : "Session"}?
        </h3>
        <p className="text-sm text-gray-500 mb-4">
          {itemType === "token"
            ? `This will immediately invalidate "${itemName}". Any CLI sessions using this token will be disconnected.`
            : `This will end the session on "${itemName}". The device will need to re-authenticate.`}
        </p>
        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={isRevoking}
            className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
          >
            {isRevoking ? "Revoking..." : "Revoke"}
          </button>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Main Page Component
// =============================================================================

export default function CliTokensPage() {
  const { tokens, stats, sessions, isLoading, refetchAll } = useCliTokensDashboard();
  const createMutation = useCreateCliToken();
  const revokeMutation = useRevokeCliToken();
  const revokeSessionMutation = useRevokeCliSession();

  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createdToken, setCreatedToken] = useState<{ token: string; name: string } | null>(null);
  const [revokeTarget, setRevokeTarget] = useState<{
    id: string;
    name: string;
    type: "token" | "session";
  } | null>(null);

  const handleCreate = async (data: {
    name: string;
    device_name?: string;
    scopes: CliTokenScope[];
    expires_in_days?: number | null;
  }) => {
    const result = await createMutation.mutateAsync(data);
    setCreatedToken({ token: result.token, name: result.name });
  };

  const handleCloseCreateModal = () => {
    setShowCreateModal(false);
    setCreatedToken(null);
  };

  const handleRevoke = async () => {
    if (!revokeTarget) return;

    if (revokeTarget.type === "token") {
      await revokeMutation.mutateAsync(revokeTarget.id);
    } else {
      await revokeSessionMutation.mutateAsync(revokeTarget.id);
    }
    setRevokeTarget(null);
  };

  if (isLoading) {
    return <CliTokensPageSkeleton />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">CLI Tokens</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage authentication tokens for CLI and terminal access
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => refetchAll()}
            className="inline-flex items-center gap-2 rounded-md bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            <ArrowPathIcon className="h-4 w-4" />
            Refresh
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700"
          >
            <PlusIcon className="h-4 w-4" />
            Create Token
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Tokens"
          value={stats?.total_tokens ?? 0}
          icon={KeyIcon}
          iconBg="bg-blue-100"
          iconColor="text-blue-600"
        />
        <StatsCard
          title="Active Tokens"
          value={stats?.active_tokens ?? 0}
          icon={CheckIcon}
          iconBg="bg-green-100"
          iconColor="text-green-600"
        />
        <StatsCard
          title="Active Sessions"
          value={stats?.active_sessions ?? 0}
          icon={CommandLineIcon}
          iconBg="bg-purple-100"
          iconColor="text-purple-600"
        />
        <StatsCard
          title="Commands (24h)"
          value={stats?.commands_last_24h ?? 0}
          icon={ArrowPathIcon}
          iconBg="bg-yellow-100"
          iconColor="text-yellow-600"
        />
      </div>

      {/* CLI Quick Start */}
      <div className="rounded-lg border bg-gradient-to-r from-gray-800 to-gray-900 p-6 text-white">
        <h2 className="text-lg font-semibold mb-2">Quick Start</h2>
        <p className="text-sm text-gray-300 mb-4">
          Install the SDLC CLI and authenticate with your token
        </p>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-gray-400">1.</span>
            <code className="bg-gray-700 px-2 py-1 rounded text-sm">
              pip install sdlc-cli
            </code>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-gray-400">2.</span>
            <code className="bg-gray-700 px-2 py-1 rounded text-sm">
              sdlc login --token YOUR_TOKEN
            </code>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-gray-400">3.</span>
            <code className="bg-gray-700 px-2 py-1 rounded text-sm">
              sdlc status
            </code>
          </div>
        </div>
        <Link
          href="/docs/cli-guide"
          className="inline-block mt-4 text-sm text-blue-400 hover:text-blue-300"
        >
          View full CLI documentation →
        </Link>
      </div>

      {/* Tokens Section */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Tokens</h2>
        {tokens.length > 0 ? (
          <div className="space-y-3">
            {tokens.map((token) => (
              <TokenRow
                key={token.id}
                token={token}
                onRevoke={() =>
                  setRevokeTarget({ id: token.id, name: token.name, type: "token" })
                }
              />
            ))}
          </div>
        ) : (
          <div className="rounded-lg border border-dashed bg-gray-50 p-8 text-center">
            <KeyIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-semibold text-gray-900">No CLI tokens</h3>
            <p className="mt-1 text-sm text-gray-500">
              Create a token to authenticate with the CLI
            </p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="mt-4 inline-flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              <PlusIcon className="h-4 w-4" />
              Create Your First Token
            </button>
          </div>
        )}
      </div>

      {/* Sessions Section */}
      {sessions.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Active Sessions</h2>
          <div className="space-y-3">
            {sessions.map((session) => (
              <SessionRow
                key={session.id}
                session={session}
                onRevoke={() =>
                  setRevokeTarget({
                    id: session.id,
                    name: session.device_name || "Unknown Device",
                    type: "session",
                  })
                }
              />
            ))}
          </div>
        </div>
      )}

      {/* Create Token Modal */}
      <CreateTokenModal
        isOpen={showCreateModal}
        onClose={handleCloseCreateModal}
        onCreate={handleCreate}
        isCreating={createMutation.isPending}
        createdToken={createdToken}
      />

      {/* Revoke Confirmation Modal */}
      <RevokeModal
        isOpen={!!revokeTarget}
        onClose={() => setRevokeTarget(null)}
        onConfirm={handleRevoke}
        isRevoking={revokeMutation.isPending || revokeSessionMutation.isPending}
        itemName={revokeTarget?.name ?? ""}
        itemType={revokeTarget?.type ?? "token"}
      />
    </div>
  );
}

// =============================================================================
// Loading Skeleton
// =============================================================================

function CliTokensPageSkeleton() {
  return (
    <div className="space-y-6">
      {/* Header skeleton */}
      <div className="flex items-start justify-between">
        <div>
          <div className="h-8 w-32 bg-gray-200 rounded animate-pulse" />
          <div className="mt-2 h-4 w-64 bg-gray-200 rounded animate-pulse" />
        </div>
        <div className="flex gap-2">
          <div className="h-10 w-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-10 w-32 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>

      {/* Stats skeleton */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-24 rounded-lg bg-gray-200 animate-pulse" />
        ))}
      </div>

      {/* Quick start skeleton */}
      <div className="h-48 rounded-lg bg-gray-200 animate-pulse" />

      {/* Tokens skeleton */}
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-24 rounded-lg bg-gray-200 animate-pulse" />
        ))}
      </div>
    </div>
  );
}
