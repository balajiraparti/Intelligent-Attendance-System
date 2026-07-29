# Design System — Smart Attendance System

> **Single source of truth** for every visual decision in the project.
> Any developer or AI assistant making UI changes should consult this document first.
> All values are sourced from `src/ui/base_layout.py`.

---

## 1. Design Philosophy & Principles

The Smart Attendance System UI is built around a **clean, accessible, information-dense** aesthetic that communicates academic clarity and institutional trust. The system serves students, faculty, and administrators — so legibility and hierarchy are paramount.

### Core Principles

| Principle | What it means in practice |
|-----------|--------------------------|
| **Clarity first** | Every element has a purpose. No decorative noise — padding, colour, and size all carry meaning. |
| **Consistent elevation** | Shadows define depth, not decoration. Higher visual importance = more elevation. |
| **Semantic colour** | Colour communicates state (success, warning, danger, info) — never used purely for aesthetics. |
| **Fluid typography** | Headings use `clamp()` to stay legible at every viewport width without breakpoint hacks. |
| **Restrained motion** | Animations are subtle (0.3s), one-directional (`fadeUp`), and reinforce spatial hierarchy. |
| **Accessible contrast** | All foreground/background pairings meet or exceed WCAG AA contrast ratios. |

### Visual Language at a Glance

- **Backgrounds**: Near-white (`#F8FAFC`) page canvas with pure-white (`#FFFFFF`) cards that lift off it.
- **Borders**: Soft `#E5E7EB` lines — present but never dominant.
- **Accents**: Primary blue (`#2563EB`) anchors interactive elements; semantic colours handle status.
- **Radii**: Generous rounding (10–20px on cards) signals friendliness; pills (`9999px`) on badges and tabs.
- **Density**: Comfortable spacing (`--sp-4` to `--sp-6`) by default; tight spacing only inside compact components.

---

## 2. Color Palette

All colours are defined as CSS custom properties on `:root`. Always use the variable, never the raw hex, in stylesheets.

### 2.1 Brand Colors

| Token | Hex | Tailwind Reference | Usage |
|-------|-----|--------------------|-------|
| `--primary` | `#2563EB` | Blue 600 | Buttons, links, active states, icon fills, borders on focus |
| `--primary-dark` | `#1D4ED8` | Blue 700 | Hover state for primary buttons and links |
| `--primary-light` | `#DBEAFE` | Blue 100 | Badge backgrounds, pill backgrounds, code pill fill |
| `--primary-muted` | `#EFF6FF` | Blue 50 | Card background tints, icon container backgrounds |

### 2.2 Semantic Colors

#### Success — Emerald

| Token | Hex | Tailwind Reference | Usage |
|-------|-----|--------------------|-------|
| `--success` | `#10B981` | Emerald 500 | Positive KPI delta, attendance above threshold, confirmed actions |
| `--success-light` | `#D1FAE5` | Emerald 100 | Success badge/chip background |
| `--success-muted` | `#ECFDF5` | Emerald 50 | Success card tint, subtle row highlight |

#### Warning — Amber

| Token | Hex | Tailwind Reference | Usage |
|-------|-----|--------------------|-------|
| `--warning` | `#F59E0B` | Amber 500 | At-risk attendance, pending states, caution indicators |
| `--warning-light` | `#FEF3C7` | Amber 100 | Warning badge/chip background |
| `--warning-muted` | `#FFFBEB` | Amber 50 | Warning card tint |

#### Danger — Red

| Token | Hex | Tailwind Reference | Usage |
|-------|-----|--------------------|-------|
| `--danger` | `#EF4444` | Red 500 | Critical attendance shortage, destructive actions, error states |
| `--danger-light` | `#FEE2E2` | Red 100 | Danger badge/chip background |
| `--danger-muted` | `#FFF5F5` | Red 50 | Danger card tint |

#### Purple — KPI Accent

| Token | Hex | Tailwind Reference | Usage |
|-------|-----|--------------------|-------|
| `--purple` | `#8B5CF6` | Violet 500 | Secondary KPI cards, subject accent (index 1) |
| `--purple-light` | `#EDE9FE` | Violet 100 | Purple badge/chip background |
| `--purple-muted` | `#F5F3FF` | Violet 50 | Purple card tint |

#### Teal — KPI Accent

