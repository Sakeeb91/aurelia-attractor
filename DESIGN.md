# Design

## Theme

Single locked dark theme ("the abyss"). No light mode: the content is luminous particles on darkness; inverting it would destroy the object being shown. This is the print-emulating exception in reverse: the medium is light itself.

## Color

Derived from the repository's committed "abyssal gold" colormap (`scripts/render_gallery.py`):

| Token | Value | Role |
|---|---|---|
| `--bg` | `#07060f` | page background (off-black indigo, never pure black) |
| `--surface` | `rgb(16 14 30 / 0.82)` | HUD panel background |
| `--ink` | `#ece9f4` | primary text |
| `--ink-dim` | `#9d97b8` | secondary text (AA on --bg and --surface) |
| `--gold` | `#ffd97d` | single interactive accent: focus, active states, slider thumbs |
| `--violet` | `#a44a9c` | data accent inside the canvas ramp only, not UI chrome |
| `--line` | `rgb(236 233 244 / 0.14)` | hairlines |

Particle ramp (z-height): `#1b1040 → #4b2e83 → #a44a9c → #e0719b → #f4a261 → #ffd97d → #fff3d6`.

One accent rule: gold is the only interactive accent across the whole page.

## Typography

- **Wordmark + numerals:** `ui-monospace, "SF Mono", "Cascadia Mono", monospace`. AURELIA wordmark in spaced uppercase mono; all live numbers tabular mono.
- **Body / labels:** system sans (`-apple-system, "Segoe UI", system-ui, sans-serif`).
- No webfonts: instant LCP, no FOIT, the page's beauty budget is spent on WebGL.
- Scale: 11px mono labels, 13px body, 15px panel headings, 28px wordmark.

## Components

- **HUD title block** (top-left): wordmark, one-line system description, three real stats (lambda-1, D_KY, equilibrium) in mono.
- **Control panel** (right side, bottom sheet on mobile): grouped sliders (parameters a/b/c, flow speed, particle size, exposure), toggle buttons (pause, auto-rotate, trails), reset actions. Flat panel, 1px hairline border, 14px radius, no glass blur (perf: it sits over a live WebGL canvas).
- **Status line**: integration state ("tracing orbit...", "diverged, restored canonical") with `aria-live=polite`.

## Shape & Spacing

- One radius system: 14px panels, 10px controls, pill sliders.
- 8px spacing rhythm; panel padding 20px.
- z-scale: canvas 0, HUD 10, panel 20, toast 30.

## Motion

- The WebGL scene is the motion: orbit drift (auto-rotate, slow), live particle advection, orbit trail growth on load.
- UI motion: 180ms ease-out transitions on hover/active; no entrance choreography.
- `prefers-reduced-motion`: auto-rotate off, particle drift paused at a fully drawn attractor, all UI transitions instant.
