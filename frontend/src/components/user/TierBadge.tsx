"use client";

/**
 * Tier Badge Component
 *
 * Sprint: 146 - Organization Access Control
 * Reference: ADR-047-Organization-Invitation-System.md
 *
 * Displays the user's effective subscription tier badge.
 * The effective tier is the HIGHEST tier among all organizations the user belongs to.
 *
 * Tier Hierarchy (highest to lowest):
 * - Enterprise (4): Full feature access, priority support
 * - Pro (3): Advanced features, standard support
 * - Starter (2): Basic features, community support
 * - Free (1): Limited features, self-service
 */

import { cn } from "@/lib/utils";

export type SubscriptionTier = "enterprise" | "pro" | "starter" | "free";

interface TierBadgeProps {
  /** The subscription tier to display */
  tier: SubscriptionTier;
  /** Size variant */
  size?: "sm" | "md" | "lg";
  /** Show full tier name or abbreviated */
  variant?: "full" | "compact";
  /** Additional CSS classes */
  className?: string;
}

/** Tier configuration with display names and colors */
const TIER_CONFIG: Record<
  SubscriptionTier,
  {
    label: string;
    shortLabel: string;
    bgColor: string;
    textColor: string;
    borderColor: string;
    icon: string;
  }
> = {
  enterprise: {
    label: "Enterprise",
    shortLabel: "ENT",
    bgColor: "bg-purple-100",
    textColor: "text-purple-800",
    borderColor: "border-purple-300",
    icon: "crown",
  },
  pro: {
    label: "Pro",
    shortLabel: "PRO",
    bgColor: "bg-blue-100",
    textColor: "text-blue-800",
    borderColor: "border-blue-300",
    icon: "star",
  },
  starter: {
    label: "Starter",
    shortLabel: "STR",
    bgColor: "bg-green-100",
    textColor: "text-green-800",
    borderColor: "border-green-300",
    icon: "zap",
  },
  free: {
    label: "Free",
    shortLabel: "FREE",
    bgColor: "bg-gray-100",
    textColor: "text-gray-700",
    borderColor: "border-gray-300",
    icon: "user",
  },
};

/** Size configuration for the badge */
const SIZE_CONFIG = {
  sm: "px-1.5 py-0.5 text-xs",
  md: "px-2 py-1 text-xs",
  lg: "px-3 py-1.5 text-sm",
};

/** Crown icon for Enterprise tier */
function CrownIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        fillRule="evenodd"
        d="M10 1l3 6 6-3-2 8H3L1 4l6 3 3-6z"
        clipRule="evenodd"
      />
    </svg>
  );
}

/** Star icon for Pro tier */
function StarIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  );
}

/** Zap icon for Starter tier */
function ZapIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        fillRule="evenodd"
        d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
        clipRule="evenodd"
      />
    </svg>
  );
}

/** User icon for Free tier */
function UserIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        fillRule="evenodd"
        d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
        clipRule="evenodd"
      />
    </svg>
  );
}

/** Get the appropriate icon component for a tier */
function TierIcon({
  tier,
  className,
}: {
  tier: SubscriptionTier;
  className?: string;
}) {
  const iconMap = {
    enterprise: CrownIcon,
    pro: StarIcon,
    starter: ZapIcon,
    free: UserIcon,
  };

  const IconComponent = iconMap[tier];
  return <IconComponent className={className} />;
}

/**
 * TierBadge Component
 *
 * Displays a styled badge showing the user's subscription tier.
 *
 * @example
 * ```tsx
 * // Basic usage
 * <TierBadge tier="enterprise" />
 *
 * // Compact variant (abbreviated)
 * <TierBadge tier="pro" variant="compact" />
 *
 * // Different sizes
 * <TierBadge tier="starter" size="lg" />
 * ```
 */
export function TierBadge({
  tier,
  size = "md",
  variant = "full",
  className,
}: TierBadgeProps) {
  const config = TIER_CONFIG[tier];
  const sizeClasses = SIZE_CONFIG[size];
  const label = variant === "full" ? config.label : config.shortLabel;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border font-medium",
        config.bgColor,
        config.textColor,
        config.borderColor,
        sizeClasses,
        className
      )}
    >
      <TierIcon tier={tier} className={size === "sm" ? "h-3 w-3" : "h-3.5 w-3.5"} />
      {label}
    </span>
  );
}

export default TierBadge;
