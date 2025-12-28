# Landing Page UI Design Specification

## Document Control

| Field | Value |
|-------|-------|
| Version | 1.1.0 |
| Status | SUBMITTED - Pending G2 Approval |
| Author | PM/PJM |
| Date | December 26, 2025 |
| Sprint | Sprint 57 |
| Depends On | Plan v2.2 (CTO Approved) |
| Gate | G2 (Design Ready) |

---

## 1. Overview

### 1.1 Purpose

This document defines the UI design specification for the SDLC Orchestrator Landing Page, following the approved Plan v2.2. It serves as the Stage 02 (Design) artifact required before Stage 03 (Build) implementation.

### 1.2 Scope

- Landing page at `sdlc.nhatquangholding.com`
- Target audience: Vietnamese SME founders, Engineering Managers, CTOs
- Primary goal: Convert visitors to Free/Founder plan signups
- Secondary goal: Enterprise lead generation

### 1.3 Design Principles

1. **Clarity over cleverness** - Clear messaging, no jargon
2. **Mobile-first** - 60%+ traffic expected from mobile
3. **Fast load** - Target Lighthouse >80
4. **Accessible** - WCAG 2.1 AA compliance
5. **Vietnamese-first** - Primary language, English secondary

---

## 2. Design System

### 2.1 Color Palette

```yaml
Primary Colors:
  primary-900: "#0f172a"    # Deep navy - Headlines
  primary-700: "#1e3a5f"    # Navy - Buttons, accents
  primary-500: "#3b82f6"    # Blue - Links, CTAs
  primary-100: "#dbeafe"    # Light blue - Backgrounds

Secondary Colors:
  accent-500: "#10b981"     # Emerald - Success, Founder badge
  accent-400: "#34d399"     # Light emerald - Hover states

Neutral Colors:
  gray-900: "#111827"       # Text primary
  gray-600: "#4b5563"       # Text secondary
  gray-400: "#9ca3af"       # Text muted
  gray-100: "#f3f4f6"       # Background secondary
  white: "#ffffff"          # Background primary

Semantic Colors:
  success: "#10b981"        # Green - Success states
  warning: "#f59e0b"        # Amber - Warning states
  error: "#ef4444"          # Red - Error states
  info: "#3b82f6"           # Blue - Info states
```

### 2.2 Typography

```yaml
Font Family:
  primary: "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
  mono: "JetBrains Mono, Consolas, monospace"

Font Sizes (rem):
  display: 3.75rem (60px)   # Hero headline
  h1: 2.25rem (36px)        # Section titles
  h2: 1.875rem (30px)       # Subsection titles
  h3: 1.5rem (24px)         # Card titles
  body-lg: 1.125rem (18px)  # Lead text
  body: 1rem (16px)         # Body text
  small: 0.875rem (14px)    # Captions, labels
  xs: 0.75rem (12px)        # Badges, tags

Font Weights:
  bold: 700                 # Headlines, CTAs
  semibold: 600             # Subheadings
  medium: 500               # Body emphasis
  regular: 400              # Body text

Line Heights:
  tight: 1.25               # Headlines
  normal: 1.5               # Body text
  relaxed: 1.75             # Long-form text
```

### 2.3 Spacing Scale

```yaml
Spacing (rem):
  0: 0
  1: 0.25rem (4px)
  2: 0.5rem (8px)
  3: 0.75rem (12px)
  4: 1rem (16px)
  5: 1.25rem (20px)
  6: 1.5rem (24px)
  8: 2rem (32px)
  10: 2.5rem (40px)
  12: 3rem (48px)
  16: 4rem (64px)
  20: 5rem (80px)
  24: 6rem (96px)

Section Padding:
  desktop: py-24 (96px top/bottom)
  tablet: py-16 (64px top/bottom)
  mobile: py-12 (48px top/bottom)

Container:
  max-width: 1280px
  padding-x: 1.5rem (24px)
```

### 2.4 Border Radius

```yaml
Radius:
  none: 0
  sm: 0.25rem (4px)         # Badges
  md: 0.5rem (8px)          # Buttons, inputs
  lg: 0.75rem (12px)        # Cards
  xl: 1rem (16px)           # Large cards
  full: 9999px              # Pills, avatars
```

