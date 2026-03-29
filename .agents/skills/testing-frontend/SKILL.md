# Testing: Space Games Downloads Frontend

## Overview
This is a static Vite + React + TypeScript + Tailwind CSS frontend app. No backend, no authentication required.

## App Structure
- All UI logic lives in `src/App.tsx`
- Data is hardcoded (no API calls)
- Images are in `public/images/` (sourced from Unsplash)
- Build output goes to `dist/`

## Running Locally
```bash
cd /home/ubuntu/eve-downloads  # or wherever the app is
npm install
npm run dev   # starts dev server at http://localhost:5173
npm run build # builds to dist/
```

## Deployment
- Use `deploy_frontend` with `dir` pointing to the `dist/` folder after running `npm run build`
- No backend deployment needed
- No environment variables required

## Key Interactive Elements to Test
1. **Game filter buttons** — 7 buttons (All Games + 6 games). Clicking one filters cards to only that game.
2. **Category tabs** — 7 tabs (All + 6 categories). Clicking one filters cards to only that category.
3. **Search bar** — Filters cards by title, description, or game name (case-insensitive). Has an X clear button.
4. **Combined filters** — Game + category + search all apply simultaneously (AND logic).
5. **Results counter** — Text below filters shows "Showing X of 24 items" with active filter names.
6. **Empty state** — When no items match, shows "No downloads found" message.
7. **Download buttons** — Present on every card but non-functional (no onClick handler).

## Useful Filter Combinations for Testing
- Eve Online: 6 items
- Star Citizen: 4 items
- Elite Dangerous: 4 items
- Guides & Manuals (all games): 6 items
- Wallpapers (all games): 6 items
- Eve Online + Guides: 1 item (Fleet Commander's Guide)
- X4: Foundations + Icons & Badges: 0 items (triggers empty state)
- Search "thargoid": 1 result (Thargoid Encounter Fan Art, Elite Dangerous)

## Devin Secrets Needed
None — this is a fully static app with no authentication or API keys.

## Tips
- Images may fail to load if Unsplash URLs change; the app has fallback placeholders via `onError` handlers.
- The app has no routing — everything is on a single page.
- No CI is configured on this repo, so there are no checks to wait for.
