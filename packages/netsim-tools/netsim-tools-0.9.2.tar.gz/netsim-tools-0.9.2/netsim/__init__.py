#!/usr/bin/env python3
#
# Create expanded topology file, Ansible inventory, host vars, or Vagrantfile from
# topology file
#

from box import Box

from . import common
from . import read_topology
from . import augment
from .outputs import ansible
from .providers import Provider

import argparse

__version__ = "0.9.2"

def dump_topology_data(topology: Box, state: str) -> None:
  print("%s topology data" % state)
  print("===============================")

  topo_copy = Box(topology,box_dots=True)

  topo_copy.pop("nodes_map",None)
  print(topo_copy.to_yaml())

def set_logging_flags(args: argparse.Namespace) -> None:
  if args.verbose:
    common.VERBOSE = True

  if args.logging:
    common.LOGGING = True

def main(args: argparse.Namespace) -> None:
  set_logging_flags(args)
  topology = read_topology.load(args.topology,args.defaults,"package:topology-defaults.yml")
  if args.verbose:
    dump_topology_data(topology,'Collected')
  common.exit_on_error()

  augment.main.transform(topology)
  common.exit_on_error()
  if args.provider is not None:
    provider = Provider.load(topology.provider,topology.defaults.providers[topology.provider])
    if args.verbose:
      common.error("Use 'netlab create -o provider=-' to write provider configuration file to stdout")
    else:
      provider.create(topology,args.provider)

  if args.xpand:
    if args.verbose:
      dump_topology_data(topology,'Augmented')
    else:
      augment.topology.create_topology_file(topology,args.xpand)

  if args.inventory:
    if args.verbose:
      ansible.dump(topology)
    else:
      ansible.ansible_inventory(topology,args.inventory,args.hostvars)

  if args.config:
    ansible.ansible_config(args.config,args.inventory)
