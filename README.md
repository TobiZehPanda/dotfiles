# ~ dotfiles ~

## Installation

```sh
  git pull
  git submodule --recursive --init or git submodules --recursive --remote
```
Then open .vimrc in VIM
```vim
  source %
  PluginInstall
  call mkdp#util#install()
```