| Token | Hex | Tailwind Reference | Usage |
|-------|-----|--------------------|-------|
| `--teal` | `#14B8A6` | Teal 400 | Tertiary KPI cards, subject accent (index 2) |
| `--teal-light` | `#CCFBF1` | Teal 100 | Teal badge/chip background |
| `--teal-muted` | `#F0FDFA` | Teal 50 | Teal card tint |

### 2.3 Neutral Scale

| Token | Hex | Tailwind Reference | Usage |
|-------|-----|--------------------|-------|
| `--bg` | `#F8FAFC` | Slate 50 | Page/app background — the canvas everything sits on |
| `--surface` | `#FFFFFF` | White | Cards, inputs, navigation, modals — the "lifted" layer |
| `--surface-alt` | `#F9FAFB` | Gray 50 | Zebra-stripe rows, chip backgrounds, tab bar fill |
| `--border` | `#E5E7EB` | Gray 200 | Standard borders on cards, inputs, dividers |
| `--border-light` | `#F3F4F6` | Gray 100 | Subtle internal dividers, nested separators |
| `--text` | `#111827` | Gray 900 | Primary body text, headings |
| `--text-secondary` | `#374151` | Gray 700 | Supporting body text, secondary labels |
| `--text-muted` | `#6B7280` | Gray 500 | Metadata, captions, placeholder text |
| `--text-subtle` | `#9CA3AF` | Gray 400 | Hint text, disabled states, neutral KPI delta |

### 2.4 Subject Card Accent Cycle

Subject cards cycle through six accent colours based on their list index (index mod 6). Each accent has a matching background tint derived from its `--*-muted` token.

| Index | Name | Accent Hex | Background Hex | CSS Variable Pair |
|-------|------|-----------|----------------|-------------------|
| 0 | Blue | `#2563EB` | `#EFF6FF` | `--primary` / `--primary-muted` |
| 1 | Purple | `#8B5CF6` | `#F5F3FF` | `--purple` / `--purple-muted` |
| 2 | Teal | `#14B8A6` | `#F0FDFA` | `--teal` / `--teal-muted` |
| 3 | Amber | `#F59E0B` | `#FFFBEB` | `--warning` / `--warning-muted` |
| 4 | Green | `#10B981` | `#ECFDF5` | `--success` / `--success-muted` |
| 5 | Red | `#EF4444` | `#FFF5F5` | `--danger` / `--danger-muted` |

The accent colour is applied as a `4px solid` left border on `.sub-card`. The background tint is used for the icon container inside the card.

### 2.5 Color Usage Rules

- **Never** use a semantic colour (success/warning/danger) for a non-semantic purpose — e.g. do not use `--success` as a decorative green highlight for something that has no status meaning.
- **Never** hardcode hex values in component styles. Always reference a CSS variable.
- **Light variants** are for backgrounds only. Use the base token (e.g. `--success`) for text or icon colour on white.
- **Muted variants** are one step lighter than light variants — use only for the subtlest card tints or hover fills.
- On `--primary-muted` or coloured backgrounds, use the base colour token for text to maintain contrast.
- The `--bg` ↔ `--surface` contrast is intentionally subtle. Do not try to increase it — the separation should be sensed, not seen.

---

## 3. Typography

### 3.1 Font Families

Two Google Fonts are loaded via a single `@import` at the top of the stylesheet.

```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
```

| Role | Family | Weights Loaded | Applied To |
|------|--------|---------------|-----------|
| **Heading** | Poppins | 400, 500, 600, 700, 800 | `.page-title`, `.section-title`, `.hero-title`, `.dash-name`, `.auth-title`, `.sub-card-name`, `.feature-card__title`, `.portal-card__title`, `.kpi-value`, `.metric-card__value`, `h1`, `h2`, `h3` |
| **Body** | Inter | 400, 500, 600, 700 | All other text — paragraphs, buttons, inputs, labels, table cells, captions |
| **Monospace** | `ui-monospace`, JetBrains Mono (fallback) | system | `.code-pill` (subject codes only) |

> **Rule**: If it conveys a number, title, or named entity (subject name, user name, metric value) → Poppins. If it describes, labels, or instructs → Inter.

### 3.2 Type Scale

