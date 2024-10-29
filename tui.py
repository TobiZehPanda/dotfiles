import pytermgui as ptg
import csv
from dataclasses import dataclass
import os.path

CONFIG = "./configurations.csv"
OUTPUT = {}

@dataclass
class config:
  name: str = ""
  source: str = ""
  destination: str = ""
  source2: str = ""
  destination2: str = ""

def config_count():
  with open(CONFIG) as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
      i = i + 1
  return i

def config_init():
  # config_list = [config() for i in range(config_count())]
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

def config_write(config_list):
  with open(CONFIG, 'w') as csvfile:
    for x in config_list:
      csvfile.write(f"{x.name},{x.source},{x.destination},{x.source2},{x.destination2}\n")

def add_config(manager: ptg.WindowManager, window: ptg.Window):
  for widget in window:
    if isinstance(widget, ptg.InputField):
      if widget.prompt == "Name: ":
        name = widget.value
      elif widget.prompt == "Source: ":
        source = widget.value
      elif widget.prompt == "Destination: ":
        destination = widget.value
      elif widget.prompt == "Source 2: ":
        source2 = widget.value
      elif widget.prompt == "Destination 2: ":
        destination2 = widget.value
      continue
  manager.stop()
  with open(CONFIG, 'a') as csvfile:
    csvfile.write(f"{name},{source},{destination},{source2},{destination2}\n")

def list_installed(config_list):
  installed = []
  for config in config_list:
    if os.path.islink(os.path.expanduser(config.destination)):
      installed.append(config)
  return installed

def list_not_installed(config_list):
  not_installed = []
  for config in config_list:
    if not os.path.islink(os.path.expanduser(config.destination)):
      not_installed.append(config)
  return not_installed

def install_config(manager: ptg.WindowManager, window: ptg.Window):
  name = ""
  for widget in window:
    if isinstance(widget, ptg.InputField):
      if widget.prompt == "Name: ":
        name = widget.value
      continue
  name = name.replace(",", " ")
  name_split = name.split()
  manager.stop()
  for y in name_split:
    for x in not_installed:
      if y == x.name:
        if os.path.isfile(os.path.expanduser(x.destination)):
          os.remove(os.path.expanduser(x.destination))
        os.symlink(os.path.expanduser(x.source), os.path.expanduser(x.destination))
        if not x.destination2 == "":
          if os.path.isfile(os.path.expanduser(x.destination2)):
            os.remove(os.path.expanduser(x.destination2))
          os.symlink(os.path.expanduser(x.source2), os.path.expanduser(x.destination2))

def remove_duplicate(x):
  final_list = []
  for y in x:
    if x not in final_list:
      final_list.append(x)
  return final_list

def remove_config(manager: ptg.WindowManager, window: ptg.Window):
  name = ""
  for widget in window:
    if isinstance(widget, ptg.InputField):
      if widget.prompt == "Name: ":
        name = widget.value
      continue
  name = name.replace(",", " ")
  name_split = name.split()
  manager.stop()
  for y in name_split:
    for x in installed:
      if y == x.name:
        os.remove(os.path.expanduser(x.destination))
        if not x.destination2 == "":
          os.remove(os.path.expanduser(x.destination2))

def _define_layout() -> ptg.Layout:
  layout = ptg.Layout()
  layout.add_slot("Header", height=3)
  layout.add_break()

  layout.add_slot("AddConfig")
  layout.add_break()

  layout.add_slot("Installer", width=0.5)
  layout.add_slot("NotInstalled", width=0.25)
  layout.add_slot("Installed", width=0.25)
  return layout

full_config_list = config_init()
config_write(full_config_list)
installed = list_installed(full_config_list)
not_installed = list_not_installed(full_config_list)

with ptg.WindowManager() as manager:
  manager.layout = _define_layout()
  header_win = ptg.Window(
  "[green bold]Dotfiles Config",
  )
  manager.add(header_win, assign="header")
  addconfig_win = ptg.Window(
    ptg.InputField("", prompt="Name: "),
    "",
    ptg.InputField("", prompt="Source: "),
    "",
    ptg.InputField("", prompt="Destination: "),
    "",
    ptg.InputField("", prompt="Source 2: "),
    "",
    ptg.InputField("", prompt="Destination 2: "),
    "",
    "",
    ptg.Button("Add", lambda *_: add_config(manager, addconfig_win)),
    title="[yellow bold]Add Config",
  )
  manager.add(addconfig_win, assign="addconfig")
  installer_win = ptg.Window(
    ptg.InputField("", prompt="Name: "),
    "",
    (ptg.Button("[green bold]Install", lambda *_: install_config(manager, installer_win)), ptg.Button("[red bold]Remove", lambda *_: remove_config(manager, installer_win))),
    title="[cyan bold]Installer",
  )
  manager.add(installer_win, assign="installer")
  buffer = ""
  for x in not_installed:
    buffer += x.name 
    buffer += "\n"
  not_installed_win = ptg.Window(
    buffer,
    title="[red bold]Not Installed",
  )
  manager.add(not_installed_win, assign="notinstalled")
  buffer = ""
  for x in installed:
    buffer += x.name 
    buffer += "\n"
  installed_win = ptg.Window(
  buffer,
  title="[green bold]Installed",
  )
  manager.add(installed_win, assign="installed")
