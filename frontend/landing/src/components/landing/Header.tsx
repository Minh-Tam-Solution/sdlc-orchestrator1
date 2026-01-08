/**
 * Header/Navigation - SDLC Orchestrator Landing Page
 *
 * @module frontend/landing/src/components/landing/Header
 * @description Sticky header with navigation and language toggle
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - Auth-aware Header
 */

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { Button } from "@/components/ui/button";
import { LanguageToggle } from "@/components/ui/LanguageToggle";
import { getCurrentUser, logout as apiLogout } from "@/lib/api";
import type { UserProfile } from "@/lib/api";

/**
 * Header component with responsive navigation and language toggle
 * Now auth-aware: shows user info when logged in
 * Sprint 69: Auto-redirect authenticated users from landing page to /app
 */
export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const t = useTranslations("header");
  const pathname = usePathname();
  const router = useRouter();

  // Check auth status on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userData = await getCurrentUser();
        setUser(userData);

        // Sprint 69: Auto-redirect authenticated users from landing page to /app
        // Only redirect from landing page (/) - not from other public pages like /pricing, /docs
        if (userData && pathname === "/") {
          router.push("/app");
        }
      } catch {
        // Not logged in or token expired
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    checkAuth();
  }, [pathname, router]);

  const handleLogout = async () => {
    try {
      await apiLogout();
    } catch {
      // Ignore logout errors
    }
    setUser(null);
    window.location.href = "/";
  };

  const navLinks = [
    { label: t("features"), href: "#features" },
    { label: t("pricing"), href: "#pricing" },
    { label: t("docs"), href: "/docs/getting-started" },
  ];

  // Check if user is superuser (for admin panel access)
  const isSuperuser = user?.is_superuser;

  return (
    <header
      className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
      role="banner"
    >
      <div className="container mx-auto px-4 md:px-6">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <span className="text-heading-3 font-bold text-foreground">SDLC</span>
            <span className="text-body-sm text-muted-foreground hidden sm:inline">
              Orchestrator
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6" aria-label="Main navigation">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-body-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* Desktop CTAs + Language Toggle */}
          <div className="hidden md:flex items-center gap-3">
            <LanguageToggle />
            {isLoading ? (
              <div className="h-9 w-20 animate-pulse rounded bg-gray-200" />
            ) : user ? (
              <>
                <Button asChild variant="ghost" size="sm">
                  <Link href="/app">
                    Dashboard
                  </Link>
                </Button>
                {isSuperuser && (
                  <Button asChild variant="outline" size="sm">
                    <Link href="/admin">
                      Admin
                    </Link>
                  </Button>
                )}
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">
                    {user.name || user.email}
                  </span>
                  <Button variant="outline" size="sm" onClick={handleLogout}>
                    {t("signOut") || "Sign Out"}
                  </Button>
                </div>
              </>
            ) : (
              <>
                <Button asChild variant="ghost" size="sm">
                  <Link href="/login">{t("signIn")}</Link>
                </Button>
                <Button asChild size="sm">
                  <Link href="/register">{t("getStarted")}</Link>
                </Button>
              </>
            )}
          </div>

          {/* Mobile: Language Toggle + Menu Button */}
          <div className="md:hidden flex items-center gap-2">
            <LanguageToggle />
            <button
              type="button"
              className="p-2 text-muted-foreground hover:text-foreground"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-menu"
              aria-label={mobileMenuOpen ? t("menu.close") : t("menu.open")}
            >
              {mobileMenuOpen ? (
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <nav
            id="mobile-menu"
            className="md:hidden py-4 border-t"
            aria-label="Mobile navigation"
          >
            <div className="flex flex-col gap-4">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-body font-medium text-muted-foreground hover:text-foreground transition-colors py-2"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
              <div className="flex flex-col gap-2 pt-4 border-t">
                {user ? (
                  <>
                    <div className="text-sm text-muted-foreground py-2">
                      {user.name || user.email}
                    </div>
                    <Button asChild variant="outline" className="w-full">
                      <Link href="/app">
                        Dashboard
                      </Link>
                    </Button>
                    {isSuperuser && (
                      <Button asChild variant="outline" className="w-full">
                        <Link href="/admin">
                          Admin Panel
                        </Link>
                      </Button>
                    )}
                    <Button variant="outline" className="w-full" onClick={handleLogout}>
                      {t("signOut") || "Sign Out"}
                    </Button>
                  </>
                ) : (
                  <>
                    <Button asChild variant="outline" className="w-full">
                      <Link href="/login">{t("signIn")}</Link>
                    </Button>
                    <Button asChild className="w-full">
                      <Link href="/register">{t("getStarted")}</Link>
                    </Button>
                  </>
                )}
              </div>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}