### 2.5 Shadows

```yaml
Shadows:
  sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)"
  md: "0 4px 6px -1px rgb(0 0 0 / 0.1)"
  lg: "0 10px 15px -3px rgb(0 0 0 / 0.1)"
  xl: "0 20px 25px -5px rgb(0 0 0 / 0.1)"

Card Shadow:
  default: "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"
  hover: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
```

---

## 3. Component Specifications

### 3.1 Navigation Bar

```
┌────────────────────────────────────────────────────────────────────────┐
│ [Logo] SDLC Orchestrator          Features  Pricing  Docs    [Đăng ký]│
└────────────────────────────────────────────────────────────────────────┘

Mobile (hamburger):
┌────────────────────────────────────────────────────────────────────────┐
│ [Logo] SDLC Orchestrator                                          [☰] │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Height: 64px (desktop), 56px (mobile)
- Background: white with `shadow-sm` on scroll
- Position: sticky top
- Logo: 32px height
- Links: `text-gray-600 hover:text-primary-700`
- CTA button: `bg-primary-700 text-white rounded-md px-4 py-2`

### 3.2 Hero Section

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│            ┌──────────────────────────────────────────┐               │
│            │ 🚀 Operating System for Software 3.0     │               │
│            └──────────────────────────────────────────┘               │
│                                                                        │
│         Control Plane for AI-Powered Development                       │
│                                                                        │
│      Orchestrate any AI coder under enterprise governance.             │
│      Native codegen for teams without AI tools.                        │
│                                                                        │
│      ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│      │  Bắt đầu miễn   │  │    Xem Demo     │  │  Liên hệ tư vấn │    │
│      │      phí        │  │                 │  │                 │    │
│      └─────────────────┘  └─────────────────┘  └─────────────────┘    │
│                                                                        │
│      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│      │🛡️ OWASP L2   │  │🏢 VN SME     │  │⚡ 4-Gate     │             │
│      └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Background: Gradient `from-gray-50 to-white`
- Badge: `bg-primary-100 text-primary-700 rounded-full px-4 py-1`
- Headline: `text-display font-bold text-gray-900`
- Subheadline: `text-body-lg text-gray-600 max-w-2xl mx-auto`
- Primary CTA: `bg-primary-700 hover:bg-primary-800 text-white px-6 py-3 rounded-lg`
- Secondary CTA: `border border-gray-300 hover:border-gray-400 px-6 py-3 rounded-lg`
- Tertiary CTA: `text-primary-700 hover:text-primary-800 underline`
- Trust badges: `bg-white border border-gray-200 rounded-md px-3 py-1.5 text-sm`

### 3.3 Features Section (4 Modes)

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                    One platform. Four superpowers.                     │
│                                                                        │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │
│   │      🚪         │  │      📦         │  │      ⚡         │       │
│   │  Quality Gates  │  │  Evidence Vault │  │  EP-06 Codegen  │       │
│   │                 │  │                 │  │                 │       │
│   │ Policy-as-Code  │  │ Immutable audit │  │ Native AI code  │       │
│   │ gates at every  │  │ trail for every │  │ generation.     │       │
│   │ stage.          │  │ decision.       │  │ IR-based, 4-Gate│       │
│   │                 │  │                 │  │ validated.      │       │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘       │
│                                                                        │
│                       ┌─────────────────┐                              │
│                       │      🛡️         │                              │
│                       │  Policy Guards  │                              │
│                       │                 │                              │
│                       │ OPA-powered     │                              │
│                       │ governance.     │                              │
│                       │ Block, warn, or │                              │
│                       │ allow auto.     │                              │
│                       └─────────────────┘                              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Section background: `bg-white`
- Title: `text-h1 font-bold text-center`
- Grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6`
- Cards: `bg-gray-50 border border-gray-200 rounded-xl p-6`
- Icon: `text-4xl mb-4`
- Card title: `text-h3 font-semibold mb-2`
- Card description: `text-body text-gray-600`

