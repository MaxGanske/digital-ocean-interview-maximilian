OrbStack local dev
==================

This project uses OrbStack for local development instead of Docker.

Quick start
-----------

1. Install OrbStack for your OS (follow OrbStack's official instructions).
2. Copy the example env and adjust if needed:

```bash
cp .env.example .env
```

3. Start the development environment using OrbStack's compose compatibility:

```bash
orbstack compose up --build
# or: orbstack up (if your OrbStack installation provides a convenience command)
```

Notes
-----
- `orbstack.yml` in the repo mirrors the previous `docker-compose.yml` layout.
- OrbStack aims to be Docker-compatible for local workflows; if your OrbStack install uses a slightly different command, use the equivalent compose-compatible command.
- For production image builds and deployment to DigitalOcean, build and publish a container image using your preferred CI or `docker`/`podman` toolchain.
