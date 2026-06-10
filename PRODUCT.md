# Product

## Register

brand

## Users

Dynamical-systems researchers, generative-art enthusiasts, and curious visitors arriving from the GitHub repo or a shared link. They come to *see* the Aurelia attractor: a newly discovered chaotic system. Viewing context: a desktop browser most of the time, sometimes a phone, usually in a dim room because the content is a glowing dark visualization.

## Product Purpose

An interactive WebGL viewer that lets anyone fly around the Aurelia attractor, watch particles ride its flow in real time, and perturb its three parameters to feel where chaos lives. Success: a visitor understands within ten seconds that this is a real mathematical object, beautiful on its own terms, and stays to play with it.

## Brand Personality

Abyssal, precise, luminous. The page is an observatory, not a dashboard: the attractor is the hero, the interface recedes. Numbers are real (Lyapunov exponents, fractal dimension), never decorative.

## Anti-references

- Generic three.js demo pages with lil-gui default panels and stats.js counters
- AI-slop landing pages: purple gradients, glass cards everywhere, eyebrow labels on every block
- Dense dashboard chrome that competes with the visualization

## Design Principles

1. **The attractor is the interface.** Chrome exists only to serve looking; everything else gets out of the way.
2. **Real numbers only.** Every figure shown is computed, reproducible, and recorded in the repo.
3. **Touch it to trust it.** Parameters are live; chaos is something you perturb, not just read about.
4. **One palette, one light source.** The abyssal-gold ramp from the gallery renders everything; UI accents borrow from it.

## Accessibility & Inclusion

- WCAG AA contrast for all HUD text against the dark backdrop
- Full keyboard operation (orbit via drag is mouse/touch, but all controls are focusable buttons/sliders)
- `prefers-reduced-motion` collapses auto-rotation and particle drift to a still render
- Touch targets at least 44px on coarse pointers