### 3.4 How It Works (3 Steps)

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                          How It Works                                  │
│                                                                        │
│     ┌─────────────┐      ┌─────────────┐      ┌─────────────┐         │
│     │     ①      │ ───► │     ②      │ ───► │     ③      │         │
│     │  Connect    │      │  Configure  │      │    Ship     │         │
│     │             │      │             │      │             │         │
│     │ Link your   │      │ Choose      │      │ AI validates│         │
│     │ GitHub repo.│      │ policies    │      │ every PR.   │         │
│     │ 2 phút      │      │ and gates.  │      │ Full audit  │         │
│     │ setup.      │      │             │      │ trail.      │         │
│     └─────────────┘      └─────────────┘      └─────────────┘         │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Section background: `bg-gray-50`
- Steps container: `flex flex-col md:flex-row items-center justify-center gap-8`
- Step number: `w-12 h-12 rounded-full bg-primary-700 text-white flex items-center justify-center font-bold text-xl`
- Step title: `text-h3 font-semibold mt-4`
- Step description: `text-body text-gray-600 text-center max-w-xs`
- Connector: Hidden on mobile, `→` icon between steps on desktop

### 3.5 EP-06 Vietnamese Founders Section

```
┌────────────────────────────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░                                                                  ░  │
│  ░        🇻🇳 Dành cho Founders Việt Nam                            ░  │
│  ░                                                                  ░  │
│  ░     EP-06 IR-based Codegen - Từ ý tưởng đến sản phẩm đầu tiên   ░  │
│  ░                                                                  ░  │
│  ░  Bạn không cần Cursor hay Claude Code. EP-06 tích hợp sẵn       ░  │
│  ░  trong platform, giúp bạn build sản phẩm đầu tiên trong         ░  │
│  ░  30 phút* với full audit trail.                                 ░  │
│  ░                                                                  ░  │
│  ░  *Typical for simple CRUD apps. Time varies by project scope.   ░  │
│  ░                                                                  ░  │
│  ░  ✅ Vietnamese domain templates (E-commerce, HRM, CRM)           ░  │
│  ░  ✅ 4-Gate Quality Pipeline                                      ░  │
│  ░  ✅ Tuân thủ quy định VN (BHXH, VAT, Luật Lao động)              ░  │
│  ░  ✅ Hỗ trợ tiếng Việt                                            ░  │
│  ░                                                                  ░  │
│  ░                    ┌─────────────────────┐                       ░  │
│  ░                    │  Bắt đầu với EP-06  │                       ░  │
│  ░                    └─────────────────────┘                       ░  │
│  ░                                                                  ░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Section background: Gradient `from-primary-900 to-primary-800`
- Text color: `text-white`
- Flag emoji: 🇻🇳 with `text-3xl`
- Title: `text-h1 font-bold`
- Subtitle: `text-body-lg text-primary-100`
- Description: `text-body text-primary-100 max-w-2xl mx-auto`
- Checklist items: `flex items-center gap-2` with ✅ emoji
- CTA: `bg-accent-500 hover:bg-accent-400 text-white px-6 py-3 rounded-lg font-semibold`

### 3.6 Pricing Section

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                              PRICING                                   │
│                  Start free. Scale with confidence.                    │
│                                                                        │
│   ┌─────────────────┐  ┌─────────────────────┐  ┌─────────────────┐   │
│   │      FREE       │  │    FOUNDER ⭐       │  │    ENTERPRISE   │   │
│   │                 │  │   PHỔ BIẾN NHẤT     │  │                 │   │
│   │     0 VND       │  │  2.5M VND/tháng     │  │    Liên hệ      │   │
│   │                 │  │    (~$99/team)      │  │                 │   │
│   │  • 1 project    │  │  • Unlimited users  │  │  • Unlimited    │   │
│   │  • 5 gates      │  │  • EP-06 Codegen    │  │  • On-premise   │   │
│   │  • Community    │  │  • Evidence Vault   │  │  • Custom SLA   │   │
│   │                 │  │  • VN Support       │  │  • Dedicated    │   │
│   │                 │  │                     │  │                 │   │
│   │  [Thử ngay]     │  │  [Bắt đầu ngay]     │  │ [Liên hệ Sales] │   │
│   └─────────────────┘  └─────────────────────┘  └─────────────────┘   │
│                                                                        │
│   💡 Founder Plan: Dành cho startup VN xây dựng sản phẩm đầu tiên     │
│                                                                        │
│   🌐 For global teams: Standard Plan at $30/user/month                │
│                        [View Global Pricing]                           │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Section background: `bg-white`
- Grid: `grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto`
- Free card: `bg-white border border-gray-200 rounded-xl p-6`
- Founder card (highlighted):
  - `bg-white border-2 border-accent-500 rounded-xl p-6 relative`
  - Badge: `absolute -top-3 left-1/2 transform -translate-x-1/2 bg-accent-500 text-white px-3 py-1 rounded-full text-sm`
- Enterprise card: `bg-gray-50 border border-gray-200 rounded-xl p-6`
- Price: `text-h1 font-bold`
- Features list: `space-y-2 text-body text-gray-600`
- CTA buttons: Same as Hero section styling
- Footnotes: `text-sm text-gray-500 text-center mt-8`

### 3.7 Three CTAs Section

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│   ┌─────────────────────┐  ┌─────────────────────┐  ┌───────────────┐ │
│   │                     │  │                     │  │               │ │
│   │      👀             │  │      🚀             │  │     📞        │ │
│   │                     │  │                     │  │               │ │
│   │    Watch Demo       │  │    Start Free       │  │   Talk to Us  │ │
│   │                     │  │                     │  │               │ │
│   │  See how it works   │  │  1 project, 5 gates │  │  For SME and  │ │
│   │  in 3 minutes       │  │  No credit card     │  │  Enterprise   │ │
│   │                     │  │                     │  │               │ │
│   │ [View Sample Proj.] │  │ [Create Account]    │  │ [Schedule]    │ │
│   │                     │  │                     │  │               │ │
│   └─────────────────────┘  └─────────────────────┘  └───────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Section background: `bg-gray-50`
- Grid: `grid-cols-1 md:grid-cols-3 gap-6`
- Cards: `bg-white rounded-xl p-8 text-center shadow-md hover:shadow-lg transition-shadow`
- Icon: `text-4xl mb-4`
- Title: `text-h3 font-semibold mb-2`
- Description: `text-body text-gray-600 mb-6`
- Center card (Start Free) highlighted: `ring-2 ring-primary-500`

### 3.8 Footer

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│  SDLC Orchestrator                                                     │
│  Operating System for Software 3.0                                     │
│                                                                        │
│  Product          Resources         Company          Legal             │
│  ─────────        ─────────         ─────────        ─────────         │
│  Features         Documentation     About Us         Privacy           │
│  Pricing          Blog              Contact          Terms             │
│  Demo             Changelog         Careers          Cookies           │
│                                                                        │
│  ────────────────────────────────────────────────────────────────────  │
│                                                                        │
│  © 2025 NQH Technology. All rights reserved.                          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Background: `bg-gray-900`
- Text: `text-gray-300`
- Links: `text-gray-400 hover:text-white`
- Grid: `grid-cols-2 md:grid-cols-4 gap-8`
- Divider: `border-t border-gray-800`
- Copyright: `text-sm text-gray-500`

---

## 4. Responsive Breakpoints

### 4.1 Breakpoint Definitions

```yaml
Breakpoints:
  mobile: 0 - 639px        # sm
  tablet: 640px - 1023px   # md
  desktop: 1024px - 1279px # lg
  wide: 1280px+            # xl

