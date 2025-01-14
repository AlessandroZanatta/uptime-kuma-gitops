# Uptime Kuma GitOps

This is a simple Python script that interacts with your Uptime Kuma instance. The goal is being able to have a YAML description of the Uptime Kuma configuration, thus enabling GitOps. Currently, it is not possible to control all the features of Uptime Kuma (such as proxies, maintenance periods, and so on). Only initial setup, notifications, monitors and status pages are supported.

This script will basically:

- fetch the current state of monitors, notifications, and status pages
- update the state of these resources, regardless of their state (updated or stale)

**NOTE**: this was built with compatibility with Uptime Kuma v2 in mind. In particular, it has been tested solely with the `beta` tag (and not extensively).

**Note**: while running this should be safe and non-destructive, run it carefully in production environments!

## Usage

Please refer to `examples/config.yaml` for an example configuration.
To add options to the monitors, notifications or status pages, please check out the related WebSocket call or open an issue/PR to expand the examples.

To run the script, use your system Python, or use [`uv`](https://docs.astral.sh/uv). With `uv`, simply run: `AUTH__PASSWORD=<your admin pwd> CONFIG_PATH=<path/to/config.yaml> uv run src/main.py` to setup your Uptime Kuma instance!

A docker container is also available! The container will sync the status of the Uptime kuma instance, and then exit.
Example usage:

```
docker run -it -v <path/to/config.yaml>:/config.yaml -e AUTH__PASSWORD=<your admin pwd> --restart no ghcr.io/alessandrozanatta/uptime-kuma-gitops:latest
```
