/**
 * Admin System Settings Page - SDLC Orchestrator
 *
 * @module frontend/src/app/app/admin/settings/page
 * @description System-wide settings administration for superusers
 * @sdlc SDLC 6.0.6 Framework - Sprint 86 Phase 2 (ADR-027)
 * @status Sprint 86 - System Settings Admin UI
 */

"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useSystemSettingsAdmin } from "@/hooks/useSystemSettings";
import {
  SECURITY_SETTINGS_META,
  LIMITS_SETTINGS_META,
  FEATURE_SETTINGS_META,
  AI_SETTINGS_META,
  formatCategoryName,
  getCategoryDescription,
} from "@/lib/types/system-settings";
import type {
  SystemSettingItem,
  SecuritySettingMeta,
  LimitsSettingMeta,
  FeatureSettingMeta,
  AISettingMeta,
  SettingCategory,
} from "@/lib/types/system-settings";

// =============================================================================
// Icons
// =============================================================================

function ShieldCheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
    </svg>
  );
}

function AdjustmentsIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
    </svg>
  );
}

function CubeIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m21 7.5-9-5.25L3 7.5m18 0-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
    </svg>
  );
}

function SparklesIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
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

function ExclamationTriangleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
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

function InformationCircleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
    </svg>
  );
}

function LockClosedIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
    </svg>
  );
}

// =============================================================================
// Helper Functions
// =============================================================================

