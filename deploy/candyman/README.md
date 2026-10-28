# candyman deploy (no-hype-ai/OpenHands)

Always-on OpenHands for the home server **candyman**. This folder is the
lift-up recipe for Nick’s fork; runtime secrets stay in `~/.openhands` on the
host and are **not** committed.

Upstream can be refreshed later with:

```bash
git fetch upstream
git merge upstream/main   # or rebase — do this deliberately
```

`upstream` remote: `https://github.com/OpenHands/OpenHands.git`

## Prerequisites

- Docker Engine on candyman
- Existing `~/.openhands` state (profiles, encrypted keys) — backup first via
  `~/Code/candyman-cleanup/scripts/backup-keepers.sh`
- Workspace dir (default `/home/nick/openhands-workspace`)

## Lift up

```bash
cd ~/Code/OpenHands
mkdir -p /home/nick/openhands-workspace
cp deploy/candyman/.env.example deploy/candyman/.env
# edit .env if needed

docker pull docker.all-hands.dev/all-hands-ai/runtime:0.59-nikolaik
docker compose -f deploy/candyman/docker-compose.yml --env-file deploy/candyman/.env up -d
```

UI: `http://127.0.0.1:3000` on the box. From another machine:

```bash
ssh -L 3000:127.0.0.1:3000 candyman   # or Tailscale Serve later
```

## Profiles (sanitized examples)

| File | Purpose |
|---|---|
| `profiles/deepseek-v4-pro.example.json` | LLM profile defaults (DeepSeek via OpenRouter) |
| `agent-profiles/default.example.json` | Default agent profile referencing that LLM |

Live copies with API keys live only under `~/.openhands/`. To re-seed a blank
host, copy the examples into `~/.openhands/profiles/` /
`~/.openhands/agent-profiles/` (drop `.example`), then set the key in the UI.

## Relation to candyman-cleanup

Cluster/home-server plan: `~/Code/candyman-cleanup` (OpenHands is a P0 keeper).
This repo owns the **app + compose recipe**; cleanup owns inventory/backup/K3s.
