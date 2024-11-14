#!/bin/python

import csv
from dataclasses import dataclass
import os
from os.path import expanduser, abspath, isfile, islink, isdir
import argparse

CONFIG = "./configurations.csv"

@dataclass
class config:
  name: str = ""
  source: str = ""
  destination: str = ""
  source2: str = ""
  destination2: str = ""

class Text:
  BOLD_START = '\033[1m'
  END = '\033[0m'
  UNDERLINE = '\033[4m'
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'

def full_path(path):
  return abspath(expanduser(path))

def config_init():
  config_list = []
  with open(CONFIG) as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
      config_list.append(config())
      config_list[i].name = row[0]
      config_list[i].source = row[1]
      config_list[i].destination = row[2]
      config_list[i].source2 = row[3]
      config_list[i].destination2 = row[4]
      i = i + 1
  return sorted(config_list, key=lambda x: x.name)

def write_config(config_list):
  with open(CONFIG, 'w') as csvfile:
    for x in config_list:
      csvfile.write(f"{x.name},{x.source},{x.destination},{x.source2},{x.destination2}\n")

def add_config(name, source, destination, source2, destination2):
  with open(CONFIG, 'a') as csvfile:
    csvfile.write(f"{name},{source},{destination},{source2},{destination2}\n")

def list_installed(config_list):
  installed = []
  for config in config_list:
    if islink(full_path(config.destination)):
      installed.append(config)
  return installed

def list_not_installed(config_list):
  not_installed = []
  for config in config_list:
    if not islink(full_path(config.destination)):
      not_installed.append(config)
  return not_installed

def install_config(name):
  if not isdir(full_path("~/.config")):
    os.mkdir(full_path("~/.config"))
  for y in name:
    for x in not_installed:
      if y == x.name:
        if isfile(full_path(x.destination)):
          print(f"File found at {x.destination}, removing...")
          os.remove(full_path(x.destination))
        print(f"Symbolic linking {x.source} -> {x.destination}")
        os.symlink(full_path(x.source), full_path(x.destination))
        if not x.destination2 == "":
          if isfile(full_path(x.destination2)):
            print(f"File found at {x.destination}, removing...")
            os.remove(full_path(x.destination2))
          print(f"Symbolic linking {x.source2} -> {x.destination2}")
          os.symlink(full_path(x.source2), full_path(x.destination2))

def remove_duplicate(x):
  final_list = []
  for y in x:
    if x not in final_list:
      final_list.append(x)
  return final_list

def remove_config(name):
  for y in name:
    for x in installed:
      if y == x.name:
        print(f"Removing {x.destination}")
        os.remove(full_path(x.destination))
        if not x.destination2 == "":
          print(f"Removing {x.destination2}")
          os.remove(full_path(x.destination2))

def delete_config(name):
  not_list = []
  for y in name:
    for x in full_config_list:
      if y == x.name:
        full_config_list.remove(x)
  write_config(full_config_list)

full_config_list = config_init()
write_config(full_config_list)
installed = list_installed(full_config_list)
not_installed = list_not_installed(full_config_list)

parser = argparse.ArgumentParser("dotfiles_installer")
parser.add_argument("-i", "--install", help="Install configs", nargs="+")
parser.add_argument("-r", "--remove", help="Remove configs", nargs="+")
parser.add_argument("-l", "--list", help="List configs", action="store_true")
parser.add_argument("-a", "--add", help="Add new configs", action="store_true")
parser.add_argument("-d", "--delete", help="Delete configs", nargs="+")
args = parser.parse_args()

if args.install:
  install_config(args.install)
elif args.remove:
  remove_config(args.remove)
elif args.list:
    print(Text.BOLD_START + Text.GREEN + "Installed" + Text.END)
    for x in installed:
        print(x.name)
    print(Text.BOLD_START + Text.RED + "Not Installed" + Text.END)
    for x in not_installed:
        print(x.name)
elif args.add:
  print("Name: ")
  name = input()
  print("Source: ")
  source = input()
  print("Destination: ")
  destination = input()
  print("Source 2: ")
  source2 = input()
  print("Destination 2: ")
  destination2 = input()
  add_config(name, source, destination, source2, destination2)
elif args.delete:
  delete_config(args.delete)
else:
  parser.print_help()