Container Max-widths:
  sm: 640px
  md: 768px
  lg: 1024px
  xl: 1280px
```

### 4.2 Mobile-Specific Adjustments

```yaml
Navigation:
  - Hamburger menu
  - Full-screen mobile menu overlay
  - Logo + hamburger only in nav bar

Hero:
  - Stack CTAs vertically
  - Reduce headline to text-3xl
  - Single-column trust badges

Features:
  - Single column grid
  - Full-width cards

Pricing:
  - Single column
  - Founder plan first (priority)

Footer:
  - 2-column grid
  - Stacked sections
```

---

## 5. Page Structure

### 5.1 Section Order

```yaml
Landing Page (/):
  1. Navigation (sticky)
  2. Hero Section
  3. Features Section (4 modes)
  4. How It Works (3 steps)
  5. EP-06 Vietnamese Founders Section
  6. Pricing Section
  7. Three CTAs Section
  8. Footer

Demo Page (/demo):
  1. Navigation
  2. Hero (video embed)
  3. Screenshots gallery
  4. CTA to register
  5. Footer

Pricing Page (/pricing):
  1. Navigation
  2. Full pricing comparison table
  3. FAQ accordion
  4. Enterprise contact form
  5. Footer
```

### 5.2 SEO Structure

```yaml
Page Title: "SDLC Orchestrator - Operating System for Software 3.0"
Meta Description: "Control plane that governs all your AI coders. Native codegen for Vietnamese SME. Quality Gates, Evidence Vault, Policy Guards."