| Role | Size | Weight | Family | Color Token | Notes |
|------|------|--------|--------|-------------|-------|
| Page eyebrow | `0.72rem` | 700 | Inter | `--primary` | All-caps, `letter-spacing: 0.10em` |
| Hero title | `clamp(2.5rem, 5vw, 4.4rem)` | 800 | Poppins | `--text` | Landing / marketing sections |
| Auth title | `clamp(1.75rem, 3.5vw, 2.6rem)` | 800 | Poppins | `--text` | Login / register page heading |
| Dashboard name | `clamp(1.5rem, 2.5vw, 2.1rem)` | 700 | Poppins | `--text` | Personalised greeting |
| Page title | `clamp(1.5rem, 2.5vw, 1.9rem)` | 700 | Poppins | `--text` | In-app page headings |
| KPI value | `1.85rem` | 700 | Poppins | `--text` | Metric card primary number |
| Section heading | `1.15rem` | 600 | Poppins | `--text` | Card or section subheadings |
| Sub-card name | `1.05rem` | 600 | Poppins | `--text` | Subject card title |
| Button | `0.9rem` | 600 | Inter | (varies by type) | All button labels |
| Body | `0.9–0.92rem` | 400 | Inter | `--text` | Standard paragraph text |
| Body muted | `0.875rem` | 400 | Inter | `--text-muted` | Supporting descriptions, timestamps |
| KPI sub-label | `0.74rem` | 600 | Inter | semantic | `.positive` → success · `.negative` → danger · `.neutral` → text-subtle |
| Small label | `0.8–0.83rem` | 500 | Inter | `--text-muted` | Form field labels, metadata chips |
| Hint text | `0.8rem` | 400 | Inter | `--text-subtle` | Helper text beneath inputs, empty-state captions, center-aligned |

### 3.3 Usage Guidelines

- **Do not** invent intermediate sizes. Pick the nearest scale step.
- `clamp()` values must not be modified per-component — they are global page-level sizes defined once.
- Poppins at weight 800 is reserved for the largest display text (hero, auth). Use 700 for page titles and KPI values.
- Inter 700 is acceptable for button labels and emphasis in body copy. Do not use Poppins for body text.
- All-caps text (`text-transform: uppercase`) must also apply `letter-spacing: 0.08em` minimum for legibility.
- Line-height defaults: headings `1.2–1.3`, body `1.5–1.6`.

---

## 4. Spacing System

All spacing is built on a `0.25rem` (4px) base unit. Use the CSS variables exclusively — do not write arbitrary `px` values.

| Token | Value | Pixels | Intended Use |
|-------|-------|--------|-------------|
| `--sp-1` | `0.25rem` | 4px | Micro gap — icon-to-label, badge internal padding |
| `--sp-2` | `0.5rem` | 8px | Tight — inline elements, compact chip padding |
| `--sp-3` | `0.75rem` | 12px | Compact — small card internal padding, list item gaps |
| `--sp-4` | `1rem` | 16px | **Default** — standard component padding, form field spacing |
| `--sp-5` | `1.25rem` | 20px | Comfortable — card body padding |
| `--sp-6` | `1.5rem` | 24px | Section padding — card top/bottom, header padding |
| `--sp-8` | `2rem` | 32px | Section gap — vertical rhythm between major page sections |
| `--sp-10` | `2.5rem` | 40px | Large spacing — hero padding, auth card top margin |
| `--sp-12` | `3rem` | 48px | Extra-large — hero vertical padding, full-page sections |

### Spacing Rules

- **Card padding**: `--sp-5` to `--sp-6` on the card body; `--sp-3` to `--sp-4` on compact inner sections.
- **Between sibling cards/sections**: use `.section-gap` (`2rem`) or the `--sp-8` token.
- **Between form fields**: `--sp-4`.
- **Icon-to-text gaps**: `--sp-2` (8px) is the standard.
- **Do not** use values outside the scale (e.g. `14px`, `18px`, `22px`). Round to the nearest token.

---

## 5. Border Radius

| Token | Value | Intended Use |
|-------|-------|-------------|
| `--r-sm` | `6px` | Small elements — icon containers, KPI icon boxes, small chips |
| `--r-md` | `10px` | Default component radius — inputs, secondary cards, tooltips |
| `--r-lg` | `14px` | Primary cards — KPI cards, subject cards, feature cards |
| `--r-xl` | `20px` | Prominent containers — dashboard header, portal cards |
| `--r-2xl` | `24px` | Large containers — auth card |
| `--r-full` | `9999px` | Pills and circles — tab bar, badges, role chips, code pills, avatar circles |

