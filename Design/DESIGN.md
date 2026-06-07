---
name: Financial Intelligence System
colors:
  surface: '#0f131f'
  surface-dim: '#0f131f'
  surface-bright: '#353946'
  surface-container-lowest: '#0a0e1a'
  surface-container-low: '#171b28'
  surface-container: '#1b1f2c'
  surface-container-high: '#262a37'
  surface-container-highest: '#313442'
  on-surface: '#dfe2f3'
  on-surface-variant: '#bbcac6'
  inverse-surface: '#dfe2f3'
  inverse-on-surface: '#2c303d'
  outline: '#859490'
  outline-variant: '#3c4947'
  surface-tint: '#4fdbc8'
  primary: '#4fdbc8'
  on-primary: '#003731'
  primary-container: '#14b8a6'
  on-primary-container: '#00423b'
  inverse-primary: '#006b5f'
  secondary: '#bcc7de'
  on-secondary: '#263143'
  secondary-container: '#3e495d'
  on-secondary-container: '#aeb9d0'
  tertiary: '#c0c6db'
  on-tertiary: '#293040'
  tertiary-container: '#9da4b8'
  on-tertiary-container: '#333a4b'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#71f8e4'
  primary-fixed-dim: '#4fdbc8'
  on-primary-fixed: '#00201c'
  on-primary-fixed-variant: '#005048'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#dce2f7'
  tertiary-fixed-dim: '#c0c6db'
  on-tertiary-fixed: '#141b2b'
  on-tertiary-fixed-variant: '#404758'
  background: '#0f131f'
  on-background: '#dfe2f3'
  surface-variant: '#313442'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1280px
  gutter: 24px
  margin-desktop: 40px
  margin-mobile: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system is engineered for a premium financial AI environment where precision meets modern technology. The brand personality is **authoritative, analytical, and frictionless**, designed to instill immediate trust in investors and financial professionals.

The visual style utilizes **Glassmorphism** and **Modern Minimalism**. By combining deep, dark surfaces with translucent layers and sharp teal accents, the interface feels like a sophisticated digital cockpit. High-quality whitespace and restrained use of vibrant gradients ensure that the "facts-focused" narrative remains the priority, while the glass effects provide a sense of depth and data-rich sophistication.

## Colors
The palette is rooted in a "Deep Space" dark mode to reduce cognitive load and emphasize the AI's "glow."

- **Primary (Teal #14B8A6):** Used exclusively for action states, success indicators, and data highlights.
- **Surface Tiers:** 
  - **Level 0 (#0a0e1a):** The canvas.
  - **Level 1 (#111827):** Primary containers and sidebar backgrounds.
  - **Level 2 (#1e293b):** Card surfaces and input backgrounds.
- **Typography:** Soft whites (#e8eaf0) are used for readability, while muted grays (#94a3b8) handle metadata and secondary descriptions.

## Typography
Inter is utilized for its exceptional legibility in data-dense environments. 

- **Hierarchy:** Use **Display-lg** for major total-value summaries. **Headlines** are semi-bold to establish clear structure in FAQ sections.
- **Readability:** Body text uses a generous 1.5x line height to ensure complex financial terms are easy to scan.
- **Labels:** Use uppercase for **Label-sm** when denoting categories or table headers to create a distinct visual contrast from standard body text.

## Layout & Spacing
The layout follows a **12-column fluid grid** for desktop, collapsing to a single column for mobile. 

- **Rhythm:** A 4px baseline grid ensures alignment. Use `stack-lg` (32px) to separate distinct AI response blocks.
- **Margins:** Desktop views should maintain a generous 40px outer margin to preserve the premium, airy feel.
- **Reflow:** On mobile, card padding should reduce from 24px to 16px to maximize screen real estate for textual information.

## Elevation & Depth
Depth is created through **translucency (Glassmorphism)** rather than traditional heavy shadows.

- **The Glass Layer:** Use a background blur of 12px–20px on level-2 components. Apply a subtle 1px border with a 10% white opacity to simulate a light-catching edge.
- **Subtle Gradients:** Apply a faint radial gradient (White at 5% opacity to transparent) from the top-left corner of cards to give a sense of light source.
- **Z-Index:** AI chat bubbles and tooltips sit on the highest elevation, using a subtle #000000 shadow at 25% opacity with a 20px blur to separate them from the underlying data grid.

## Shapes
This design system uses a **Rounded (0.5rem base)** approach to balance the technical nature of finance with the approachability of an AI assistant.

- **Standard Elements:** Buttons and input fields use 8px (0.5rem) corner radii.
- **Large Containers:** Main FAQ cards or dashboard panels use `rounded-lg` (16px) to feel distinct from smaller UI controls.
- **Data Points:** Small tags or status indicators can use `rounded-xl` for a pill-style appearance.

## Components
- **Buttons:** 
  - *Primary:* Solid Teal (#14b8a6) with white text. 
  - *Secondary:* Ghost style with a 1px teal border.
- **Chat Bubbles:** The AI response bubble should use the Level 2 background (#1e293b) with a Glassmorphism blur, while user prompts remain Level 1 (#111827) to create a visual dialogue hierarchy.
- **Input Fields:** Search and question bars should be dark (#1e293b) with a 1px border that glows Teal when focused. 
- **Cards:** Financial cards (e.g., Fund Performance) feature a subtle white-to-teal gradient "shimmer" on hover to indicate interactivity.
- **Chips/Badges:** Used for fund categories (e.g., "Equity", "Debt"). Use a low-opacity teal background (10%) with solid teal text.
- **Progress Indicators:** Use thin, 4px-high bars with a teal gradient to show data loading or portfolio allocations.