H1: "Control Plane for AI-Powered Development" (Hero)
H2:
  - "One platform. Four superpowers." (Features)
  - "How It Works" (Steps)
  - "Dành cho Founders Việt Nam" (EP-06)
  - "Pricing" (Pricing)
H3: Feature card titles, Step titles, CTA card titles
```

---

## 6. Interaction States

### 6.1 Button States

```yaml
Primary Button:
  default: bg-primary-700 text-white
  hover: bg-primary-800
  active: bg-primary-900
  disabled: bg-gray-300 text-gray-500 cursor-not-allowed
  focus: ring-2 ring-primary-500 ring-offset-2

Secondary Button:
  default: border border-gray-300 text-gray-700
  hover: border-gray-400 bg-gray-50
  active: bg-gray-100
  focus: ring-2 ring-gray-300 ring-offset-2

Accent Button (EP-06 CTA):
  default: bg-accent-500 text-white
  hover: bg-accent-400
  active: bg-accent-600
  focus: ring-2 ring-accent-400 ring-offset-2
```

### 6.2 Card Hover Effects

```yaml
Feature Cards:
  default: shadow-sm
  hover: shadow-md transform -translate-y-1 transition-all duration-200

Pricing Cards:
  default: shadow-md
  hover: shadow-lg

CTA Cards:
  default: shadow-md
  hover: shadow-lg ring-2 ring-primary-100
```

### 6.3 Link States

```yaml
Text Links:
  default: text-primary-700 underline-offset-2
  hover: text-primary-800 underline
  active: text-primary-900
  visited: text-primary-600
```

---

## 7. Accessibility Requirements

### 7.1 WCAG 2.1 AA Compliance

```yaml
Color Contrast:
  - Body text on white: minimum 4.5:1
  - Large text on white: minimum 3:1
  - Button text: minimum 4.5:1
  - All colors validated with contrast checker

Keyboard Navigation:
  - All interactive elements focusable
  - Visible focus indicators (ring-2)
  - Skip to main content link
  - Logical tab order

Screen Reader:
  - Semantic HTML (header, main, footer, nav, section)
  - Alt text for all images
  - ARIA labels for icon buttons
  - Heading hierarchy (h1 → h2 → h3)

Motion:
  - Respect prefers-reduced-motion
  - No auto-playing videos
  - Subtle animations only
```

### 7.2 Semantic HTML Structure

```html
<header>
  <nav aria-label="Main navigation">...</nav>
</header>

<main id="main-content">
  <section aria-labelledby="hero-title">
    <h1 id="hero-title">...</h1>
  </section>

  <section aria-labelledby="features-title">
    <h2 id="features-title">...</h2>
  </section>

  <!-- ... more sections -->
</main>

<footer aria-label="Site footer">...</footer>
```

---

## 8. Performance Budget

### 8.1 Lighthouse Targets

```yaml
Performance: >80
Accessibility: >95
Best Practices: >90
SEO: >95

Core Web Vitals:
  LCP (Largest Contentful Paint): <2.5s
  FID (First Input Delay): <100ms
  CLS (Cumulative Layout Shift): <0.1
```

### 8.2 Asset Optimization

```yaml
Images:
  - Format: WebP with JPEG fallback
  - Lazy loading: Below-fold images
  - Responsive: srcset for different sizes
  - Max size: 200KB per image

