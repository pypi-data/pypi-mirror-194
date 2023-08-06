import subprocess

from e2e_cli.config.config_routing import ConfigRouting
from e2e_cli.loadbalancer.lb_routing import LBRouting
from e2e_cli.node.node_routing import NodeRouting
from e2e_cli.bucket_store.bucket_routing import BucketRouting
from e2e_cli.dbaas.dbaas_routing import DBaaSRouting


class CommandsRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.command is None:
            subprocess.call(['e2e_cli', '-h'])

        elif self.arguments.command == "config":
            ConfigRouting(self.arguments).route()

        elif self.arguments.command == "node":
            NodeRouting(self.arguments).route()

        elif self.arguments.command == "lb":
            LBRouting(self.arguments).route()
        
        elif self.arguments.command == "bucket":
            BucketRouting(self.arguments).route()
            
        elif self.arguments.command == "dbaas":
            DBaaSRouting(self.arguments).route()
