#!/bin/bash

pwd=$(pwd)

if_exists () {
    if [ -f "$1" ]; then
      rm "$1"
    elif [ -L "$1" ]; then
	    rm "$1"
    elif [ -d "$1" ]; then
      rm -r "$1"
    fi
}

if pacman -Qi gum > /dev/null; then
  echo "Gum is installed"
else
  echo "Installing gum"
  sudo pacman -S --noconfirm gum
fi

TYPE=$(gum choose "all" "vim" "zsh" "xorg" "i3")

case $TYPE in
  "all")
    echo "Installing all links"
    if_exists ~/.vimrc
    ln -s $pwd/.vimrc ~/.vimrc
    
    if_exists ~/.zshrc
    ln -s $pwd/.zshrc ~/.zshrc
    
    if_exists ~/.zsh
    ln -s $pwd/.zsh ~/.zsh
    
    if_exists ~/.Xresources
    ln -s $pwd/.Xresources ~/.Xresources
    
    if_exists ~/.Xdefaults
    ln -s $pwd/.Xresources ~/.Xdefaults
    
    if_exists ~/.config/i3/config
    ln -s $pwd/.config/i3/config ~/.config/i3/config
    
    if_exists ~/.config/i3status/config
    ln -s $pwd/.config/i3status/config ~/.config/i3status/config;;

  "vim")
    echo "Installing vim links"
    if_exists ~/.vimrc
    ln -s $pwd/.vimrc ~/.vimrc;;

  "zsh")
    echo "Installing zsh links"
    if_exists ~/.zshrc
    ln -s $pwd/.zshrc ~/.zshrc
    
    if_exists ~/.zsh
    ln -s $pwd/.zsh ~/.zsh;;

  "xorg")
    echo "Installing Xorg links"
    if_exists ~/.Xresources
    ln -s $pwd/.Xresources ~/.Xresources
    
    if_exists ~/.Xdefaults
    ln -s $pwd/.Xresources ~/.Xdefaults;;

  "i3")
    echo "Installing i3 links"
    if_exists ~/.config/i3/config
    ln -s $pwd/.config/i3/config ~/.config/i3/config
    
    if_exists ~/.config/i3status/config
    ln -s $pwd/.config/i3status/config ~/.config/i3status/config;;
esac

echo "Done :)"