Fonts:
  - Inter: subset Vietnamese + Latin
  - Load: font-display: swap
  - Preload: critical weights only (400, 600, 700)

JavaScript:
  - Bundle: <100KB gzipped
  - Code splitting: Per-route
  - Tree shaking: Remove unused code

CSS:
  - Tailwind: Purge unused classes
  - Critical CSS: Inline above-fold styles
  - Bundle: <50KB gzipped
```

---

## 9. Wireframes (ASCII)

### 9.1 Full Page Desktop View

```
┌────────────────────────────────────────────────────────────────────────┐
│                           NAVIGATION                                   │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                              HERO                                      │
│                   Badge + Headline + CTAs + Trust                      │
│                         (height: ~600px)                               │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                            FEATURES                                    │
│                    4 cards in horizontal grid                          │
│                         (height: ~500px)                               │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                          HOW IT WORKS                                  │
│                      3 steps with arrows                               │
│                         (height: ~400px)                               │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░                                                                  ░  │
│  ░                    EP-06 VIETNAMESE FOUNDERS                     ░  │
│  ░                     Dark background section                      ░  │
│  ░                         (height: ~450px)                         ░  │
│  ░                                                                  ░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                            PRICING                                     │
│                      3 pricing cards                                   │
│                         (height: ~600px)                               │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                           THREE CTAs                                   │
│                     Demo / Free / Talk cards                           │
│                         (height: ~350px)                               │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                            FOOTER                                      │
│                      4-column link grid                                │
│                         (height: ~250px)                               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Mobile View

```
┌─────────────────────┐
│ [Logo]          [☰] │  <- Sticky nav
├─────────────────────┤
│                     │
│    [Badge]          │
│                     │
│   Headline text     │
│   spans multiple    │
│   lines             │
│                     │
│   Subheadline       │
│                     │
│  [Primary CTA]      │
│  [Secondary CTA]    │
│  [Tertiary link]    │
│                     │
│   Trust badges      │
│   (horizontal       │
│    scroll)          │
│                     │
├─────────────────────┤
│                     │
│   FEATURES          │
│                     │
│  ┌───────────────┐  │
│  │ Feature 1     │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ Feature 2     │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ Feature 3     │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ Feature 4     │  │
│  └───────────────┘  │
│                     │
├─────────────────────┤
│                     │
│   HOW IT WORKS      │
│                     │
│      ┌─────┐        │
│      │  1  │        │
│      └─────┘        │
│      Connect        │
│        ↓            │
│      ┌─────┐        │
│      │  2  │        │
│      └─────┘        │
│      Configure      │
│        ↓            │
│      ┌─────┐        │
│      │  3  │        │
│      └─────┘        │
│      Ship           │
│                     │
├─────────────────────┤
│░░░░░░░░░░░░░░░░░░░░░│
│░                   ░│
│░  🇻🇳 VN Founders  ░│
│░                   ░│
│░  EP-06 section    ░│
│░  with checklist   ░│
│░                   ░│
│░  [CTA Button]     ░│
│░                   ░│
│░░░░░░░░░░░░░░░░░░░░░│
├─────────────────────┤
│                     │
│   PRICING           │
│                     │
│  ┌───────────────┐  │
│  │ FOUNDER ⭐    │  │  <- First (priority)
│  │ 2.5M VND      │  │
│  │ [CTA]         │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ FREE          │  │
│  │ 0 VND         │  │
│  │ [CTA]         │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ ENTERPRISE    │  │
│  │ Liên hệ       │  │
│  │ [CTA]         │  │
│  └───────────────┘  │
│                     │
├─────────────────────┤
│                     │
│   THREE CTAs        │
│   (stacked cards)   │
│                     │
├─────────────────────┤
│                     │
│   FOOTER            │
│   (2-col grid)      │
│                     │
│   © 2025 NQH        │
│                     │
└─────────────────────┘
```

---

## 10. Component Library

### 10.1 shadcn/ui Components to Use

