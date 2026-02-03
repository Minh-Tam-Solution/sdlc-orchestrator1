"use client";

/**
 * User Organizations Panel
 *
 * Sprint: 146 - Organization Access Control
 * Reference: ADR-047-Organization-Invitation-System.md
 *
 * Displays the user's organizations with their subscription tiers.
 * Shows the effective tier badge prominently.
 */

import Link from "next/link";
import { TierBadge, type SubscriptionTier } from "./TierBadge";
import { useUserTier, type UserOrganization } from "@/hooks/useUserTier";

/** Organization row in the panel */
function OrganizationRow({ org }: { org: UserOrganization }) {
  return (
    <Link
      href={`/app/organizations/${org.slug}`}
      className="flex items-center justify-between rounded-md px-3 py-2 hover:bg-gray-50"
    >
      <div className="flex items-center gap-2">
        <BuildingOfficeIcon className="h-4 w-4 text-gray-400" />
        <div>
          <p className="text-sm font-medium text-gray-900">{org.name}</p>
          <p className="text-xs text-gray-500 capitalize">{org.role}</p>
        </div>
      </div>
      <TierBadge tier={org.plan} size="sm" variant="compact" />
    </Link>
  );
}

/** Building office icon */
function BuildingOfficeIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21"
      />
    </svg>
  );
}

/** Plus icon for adding organizations */
function PlusIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 4.5v15m7.5-7.5h-15"
      />
    </svg>
  );
}

interface UserOrganizationsPanelProps {
  /** Maximum number of organizations to show (rest collapsed) */
  maxVisible?: number;
  /** Whether to show the effective tier header */
  showEffectiveTier?: boolean;
  /** Additional CSS classes */
  className?: string;
}

/**
 * UserOrganizationsPanel Component
 *
 * Displays the user's organizations with their subscription tiers.
 *
 * @example
 * ```tsx
 * // In user profile dropdown
 * <UserOrganizationsPanel maxVisible={3} showEffectiveTier />
 * ```
 */
export function UserOrganizationsPanel({
  maxVisible = 5,
  showEffectiveTier = true,
  className,
}: UserOrganizationsPanelProps) {
  const {
    effectiveTier,
    organizations,
    organizationCount,
    isLoading,
    error,
  } = useUserTier();

  if (isLoading) {
    return (
      <div className={className}>
        <div className="animate-pulse space-y-2 p-3">
          <div className="h-6 w-24 rounded bg-gray-200" />
          <div className="h-10 w-full rounded bg-gray-100" />
          <div className="h-10 w-full rounded bg-gray-100" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={className}>
        <div className="p-3 text-sm text-red-500">
          Failed to load organizations
        </div>
      </div>
    );
  }

  const visibleOrgs = organizations.slice(0, maxVisible);
  const hiddenCount = organizationCount - maxVisible;

  return (
    <div className={className}>
      {/* Effective Tier Header */}
      {showEffectiveTier && (
        <div className="border-b border-gray-100 px-3 py-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-gray-500 uppercase">
              Your Plan
            </span>
            <TierBadge tier={effectiveTier} size="sm" />
          </div>
          <p className="mt-1 text-xs text-gray-400">
            Based on highest tier among your organizations
          </p>
        </div>
      )}

      {/* Organizations List */}
      <div className="py-1">
        <div className="px-3 py-1">
          <span className="text-xs font-medium text-gray-500 uppercase">
            Organizations ({organizationCount})
          </span>
        </div>

        {organizationCount === 0 ? (
          <div className="px-3 py-4 text-center">
            <BuildingOfficeIcon className="mx-auto h-8 w-8 text-gray-300" />
            <p className="mt-2 text-sm text-gray-500">No organizations yet</p>
            <Link
              href="/app/organizations/new"
              className="mt-2 inline-flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              <PlusIcon className="h-4 w-4" />
              Create Organization
            </Link>
          </div>
        ) : (
          <>
            {visibleOrgs.map((org) => (
              <OrganizationRow key={org.id} org={org} />
            ))}

            {hiddenCount > 0 && (
              <Link
                href="/app/organizations"
                className="block px-3 py-2 text-center text-sm text-blue-600 hover:text-blue-700"
              >
                View {hiddenCount} more organization{hiddenCount > 1 ? "s" : ""}
              </Link>
            )}
          </>
        )}
      </div>

      {/* Actions */}
      <div className="border-t border-gray-100 px-3 py-2">
        <Link
          href="/app/organizations"
          className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
        >
          <BuildingOfficeIcon className="h-4 w-4" />
          Manage Organizations
        </Link>
      </div>
    </div>
  );
}

export default UserOrganizationsPanel;
