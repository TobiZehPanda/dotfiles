#!/bin/bash

pwd=$(pwd)

if_exists() {
    if [ -f "$1" ]; then
      rm "$1"
    elif [ -L "$1" ]; then
	    rm "$1"
    elif [ -d "$1" ]; then
      rm -r "$1"
    fi
}

link_vim() {
  echo "Installing vim links"
  if_exists ~/.vimrc
  ln -s $pwd/.vimrc ~/.vimrc
}

link_zsh() {
  echo "Installing zsh links"
  if_exists ~/.zshrc
  ln -s $pwd/.zshrc ~/.zshrc
  
  if_exists ~/.zsh
  ln -s $pwd/.zsh ~/.zsh
}

link_tmux() {
  echo "Installing tmux links"
  if_exists ~/.tmux.conf
  ln -s $pwd/.tmux.conf ~/.tmux.conf  
}

link_xorg() {
  echo "Installing Xorg links"
  if_exists ~/.Xresources
  ln -s $pwd/.Xresources ~/.Xresources
  
  if_exists ~/.Xdefaults
  ln -s $pwd/.Xresources ~/.Xdefaults
}
link_i3() {
  echo "Installing i3 links"
  if_exists ~/.config/i3/config
  ln -s $pwd/.config/i3/config ~/.config/i3/config
    
  if_exists ~/.config/i3status/config
  ln -s $pwd/.config/i3status/config ~/.config/i3status/config
}

if pacman -Qi gum > /dev/null; then
  echo "Gum is installed"
else
  echo "Installing gum"
  sudo pacman -S --noconfirm gum
fi

TYPE=$(gum choose --no-limit "vim" "zsh" "tmux" "xorg" "i3")
grep -q "vim" <<< "$TYPE" && link_vim
grep -q "zsh" <<< "$TYPE" && link_zsh
grep -q "tmux" <<< "$TYPE" && link_tmux
grep -q "xorg" <<< "$TYPE" && link_xorg
grep -q "i3" <<< "$TYPE" && link_i3

echo "Done :)"
