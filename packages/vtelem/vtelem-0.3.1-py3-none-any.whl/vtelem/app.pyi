import argparse
from vtelem.mtu import Host as Host
from vtelem.telemetry.server import TelemetryServer as TelemetryServer
from vtelem.types.telemetry_server import Service as Service, TelemetryServices as TelemetryServices, default_services as default_services

def entry(args: argparse.Namespace) -> int: ...
def add_app_args(parser: argparse.ArgumentParser) -> None: ...