### Radius Rules

- The radius of a container and its child elements should form a **concentric hierarchy** — inner elements get a smaller radius than their parent.
- At mobile breakpoints (≤768px), radii **step down one level** (e.g. `--r-xl` → `--r-lg`, `--r-lg` → `--r-md`) to avoid over-rounded edges on small screens.
- Interactive elements (buttons, tab items) always use `--r-full` or `--r-md` — never sharp corners.
- `--r-full` is for badges, pills, and tab containers only. Do not use it on large cards.

---

## 6. Shadows & Elevation

Shadows communicate the **elevation layer** of a component. Higher elevation = more visual importance = more prominent shadow. Match shadow to component role, not to personal preference.

| Token | Value | Elevation Level | Use Case |
|-------|-------|-----------------|----------|
| `--shadow-xs` | `0 1px 2px rgba(0,0,0,0.05)` | 1 — resting | KPI cards, subject cards at rest, subtle inputs |
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.10), 0 1px 2px rgba(0,0,0,0.06)` | 2 — low | Active tab items, dropdowns, popovers |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)` | 3 — medium | Navigation bar, floating action areas |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.10), 0 4px 6px rgba(0,0,0,0.05)` | 4 — high | Modals, dialogs, sheet panels |
| `--shadow-hover` | `0 20px 25px rgba(0,0,0,0.10), 0 10px 10px rgba(0,0,0,0.04)` | 5 — lifted | Hover state for interactive cards |

### Elevation Rules

- Cards rest at `--shadow-xs`. On hover/focus, they lift to `--shadow-hover` with a `translateY(-2px)` transform. The transition is `0.25s ease`.
- Navigation and persistent UI elements use `--shadow-md` to stay above the page canvas without competing with modal-level elevation.
- **Never** apply `--shadow-lg` or `--shadow-hover` to resting (non-interactive) elements.
- Do not use `box-shadow` values that aren't from this token set.

---

## 7. Component Reference

### 7.1 Dashboard Header

**Class:** `.dash-header`

A full-width greeting card that anchors the dashboard. It introduces the logged-in user and orients them with a role badge.

| Property | Value |
|----------|-------|
| Background | Linear gradient: `--primary-muted` → `#F0F9FF` → `--bg` |
| Border radius | `--r-xl` (20px) |
| Padding | `--sp-6` |
| Border | `1px solid --border-light` |
| Animation | `fadeUp` 0.3s ease |

**Child elements:**

| Class | Description |
|-------|-------------|
| `.dash-name` | Personalised greeting — Poppins 700, `clamp(1.5rem, 2.5vw, 2.1rem)`, `--text` |
| `.dash-role-badge` | Inline-flex pill, `--primary-light` bg, `--primary` text, `--r-full`, `0.8rem 600` |
| `.dash-meta` | Supporting metadata (date, department, etc.) — `0.875rem`, `--text-muted` |

---

### 7.2 KPI Cards

**Class:** `.kpi-card`

Metric summary cards arranged in a grid. Each card surfaces a single key number with context.

| Property | Value |
|----------|-------|
| Background | `--surface` (white) |
| Border radius | `--r-lg` (14px) |
| Shadow | `--shadow-xs` → `--shadow-hover` on hover |
| Top accent stripe | `3px solid var(--kpi-accent)` — set per-card via inline custom property |
| Padding | `--sp-5` |
| Hover transform | `translateY(-2px)` |
| Animation | `fadeUp` with staggered `animation-delay` (0.04s increments) |

**Child elements:**

| Class | Description |
|-------|-------------|
| `.kpi-icon` | `2.25rem` square icon container, `--r-sm`, coloured background from `--kpi-accent` muted variant |
| `.kpi-value` | Primary metric number — Poppins 700, `1.85rem`, `--text` |
| `.kpi-label` | Metric name — `0.8rem`, `--text-muted` |
| `.kpi-sub` | Delta or context — `0.74rem 600`; add `.positive` (success), `.negative` (danger), or `.neutral` (text-subtle) |

**KPI accent colours** match the same cycle as subject cards (blue → purple → teal → amber → green → red).

---

### 7.3 Tab Bar

**Class:** `.tab-bar`

Segmented control used for switching between views (e.g. attendance by subject vs. by date).

