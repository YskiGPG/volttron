# Home Assistant Test Instance

A disposable Home Assistant instance for running the Home Assistant driver
integration tests without touching a production HA deployment.

## Start

```bash
cd services/core/PlatformDriverAgent/tests/ha-docker
docker compose up -d
docker compose logs -f   # watch startup; Ctrl+C does not stop the container
```

First boot pulls ~500 MB and takes 1-2 minutes. HA is ready when the log
shows `INFO (MainThread) [homeassistant.core] Starting Home Assistant`
followed by the HTTP server line.

Open <http://localhost:8123> and complete onboarding:

1. Create a local account (any username/password — this instance is disposable).
2. Pick Seattle as the location.
3. **Profile → Security → Long-lived access tokens → Create token.**
   Copy the token into the `access_token` field of your
   `HomeAssistant_Driver/*.example.config` files.
4. **Settings → Devices & services → Helpers → Create Helper**:
   - `Toggle` named `volttrontest` (exercises the `input_boolean` domain)
   - Additional `Input boolean` / `Input number` helpers as needed to
     stand in for switch / fan / cover entities.

## Stop / reset

```bash
docker compose down           # stop, keep config
docker compose down -v        # stop and wipe the bind-mounted config
rm -rf config                 # full reset: forces fresh onboarding next start
```

## Notes

- `config/` is bind-mounted and git-ignored — it contains the HA database,
  your account, and the access token. Never commit it.
- The driver running on the host reaches HA at `http://127.0.0.1:8123`.
- Time zone is `America/Los_Angeles`; change the `TZ` env var in
  `docker-compose.yml` if you are elsewhere.
