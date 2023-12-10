# ~ dotfiles ~

## Installation

```sh
  git pull
  git submodule update --recursive --init or git submodules update --recursive --remote
```
Then open .vimrc in VIM
```vim
  source %
  PluginInstall
  call mkdp#util#install()
```