| Property | Value |
|----------|-------|
| Container background | `--surface-alt` |
| Container border | `1px solid --border` |
| Container radius | `--r-full` (pill container) |
| Item font | `0.875rem 500`, `--text-muted` |
| Active item bg | `--surface` (white) |
| Active item text | `--primary` |
| Active item shadow | `--shadow-sm` |
| Active item radius | `--r-full` |

**Usage:** Wrap all tabs in `.tab-bar`; add `.active` to the currently selected `.tab-item`. Do not mix `.tab-bar` with standard link underlines — it is a pill-style control only.

---

### 7.4 Subject Cards

**Class:** `.sub-card`

One card per enrolled subject, displayed in a list or grid. Accent colour cycles by list index.

| Property | Value |
|----------|-------|
| Background | `--surface` (white) |
| Left border | `4px solid var(--accent)` (inline custom property, from accent cycle) |
| Border radius | `--r-lg` (14px) |
| Shadow | `--shadow-xs` → `--shadow-hover` on hover |
| Hover transform | `translateY(-2px)` |
| Animation | `fadeUp` staggered |

**Child elements:**

| Class | Description |
|-------|-------------|
| `.sub-card-name` | Subject name — Poppins 600, `1.05rem`, `--text` |
| `.code-pill` | Subject code badge — `ui-monospace` / JetBrains Mono, `--primary-light` bg, `--primary` text, `--r-full`, `0.8rem` |
| `.section-pill` | Section identifier — `--surface-alt` bg, `--border` border, `--r-full`, `0.8rem 500` |

**Accent cycle implementation:**

```python
SUBJECT_ACCENTS = [
    {"accent": "#2563EB", "bg": "#EFF6FF"},  # 0 Blue
    {"accent": "#8B5CF6", "bg": "#F5F3FF"},  # 1 Purple
    {"accent": "#14B8A6", "bg": "#F0FDFA"},  # 2 Teal
    {"accent": "#F59E0B", "bg": "#FFFBEB"},  # 3 Amber
    {"accent": "#10B981", "bg": "#ECFDF5"},  # 4 Green
    {"accent": "#EF4444", "bg": "#FFF5F5"},  # 5 Red
]
style = SUBJECT_ACCENTS[index % len(SUBJECT_ACCENTS)]
```

Apply via inline style: `style="--accent: {style['accent']}; --accent-bg: {style['bg']};"`.

---

### 7.5 Auth Page

**Class:** `.auth-card`

The container for login and registration forms.

| Property | Value |
|----------|-------|
| Background | `--surface` (white) |
| Border radius | `--r-2xl` (24px) |
| Shadow | `--shadow-sm` |
| Padding | `--sp-6` (vertical) `--sp-8` (horizontal) |
| Animation | `fadeUp` 0.3s ease |

**Child elements:**

| Class | Description |
|-------|-------------|
| `.auth-brand__logo` | `3.25rem` square logo container, `--r-lg`, `--primary-muted` bg |
| `.auth-brand__title` | App name — Poppins 800, `1.5rem`, `--primary` |
| `.auth-title` | Page heading — Poppins 800, `clamp(1.75rem, 3.5vw, 2.6rem)`, `--text` |

**Mobile:** At `≤768px`, padding reduces and font sizes scale down via their `clamp()` values automatically.

---

### 7.6 Buttons

Buttons are Streamlit native elements styled via CSS injection. Three tiers of visual weight exist.

| Tier | Class Pattern | Background | Text | Border | Hover |
|------|--------------|------------|------|--------|-------|
| **Primary** | `stButton > button` (main) | `--primary` | `#FFFFFF` | none | `--primary-dark` bg + `--shadow-sm` lift |
| **Secondary** | `stButton > button` (secondary) | `--surface` | `--primary` | `1px solid --primary` | `--primary-muted` bg |
| **Tertiary** | `stButton > button` (tertiary) | transparent | `--text-muted` | none | `--surface-alt` bg |

**All buttons share:**
- Font: Inter 600, `0.9rem`
- Border radius: `--r-md` (10px) or `--r-full` for pill buttons
- Transition: `0.2s ease` on background, color, shadow, and transform
- Padding: `--sp-2` `--sp-4` (8px 16px) minimum

**Rules:**
- Never use more than one Primary button per visible section.
- Destructive actions use `--danger` fill (same structure as Primary, different colour).
- Disabled state: 60% opacity, cursor `not-allowed`, no hover effects.