```yaml
Core Components:
  - Button (primary, secondary, ghost, link variants)
  - Card (CardHeader, CardContent, CardFooter)
  - Badge (default, secondary, outline variants)
  - Separator
  - Sheet (mobile navigation)

Form Components (for future register/login):
  - Input
  - Label
  - Form (with react-hook-form)

Feedback Components:
  - Toast (notifications)
  - Alert (inline messages)

Layout Components:
  - Container (custom, max-w-7xl)
  - Section (custom, with consistent padding)
```

### 10.2 Custom Components to Create

```yaml
Landing-Specific:
  - Hero.tsx
  - FeatureCard.tsx
  - HowItWorksStep.tsx
  - EP06Section.tsx
  - PricingCard.tsx
  - CTACard.tsx
  - Footer.tsx
  - MobileNav.tsx

Shared:
  - Container.tsx (max-width wrapper)
  - Section.tsx (consistent section padding)
  - TrustBadge.tsx
  - IconCircle.tsx (step numbers)
```

---

## 11. Approval Checklist

### 11.1 Design Review Criteria

| Criterion | Status | Reviewer |
|-----------|--------|----------|
| Color contrast WCAG AA | ✅ Spec defines contrast requirements | CTO |
| Typography hierarchy | ✅ Inter + JetBrains Mono defined | CTO |
| Responsive breakpoints | ✅ Mobile-first breakpoints in Section 4 | CTO |
| Component specifications | ✅ All components spec'd in Section 3 | CTO |
| Accessibility requirements | ✅ WCAG 2.1 AA requirements in Section 7 | CTO |
| Performance budget | ✅ Lighthouse >80 target in Section 8 | CTO |
| Vietnamese content | ✅ VN-first messaging approved | CTO |
| Brand consistency | ✅ Tokens locked, no external copying | CTO |

### 11.2 Gate G2 (Design Ready) Requirements

```yaml
Required Artifacts:
  ✅ Design Specification Document (this document)
  ✅ Color palette approved (Section 2.1)
  ✅ Typography approved (Section 2.2)
  ✅ Wireframes reviewed (Section 9)
  ✅ Component specs validated (Section 3, 10)
  ✅ Accessibility check passed (Section 7)
  ✅ Performance budget confirmed (Section 8)

Approvers:
  - [x] CTO - Conditional PASS Dec 26, 2025
  - [ ] Design Lead (optional - N/A)
  - [ ] Frontend Lead (validate during implementation)
```

---

## 12. G2 Review Checklist (CTO/Design Lead Sign-off)

### 12.1 Scope & Messaging

| Criterion | Status | Notes |
|-----------|--------|-------|
| Hero uses locked copy: "Operating System for Software 3.0" | ✅ | Per Plan v2.2 Section 1.1 |
| "Control plane that governs all your AI coders" subheadline | ✅ | Per Plan v2.2 |
| 3-layer positioning visible (at least 1 section) | ✅ | Features section shows layers |
| EP-06 "Founders Việt Nam" CTA → `/register?plan=founder` | ✅ | Per Plan v2.2 Section 1.3 |

### 12.2 IA & Navigation

| Criterion | Status | Notes |
|-----------|--------|-------|
| Routes V1: `/`, `/pricing`, `/demo`, `/docs/getting-started`, `/login`, `/register` | ✅ | Per Plan v2.2 Section 4.1 |
| Standard plan displays as manual (no checkout link) | ✅ | Links to /support or Calendly |
| No "Vibecode" or external UI copying | ✅ | Original design only |

### 12.3 Visual System (Design Tokens)

| Criterion | Status | Notes |
|-----------|--------|-------|
| Color palette locked (no new colors) | ✅ | Section 2.1 defines all colors |
| Typography consistent (Inter + JetBrains Mono) | ✅ | Section 2.2 |
| Spacing scale follows 4px grid | ✅ | Section 2.3 |
| shadcn/ui component mapping complete | ✅ | Section 10.1 |

### 12.4 Responsive & Layout

| Criterion | Status | Notes |
|-----------|--------|-------|
| Mobile-first breakpoints defined | ✅ | Section 4 |
| Hero CTAs stack vertically on mobile | ✅ | Section 4.2 |
| Pricing: Founder card prominent but not oversized | ✅ | Section 3.6 |
| Mobile pricing: Founder first, then Free, then Enterprise | ✅ | Section 9.2 |

