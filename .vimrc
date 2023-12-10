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

let mapleader = ','

" Vundle
set nocompatible
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'gabrielelana/vim-markdown'
Plugin 'godlygeek/tabular'
Plugin 'iamcco/markdown-preview.nvim'
" call mkdp#util#install()

call vundle#end()
filetype plugin indent on

let g:markdown_include_jekyll_support = 1
let g:markdown_enable_folding = 0
let g:markdown_enable_conceal = 1
let g:markdown_enable_spell_checking = 0

let g:mkdp_auto_start = 1
let g:mkdp_auto_close = 1
