# QEPilot Stack

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A browsable catalogue of Claude Code components — agents, commands, skills, MCP
servers, hooks and settings — with a one-line install for each.

| | |
|---|---|
| **Dashboard** | https://app.qapilot.live |
| **Static site** | http://stack.qapilot.live |

## What this is

Claude Code can be extended with reusable components: subagents that specialise
in a task, custom slash commands, skills, MCP server configs, hooks and settings
bundles. This project indexes them and makes them searchable, so you can find
one and install it without hunting through a repository.

Install any component with the upstream CLI:

```bash
npx claude-code-templates@latest --skill creative-design/frontend-design
npx claude-code-templates@latest --agent development-team/frontend-developer
npx claude-code-templates@latest --command testing/generate-tests
```

## Repository layout

| Path | What it is |
|---|---|
| `dashboard/` | Astro 5 + React + Tailwind app — serves `app.qapilot.live`, deployed to Cloudflare Pages |
| `docs/` | Older static HTML site — serves `stack.qapilot.live` via GitHub Pages |
| `cli-tool/` | The `claude-code-templates` npm CLI and the component library it installs from |
| `cloudflare-workers/` | Scheduled workers (cron, reports, newsletter) |
| `scripts/` | Catalogue generation — `generate_components_json.py` builds the JSON both sites read |

## Local development

```bash
# Dashboard (Astro) — http://localhost:4321
cd dashboard && npm install && npm run dev

# Static site — http://localhost:8908
python3 -m http.server 8908 --directory docs
```

Regenerate the component catalogue after adding or changing components:

```bash
python3 scripts/generate_components_json.py
```

## Deploying

The dashboard deploys to Cloudflare Pages:

```bash
cd dashboard && npm run build
npx wrangler pages deploy dist --project-name=qepilot-stack-dashboard
```

The static site publishes from `docs/` on the default branch via GitHub Pages.

CI deploys are wired in `.github/workflows/deploy.yml` but inactive until
`CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set as repository
secrets.

## Configuration

Authentication is intentionally **not configured**. Browsing, search and
installation all work without it; sign-in, saved collections and download
tracking do not, and their UI degrades quietly rather than erroring.

To enable them, create your own Clerk application, GitHub OAuth app, Supabase
project and Neon database, then:

- set `PUBLIC_CLERK_PUBLISHABLE_KEY` and `PUBLIC_GITHUB_CLIENT_ID` as repository
  **variables** (the deploy workflow reads `${{ vars.* }}`) and in
  `dashboard/wrangler.toml`
- set `CLERK_SECRET_KEY`, `GITHUB_CLIENT_SECRET`, `SUPABASE_URL`,
  `SUPABASE_SERVICE_ROLE_KEY` and `NEON_DATABASE_URL` as Cloudflare Pages
  secrets via `wrangler pages secret put`

CLI telemetry is off unless `QEPILOT_TELEMETRY=1` is set.

## Credits

This is a fork of
**[claude-code-templates](https://github.com/davila7/claude-code-templates)**
by **Daniel (San) Ávila**, used under the MIT licence. The component library,
the CLI and both site codebases are their work; this fork rebrands the sites and
changes how they are hosted and configured.

If you find this useful, the upstream project is the place to star, contribute
components, and support the author.

The component catalogue is still served by upstream infrastructure — see
`cli-tool/src/upstream-config.js` to point it at your own.

## Licence

MIT — see [LICENSE](LICENSE). The original copyright notice is retained, as the
licence requires.
