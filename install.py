import os
import streamlit as st

class Config:
  def __init__(self, name, local, to):
    self.name = name
    self.local = local
    self.to = to

def absolute_path(path):
  return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

def install(config):
  if os.path.islink(absolute_path(config.to)):
    st.warning("Link found. Removing!")
    os.unlink(absolute_path(config.to))
  elif os.path.isfile(absolute_path(config.to)):
    st.warning("File found. Removing!")
    os.remove(absolute_path(config.to))
  elif os.path.isdir(absolute_path(config.to)):
    st.warning("Directory found. Removing!")
    os.rmdir(absolute_path(config.to))
  st.info(f"Installing {config.name} links!")
  os.symlink(config.local, absolute_path(config.to))

dunst = Config("dunst", ".config/dunst", "~/.config/dunst")
hyprland = Config("hyprland", ".config/hypr", "~/.config/hypr")
i3 = Config("i3", ".config/i3/config", "~/.config/i3/config")
pylint = Config("pylint", ".pylintrc", "~/.pylintrc")
rofi = Config("rofi", ".config/rofi", "~/.config/rofi")
tmux = Config("tmux", ".tmux.conf", "~/.tmux.conf")
kitty = Config("kitty", ".config/kitty", "~/.config/kitty")
vim = Config("vim", ".vimrc", "~/.vimrc")
waybar = Config("waybar", ".config/waybar", "~/.config/waybar")
xdefaults = Config("xdefaults", ".Xresources", "~/.Xdefaults")
xresources = Config("xresources", ".Xresources", "~/.Xresources")
zsh = Config("zsh", ".zshrc", "~/.zshrc")
zsh_directory = Config("zsh_directory", ".zsh", "~/.zsh")


app_config = st.multiselect('Choose configs to systemlink:', ["dunst", "hyprland", "i3", "pylint", "rofi", "tmux", "kitty", "vim", "waybar", "xorg", "zsh"])
button = st.button('Submit')

if button and app_config:
  st.success("Installing configs....")
  for app in app_config:
    match app:
      case dunst.name:
        install(dunst)
      case hyprland.name:
        install(hyprland)
      case i3.name:
        install(i3)
      case pylint.name:
        install(pylint)
      case rofi.name:
        install(rofi)
      case tmux.name:
        install(tmux)
      case kitty.name:
        install(kitty)
      case vim.name:
        install(vim)
      case waybar.name:
        install(waybar)
      case "xorg":
        install(xdefaults)
        install(xresources)
      case zsh.name:
        install(zsh)
        install(zsh_directory)