---

### 7.7 Inputs

Streamlit inputs (`st.text_input`, `st.selectbox`, etc.) are styled via CSS injection.

| Property | Value |
|----------|-------|
| Background | `--surface` |
| Border | `1px solid --border` |
| Border radius | `--r-md` (10px) |
| Font | Inter 400, `0.9rem`, `--text` |
| Placeholder | `--text-subtle` |
| Focus border | `2px solid --primary` |
| Focus shadow | `0 0 0 3px rgba(37,99,235,0.15)` |
| Label | Inter 500, `0.83rem`, `--text-secondary` |
| Padding | `--sp-3` `--sp-4` |

---

### 7.8 Utility Spacers

Three utility classes create consistent vertical whitespace between sections. Use these instead of adding margin to components.

| Class | Height | Use |
|-------|--------|-----|
| `.section-gap` | `2rem` (`--sp-8`) | Between major page sections (e.g. header → KPI grid → content) |
| `.section-gap-sm` | `1rem` (`--sp-4`) | Between related sub-sections within a card or panel |
| `.section-gap-xs` | `0.5rem` (`--sp-2`) | Between tightly related elements (e.g. label + chart) |

**Usage in Python/HTML:**

```html
<div class="section-gap"></div>
<div class="section-gap-sm"></div>
<div class="section-gap-xs"></div>
```

---

## 8. Animation & Motion

### The `fadeUp` Keyframe

The single animation used across all major surfaces.

```css
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### Animation Application

| Component | Duration | Easing | Delay |
|-----------|----------|--------|-------|
| `.auth-card` | `0.3s` | `ease` | none |
| `.dash-header` | `0.3s` | `ease` | none |
| `.kpi-card` (1st) | `0.3s` | `ease` | `0.00s` |
| `.kpi-card` (2nd) | `0.3s` | `ease` | `0.04s` |
| `.kpi-card` (3rd) | `0.3s` | `ease` | `0.08s` |
| `.kpi-card` (4th) | `0.3s` | `ease` | `0.12s` |
| `.sub-card` (nth) | `0.3s` | `ease` | `n × 0.04s` |

### Hover Transitions

All interactive cards (`kpi-card`, `sub-card`, `portal-card`) share the same hover motion:

```css
transition: transform 0.25s ease, box-shadow 0.25s ease;
/* On hover: */
transform: translateY(-2px);
box-shadow: var(--shadow-hover);
```

### Motion Rules

- **Maximum duration**: `0.35s`. Nothing in the UI takes longer to animate than that.
- **Stagger limit**: Do not stagger more than 6 items. Beyond that, perceived delay feels sluggish.
- **No bounce or spring**: Easing is always `ease` or `ease-out` — never `cubic-bezier` bounce.
- **Respect `prefers-reduced-motion`**: Wrap all animations in a media query:
  ```css
  @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; transition: none !important; }
  }
  ```

---

## 9. Icons

### Library

**Material Symbols Rounded** — loaded via Google Fonts HTML link tag in the base layout.

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
```

### Usage

```html
<span class="material-symbols-rounded">icon_name</span>
```

- **Default size**: `1.15rem` (matches body text baseline).
- **Override inline** when a larger or smaller icon is needed: `style="font-size: 1.5rem"`.
- Icons should always be paired with visible text labels except in compact icon-only buttons (which must have `aria-label`).

### Common Icon Vocabulary

| Icon name | Context |
|-----------|---------|
| `school` | Academic/institution branding |
| `person` | User profile, student identifier |
| `home` | Dashboard / home navigation |
| `book_2` | Subject / course |
| `camera_alt` | Camera / face recognition attendance |
| `analytics` | Reports, analytics page |
| `group` | Class, cohort, group |
| `event_available` | Attendance record confirmed |
| `percent` | Attendance percentage |
| `calendar_month` | Date, schedule |
| `dashboard` | Dashboard view |
| `logout` | Sign out |
| `arrow_back` | Back navigation |
| `add` | Create / add new record |
| `share` | Export / share report |
| `delete` | Remove / destructive action |
| `save` | Persist data |
| `mic` | Voice input |
| `photo_prints` | Photo gallery / image output |

### Icon Colour Rules

- In KPI cards: icon fills match `--kpi-accent` on a `--*-muted` background.
- In navigation: `--text-muted` for inactive, `--primary` for active.
- In buttons: match button text colour.
- In status badges: match the semantic colour (`--success`, `--warning`, `--danger`).

