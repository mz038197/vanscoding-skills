---
name: deploy-cheatsheet
description: Quick-reference card for Netlify CLI commands actually run end-to-end (login, sites:create, deploy). Use when the user wants a copy-pasteable deploy script.
---

# Deploy cheatsheet — verified commands

> These are the commands that actually worked against `netlify-cli@latest` on Windows PowerShell in 2026-08. Older skill docs assumed `--no-build`; that flag is gone in current versions. Do **not** add `--no-build` — it errors with `unknown option '--no-build'`.

## One-time setup

### 1. Login (opens OAuth page in browser)

```powershell
npx --yes netlify-cli login --new --debug
```

- `--new` is optional but forces a fresh ticket.
- `--debug` keeps stdout non-empty in case the user needs to see what's happening.
- The browser opens `https://app.netlify.com/authorize?...` automatically. User clicks **Authorize**.
- `npx` will download netlify-cli on first run (may take ~30s). Subsequent runs hit the cache.

### 2. Find your team slug

```powershell
npx --yes netlify-cli api listAccountsForUser
```

Returns JSON; pick `slug` (e.g. `mz038197`). `--account-slug` needs this, **not** the team's display `name`.

### 3. Create + link the site

```powershell
cd <artifact-folder>
npx --yes netlify-cli sites:create --account-slug <team-slug> --name <site-name> --json
```

- Creates a blank site under the team.
- Auto-links the current directory to that site (writes `.netlify/state.json`).
- `--json` keeps output parseable. Skip `--create-site` — that flag no longer exists on `deploy`.
- Returns `id`, `name`, `url` (`https://<name>.netlify.app`).

## Every deploy

```powershell
cd <artifact-folder>
npx --yes netlify-cli deploy --dir=. --prod --json
```

- `--dir=.` points at the current folder. Replace with `dist`/`build` if there's a build output.
- `--prod` publishes to production (default would be a draft URL).
- `--json` is required — read `.url` for the live URL, **do not** parse stdout banners.
- Already-linked folders run non-interactively. Unlinked folders will hang waiting for input — that's the most common reason a deploy "freezes."

## Update flow

The same `deploy --dir=. --prod --json` command overwrites the live site. URL stays the same. No rollback API needed; just fix the artifact and re-run.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `unknown option '--no-build'` | Newer CLI removed the flag | Drop it; default is no build |
| Deploy hangs, no output | Folder not linked | Run `sites:create` first, or `netlify link` |
| `404: Not Found` on `sites:create` | Used team `name` instead of `slug` | Run `listAccountsForUser`, use `slug` field |
| `Error: Missing required path variable 'account_slug'` | Old API call shape | Use the `sites:create` command instead of `api createSiteInTeam` |
| Browser doesn't open for OAuth | Headless env or popup blocked | Copy the `https://app.netlify.com/authorize?...` URL from stdout into a browser manually |
