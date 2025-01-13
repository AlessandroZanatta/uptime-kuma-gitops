# Uptime Kuma GitOps

This is a simple Python script that interacts with your Uptime Kuma instance. The goal is being able to have a YAML description of the Uptime Kuma configuration, thus enabling GitOps. Currently, it is not possible to control all the features of Uptime Kuma (such as proxies, maintenance periods, and so on). Only initial setup, notifications, monitors and status pages are supported.

**NOTE**: this was built with compatibility with Uptime Kuma v2 in mind. In particular, it has been tested solely with the `beta` tag.

**Note**: while running this should be safe and non destructive, run it carefully in production environments!

## Usage

Please refer to `examples/config.yaml` for an example configuration.
To add options to the monitors, notifications or status pages, please check out the related WebSocket call or open an issue/PR to expand the examples.