---

## 10. Responsive Design

All breakpoints are applied via `@media` queries in the injected CSS. The layout is **desktop-first** (Streamlit's natural rendering direction).

### Breakpoints

| Breakpoint | Width | Label |
|------------|-------|-------|
| Mobile | `≤ 768px` | Phones, small tablets |
| Tablet | `≤ 1024px` | Tablets, small laptops |
| Desktop cap | `> 1280px` | `.block-container` max-width capped at `1280px` |

### Mobile (`≤ 768px`) Adaptations

| Element | Desktop | Mobile |
|---------|---------|--------|
| `.hide-mobile` | visible | `display: none` |
| `.top-nav__links` | visible | `display: none` |
| `.hero-title` | `clamp(2.5rem, 5vw, 4.4rem)` | `clamp(2rem, 10vw, 3rem)` |
| `.section-title` | standard | `clamp(1.4rem, 7vw, 2rem)` |
| `.auth-card` | full padding | reduced vertical padding |
| `.dash-header` | full padding | reduced padding |
| Border radii | standard scale | one step down (e.g. `--r-xl` → `--r-lg`) |
| KPI grid | 4-column | 2-column or 1-column |

### Tablet (`≤ 1024px`) Adaptations

| Element | Desktop | Tablet |
|---------|---------|--------|
| `.top-nav__actions` | `margin-left: auto` | `margin-left: 0` |
| Content columns | multi-column | may collapse to fewer |

### Desktop Cap (`> 1280px`)

```css
.block-container {
    max-width: 1280px;
    margin-inline: auto;
}
```

This prevents content from stretching uncomfortably wide on large monitors.

---

## 11. Do & Don't — Design Rules

### Colors

| ✅ Do | ❌ Don't |
|-------|---------|
| Use CSS variable tokens for every color | Hardcode hex values like `color: #10B981` |
| Use `--danger` only for genuinely problematic states | Use `--danger` as a decorative red accent |
| Use `--primary-light` / `--*-muted` for backgrounds | Put dark text directly on `--primary` without checking contrast |
| Use `--surface-alt` for zebra rows and chip fills | Use a pure white chip on a white card (invisible border is needed) |
| Test that colored text on colored bg passes WCAG AA | Assume muted tokens are accessible without checking |

### Typography

| ✅ Do | ❌ Don't |
|-------|---------|
| Use Poppins for headings, Inter for body | Mix Poppins into paragraph text |
| Use the defined type scale values | Invent intermediate sizes like `0.85rem` or `1.1rem` |
| Apply `letter-spacing: 0.08em+` to all-caps text | Use uppercase without letter-spacing |
| Let `clamp()` handle fluid sizing | Override `clamp()` sizes with fixed values at breakpoints |
| Use Inter 600 max for emphasis in body copy | Use Poppins 800 anywhere except hero/auth headings |

### Spacing

| ✅ Do | ❌ Don't |
|-------|---------|
| Use spacing tokens (`--sp-*`) for all margin and padding | Write arbitrary values like `padding: 14px 22px` |
| Use `.section-gap` classes for vertical rhythm | Add `margin-bottom` directly to section components |
| Scale spacing down at mobile via breakpoints | Use the same padding at all viewport widths |

### Components

| ✅ Do | ❌ Don't |
|-------|---------|
| Match shadow to component elevation role | Apply `--shadow-lg` to flat resting cards |
| Give interactive cards a `fadeUp` entrance | Animate decorative/static elements |
| Use `--r-full` only for pills, badges, and circles | Apply `--r-full` to large content cards |
| Use the subject accent cycle for cards | Manually pick arbitrary colours for subjects |
| Stagger card animations by `0.04s` increments | Animate more than 6 items with individual delays |
| Pair every icon-only button with `aria-label` | Use standalone icons without accessible labels |

### Responsive

| ✅ Do | ❌ Don't |
|-------|---------|
| Step border radii down one level on mobile | Keep large radii on small-screen containers |
| Use `.hide-mobile` to remove non-essential UI | Just visually compress content that doesn't fit |
| Cap the layout at `1280px` on wide screens | Let content stretch edge-to-edge on 4K monitors |

---

*Last updated: 2026-07-29 · Source: `src/ui/base_layout.py`*
