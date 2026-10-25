FROM node:22-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends git python3 python3-pytest ca-certificates && rm -rf /var/lib/apt/lists/*
RUN npm install -g typescript@5 tsx vitest@3 && npm cache clean --force
