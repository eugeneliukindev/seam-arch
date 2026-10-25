FROM rust:1-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends git python3 python3-pytest && rm -rf /var/lib/apt/lists/*
RUN rustup component add clippy
ENV CARGO_HOME=/usr/local/cargo
