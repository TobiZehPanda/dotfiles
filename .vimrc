set shiftwidth=2
set tabstop=2
set expandtab
set nobackup
set incsearch
set ignorecase
set smartcase
set showmatch
set hlsearch
syntax enable

" Vundle
set nocompatible
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'godlygeek/tabular'
Plugin 'preservim/vim-markdown'

call vundle#end()
filetype plugin indent on

let g:vim_markdown_folding_disabled = 1
