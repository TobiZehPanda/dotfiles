#!/bin/bash

pwd=$(pwd)

if_exists () {
    if [ -f "$1" ]; then
        rm "$1"
    elif [ -L "$1" ]; then
	rm "$1"
    fi
}

if_exists ~/.zshrc
ln -s $pwd/.zshrc ~/.zshrc

if_exists ~/.vimrc
ln -s $pwd/.vimrc ~/.vimrc

if_exists ~/.config/i3/config
ln -s $pwd/.config/i3/config ~/.config/i3/config

if_exists ~/.config/i3status/config
ln -s $pwd/.config/i3status/config ~/.config/i3status/config

if_exists ~/.Xresources
ln -s $pwd/.Xresources ~/.Xresources

if_exists ~/.Xdefaults
ln -s $pwd/.Xresources ~/.Xdefaults