### 12.5 Accessibility (WCAG 2.1 AA)

| Criterion | Status | Notes |
|-----------|--------|-------|
| Text contrast ≥4.5:1 (body), ≥3:1 (large) | ✅ | Section 7.1 - validate in impl |
| Focus states visible (ring-2) | ✅ | Section 6.1 |
| Keyboard navigation for all interactive elements | ✅ | Section 7.1 |
| Skip-to-content link | ✅ | Section 7.1 |
| Semantic HTML structure | ✅ | Section 7.2 |

### 12.6 Performance Budget

| Criterion | Status | Notes |
|-----------|--------|-------|
| Lighthouse Performance >80 | ✅ | Section 8.1 - validate post-build |
| Lighthouse SEO >95 | ✅ | Section 8.1 - validate post-build |
| LCP <2.5s | ✅ | Section 8.1 - validate post-build |
| OG image ≤200KB | ✅ | Section 8.2 |
| Fonts self-hosted (next/font) | ✅ | Section 8.2 |
| JS bundle <100KB gzipped | ✅ | Section 8.2 - validate post-build |

### 12.7 Analytics (Mixpanel)

| Criterion | Status | Notes |
|-----------|--------|-------|
| `landing_page_view` event defined | ✅ | Per Plan v2.2 Section 8.2 |
| `hero_cta_click` with cta_type property | ✅ | demo/free/talk |
| `pricing_plan_click` with plan property | ✅ | free/founder/enterprise |
| `demo_video_play` event | ✅ | For /demo page |
| UTM properties captured | ✅ | source, utm_campaign |

### 12.8 Open Questions / Decisions

| Question | Owner | Deadline | Status |
|----------|-------|----------|--------|
| None - all decisions resolved in Plan v2.2 | - | - | ✅ Resolved |

---

## 13. G2 Gate Acceptance

### Pass/Fail Criteria

| Criterion | Required | Status |
|-----------|----------|--------|
| All Section 12.1-12.7 items checked | MUST | ✅ |
| No open questions blocking implementation | MUST | ✅ |
| CTO sign-off | MUST | ✅ CONDITIONAL PASS |
| Frontend Lead sign-off | MUST | ⏳ Validate during impl |

### Reviewer Sign-offs

| Reviewer | Role | Signature | Date |
|----------|------|-----------|------|
| CTO | CTO | ✅ CONDITIONAL PASS | Dec 26, 2025 |
| | Frontend Lead | (validate during impl) | |
| | Design Lead (optional) | N/A | |

### CTO G2 Review Summary

**Decision: CONDITIONAL PASS (Design Ready)**

Approved to start Sprint 57 implementation.

**Must-fix before "done-done" (not blocking Sprint 57 start):**
1. Wire `primary-*` / `accent-*` tokens to real Tailwind/shadcn theme during implementation
2. Validate Lighthouse/performance metrics post-build

**Non-blocking notes:**
- Good "30 phút*" disclaimer in EP-06 section
- No external UI copying - original design only

---

## 14. Next Steps

1. ~~**Submit for G2 Review** - This document to CTO/Frontend Lead~~ ✅ Done
2. ~~**Feedback Incorporation** - Update based on review comments~~ ✅ Done
3. ~~**G2 Approval** - Get sign-off (Section 13)~~ ✅ CONDITIONAL PASS
4. **Sprint 57 Start** - Begin implementation (UNBLOCKED)

---

## 15. Document Control

| Field | Value |
|-------|-------|
| Version | 1.1.0 |
| Status | SUBMITTED - Pending G2 Approval |
| Author | PM/PJM |
| Created | December 26, 2025 |
| Last Updated | December 26, 2025 |
| Depends On | Plan v2.2 (CTO Approved) |
| Gate | G2 (Design Ready) |

### Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Dec 26, 2025 | Initial design specification |
| 1.1.0 | Dec 26, 2025 | Added G2 Review Checklist, clarified EP-06 "30 phút" claim with disclaimer |