function formatRelativeTime(dateStr: string | null): string {
  if (!dateStr) return "Never";
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins} min ago`;
  if (diffHours < 24) return `${diffHours} hours ago`;
  if (diffDays < 30) return `${diffDays} days ago`;
  return new Date(dateStr).toLocaleDateString();
}

// =============================================================================
// Components
// =============================================================================

interface CategoryTabProps {
  category: SettingCategory;
  isActive: boolean;
  onClick: () => void;
  icon: React.ReactNode;
}

function CategoryTab({ category, isActive, onClick, icon }: CategoryTabProps) {
  return (
    <button
      onClick={onClick}
      className={`
        flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-colors
        ${isActive
          ? "bg-blue-100 text-blue-700"
          : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
        }
      `}
    >
      {icon}
      {formatCategoryName(category)}
    </button>
  );
}

interface NumberSettingRowProps {
  setting: SystemSettingItem | undefined;
  meta: SecuritySettingMeta | LimitsSettingMeta | {
    key: string;
    label: string;
    description: string;
    type: "number";
    min?: number;
    max?: number;
    step?: number;
    unit?: string;
    default: number;
  };
  onUpdate: (key: string, value: number) => void;
  isUpdating: boolean;
}

function NumberSettingRow({
  setting,
  meta,
  onUpdate,
  isUpdating,
}: NumberSettingRowProps) {
  const [editValue, setEditValue] = useState<string | null>(null);
  const currentValue = setting?.value as number ?? meta.default;

  const handleSave = () => {
    if (editValue !== null) {
      const numValue = parseInt(editValue);
      if (!isNaN(numValue)) {
        onUpdate(meta.key, numValue);
      }
      setEditValue(null);
    }
  };

  const handleCancel = () => {
    setEditValue(null);
  };

  return (
    <div className="flex items-center justify-between py-4 border-b border-gray-100 last:border-b-0">
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="font-medium text-gray-900">{meta.label}</span>
          {meta.unit && (
            <span className="text-xs text-gray-400">({meta.unit})</span>
          )}
        </div>
        <p className="text-sm text-gray-500 mt-1">{meta.description}</p>
        {setting?.updated_at && (
          <p className="text-xs text-gray-400 mt-1">
            Last updated: {formatRelativeTime(setting.updated_at)}
            {setting.updated_by && ` by ${setting.updated_by}`}
          </p>
        )}
      </div>
      <div className="flex items-center gap-3">
        {editValue !== null ? (
          <>
            <input
              type="number"
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              min={meta.min}
              max={meta.max}
              className="w-24 px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <button
              onClick={handleSave}
              disabled={isUpdating}
              className="p-1.5 text-green-600 hover:bg-green-50 rounded-lg disabled:opacity-50"
            >
              <CheckIcon className="h-4 w-4" />
            </button>
            <button
              onClick={handleCancel}
              className="p-1.5 text-gray-400 hover:bg-gray-100 rounded-lg"
            >
              <span className="text-xs">Cancel</span>
            </button>
          </>
        ) : (
          <>
            <span className="font-mono text-sm bg-gray-100 px-3 py-1.5 rounded-lg min-w-[80px] text-center">
              {currentValue}
            </span>
            <button
              onClick={() => setEditValue(String(currentValue))}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Edit
            </button>
          </>
        )}
      </div>
    </div>
  );
}

interface BooleanSettingRowProps {
  setting: SystemSettingItem | undefined;
  meta: FeatureSettingMeta | { key: string; label: string; description: string; default: boolean };
  onUpdate: (key: string, value: boolean) => void;
  isUpdating: boolean;
}

function BooleanSettingRow({
  setting,
  meta,
  onUpdate,
  isUpdating,
}: BooleanSettingRowProps) {
  const currentValue = setting?.value as boolean ?? meta.default;

  const handleToggle = () => {
    onUpdate(meta.key, !currentValue);
  };

  return (
    <div className="flex items-center justify-between py-4 border-b border-gray-100 last:border-b-0">
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="font-medium text-gray-900">{meta.label}</span>
          {currentValue && (
            <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
              Enabled
            </span>
          )}
        </div>
        <p className="text-sm text-gray-500 mt-1">{meta.description}</p>
        {setting?.updated_at && (
          <p className="text-xs text-gray-400 mt-1">
            Last updated: {formatRelativeTime(setting.updated_at)}
            {setting.updated_by && ` by ${setting.updated_by}`}
          </p>
        )}
      </div>
      <div className="flex items-center gap-3">
        <button
          onClick={handleToggle}
          disabled={isUpdating}
          className={`
            relative inline-flex h-6 w-11 items-center rounded-full transition-colors
            ${currentValue ? "bg-blue-600" : "bg-gray-200"}
            ${isUpdating ? "opacity-50 cursor-wait" : "cursor-pointer"}
          `}
        >
          <span
            className={`
              inline-block h-4 w-4 transform rounded-full bg-white transition-transform
              ${currentValue ? "translate-x-6" : "translate-x-1"}
            `}
          />
        </button>
      </div>
    </div>
  );
}

interface SelectSettingRowProps {
  setting: SystemSettingItem | undefined;
  meta: AISettingMeta;
  onUpdate: (key: string, value: string) => void;
  isUpdating: boolean;
}

function SelectSettingRow({
  setting,
  meta,
  onUpdate,
  isUpdating,
}: SelectSettingRowProps) {
  const currentValue = setting?.value as string ?? meta.default;

  return (
    <div className="flex items-center justify-between py-4 border-b border-gray-100 last:border-b-0">
      <div className="flex-1">
        <span className="font-medium text-gray-900">{meta.label}</span>
        <p className="text-sm text-gray-500 mt-1">{meta.description}</p>
        {setting?.updated_at && (
          <p className="text-xs text-gray-400 mt-1">
            Last updated: {formatRelativeTime(setting.updated_at)}
          </p>
        )}
      </div>
      <div className="flex items-center gap-3">
        <select
          value={currentValue}
          onChange={(e) => onUpdate(meta.key, e.target.value)}
          disabled={isUpdating}
          className="px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50"
        >
          {meta.options?.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

// =============================================================================
// Main Component
// =============================================================================

export default function AdminSettingsPage() {
  const { user } = useAuth();
  const [activeCategory, setActiveCategory] = useState<SettingCategory>("security");
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    securitySettings,
    limitsSettings,
    featureSettings,
    aiSettings,
    isLoading,
    error,
    updateSettingAsync,
    isUpdating,
    refetch,
  } = useSystemSettingsAdmin();

  // Check if user is superuser
  const isSuperuser = user?.roles?.includes("admin") || user?.roles?.includes("superuser");

  const handleUpdateSetting = async (key: string, value: unknown) => {
    try {
      await updateSettingAsync({ key, data: { value } });
      setSuccessMessage(`Setting "${key}" updated successfully`);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      console.error("Failed to update setting:", err);
    }
  };

  // Access denied view
  if (!isSuperuser) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <LockClosedIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h2 className="mt-4 text-lg font-semibold text-gray-900">Access Denied</h2>
          <p className="mt-2 text-sm text-gray-500">
            You need superuser privileges to access system settings.
          </p>
        </div>
      </div>
    );
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="p-6 max-w-5xl mx-auto">
        <div className="animate-pulse space-y-6">
          <div className="h-8 w-64 bg-gray-200 rounded" />
          <div className="h-4 w-96 bg-gray-100 rounded" />
          <div className="flex gap-2">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-10 w-28 bg-gray-200 rounded-lg" />
            ))}
          </div>
          <div className="bg-white rounded-lg border p-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex justify-between py-4 border-b last:border-b-0">
                <div className="space-y-2">
                  <div className="h-5 w-40 bg-gray-200 rounded" />
                  <div className="h-4 w-64 bg-gray-100 rounded" />
                </div>
                <div className="h-8 w-24 bg-gray-200 rounded-lg" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="p-6 max-w-5xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
            <div>
              <h3 className="font-medium text-red-800">Failed to load settings</h3>
              <p className="text-sm text-red-600">{error.message}</p>
            </div>
          </div>
          <button
            onClick={() => refetch()}
            className="mt-3 flex items-center gap-2 text-sm text-red-600 hover:text-red-700"
          >
            <ArrowPathIcon className="h-4 w-4" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">System Settings</h1>
        <p className="text-gray-500 mt-1">
          Configure platform-wide security, limits, and features. Changes propagate within 5 minutes.
        </p>
      </div>

      {/* Success Message */}
      {successMessage && (
        <div className="mb-4 bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">
          <CheckIcon className="h-5 w-5 text-green-600" />
          <span className="text-sm text-green-800">{successMessage}</span>
        </div>
      )}

      {/* Cache Notice */}
      <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-start gap-2">
        <InformationCircleIcon className="h-5 w-5 text-blue-600 mt-0.5" />
        <div>
          <p className="text-sm text-blue-800">
            <strong>ADR-027 Phase 1:</strong> Settings are cached in Redis with 5-minute TTL.
            Changes take effect within 5 minutes across all services.
          </p>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        <CategoryTab
          category="security"
          isActive={activeCategory === "security"}
          onClick={() => setActiveCategory("security")}
          icon={<ShieldCheckIcon className="h-4 w-4" />}
        />
        <CategoryTab
          category="limits"
          isActive={activeCategory === "limits"}
          onClick={() => setActiveCategory("limits")}
          icon={<AdjustmentsIcon className="h-4 w-4" />}
        />
        <CategoryTab
          category="features"
          isActive={activeCategory === "features"}
          onClick={() => setActiveCategory("features")}
          icon={<CubeIcon className="h-4 w-4" />}
        />
        <CategoryTab
          category="ai"
          isActive={activeCategory === "ai"}
          onClick={() => setActiveCategory("ai")}
          icon={<SparklesIcon className="h-4 w-4" />}
        />
      </div>

      {/* Settings Panel */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-4 border-b bg-gray-50">
          <h2 className="font-semibold text-gray-900">
            {formatCategoryName(activeCategory)}
          </h2>
          <p className="text-sm text-gray-500">
            {getCategoryDescription(activeCategory)}
          </p>
        </div>

        <div className="p-4">
          {/* Security Settings */}
          {activeCategory === "security" && (
            <div className="space-y-1">
              {SECURITY_SETTINGS_META.map((meta) => {
                const setting = securitySettings.find((s) => s.key === meta.key);
                return meta.type === "boolean" ? (
                  <BooleanSettingRow
                    key={meta.key}
                    setting={setting}
                    meta={{
                      key: meta.key,
                      label: meta.label,
                      description: meta.description,
                      default: meta.default as boolean,
                    }}
                    onUpdate={(key, value) => handleUpdateSetting(key, value)}
                    isUpdating={isUpdating}
                  />
                ) : (
                  <NumberSettingRow
                    key={meta.key}
                    setting={setting}
                    meta={meta}
                    onUpdate={(key, value) => handleUpdateSetting(key, value)}
                    isUpdating={isUpdating}
                  />
                );
              })}
            </div>
          )}

          {/* Limits Settings */}
          {activeCategory === "limits" && (
            <div className="space-y-1">
              {LIMITS_SETTINGS_META.map((meta) => {
                const setting = limitsSettings.find((s) => s.key === meta.key);
                return (
                  <NumberSettingRow
                    key={meta.key}
                    setting={setting}
                    meta={meta}
                    onUpdate={(key, value) => handleUpdateSetting(key, value)}
                    isUpdating={isUpdating}
                  />
                );
              })}
            </div>
          )}

          {/* Feature Flags */}
          {activeCategory === "features" && (
            <div className="space-y-1">
              {FEATURE_SETTINGS_META.map((meta) => {
                const setting = featureSettings.find((s) => s.key === meta.key);
                return (
                  <BooleanSettingRow
                    key={meta.key}
                    setting={setting}
                    meta={meta}
                    onUpdate={(key, value) => handleUpdateSetting(key, value)}
                    isUpdating={isUpdating}
                  />
                );
              })}
            </div>
          )}

          {/* AI Settings */}
          {activeCategory === "ai" && (
            <div className="space-y-1">
              {AI_SETTINGS_META.map((meta) => {
                const setting = aiSettings.find((s) => s.key === meta.key);
                if (meta.type === "select") {
                  return (
                    <SelectSettingRow
                      key={meta.key}
                      setting={setting}
                      meta={meta}
                      onUpdate={(key, value) => handleUpdateSetting(key, value)}
                      isUpdating={isUpdating}
                    />
                  );
                } else if (meta.type === "boolean") {
                  return (
                    <BooleanSettingRow
                      key={meta.key}
                      setting={setting}
                      meta={{ ...meta, default: meta.default as boolean }}
                      onUpdate={(key, value) => handleUpdateSetting(key, value)}
                      isUpdating={isUpdating}
                    />
                  );
                } else {
                  return (
                    <NumberSettingRow
                      key={meta.key}
                      setting={setting}
                      meta={{
                        key: meta.key,
                        label: meta.label,
                        description: meta.description,
                        type: "number" as const,
                        min: meta.min ?? 0,
                        max: meta.max ?? 100000,
                        step: meta.step,
                        default: meta.default as number,
                      }}
                      onUpdate={(key, value) => handleUpdateSetting(key, value)}
                      isUpdating={isUpdating}
                    />
                  );
                }
              })}
            </div>
          )}
        </div>
      </div>

      {/* Documentation Link */}
      <div className="mt-6 text-sm text-gray-500">
        <p>
          See{" "}
          <a
            href="https://docs.sdlc-orchestrator.io/admin/settings"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            ADR-027 documentation
          </a>{" "}
          for detailed information about each setting.
        </p>
      </div>
    </div>
  );
}
