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

set nocompatible
filetype off

" Install vim-plug if not found
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
endif

" Run PlugInstall if there are missing plugins
autocmd VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
  \| PlugInstall --sync | source $MYVIMRC
\| endif

call plug#begin()

Plug 'gabrielelana/vim-markdown'
Plug 'godlygeek/tabular'
Plug 'iamcco/markdown-preview.nvim', { 'do': { -> mkdp#util#install() }, 'for': ['markdown', 'vim-plug']}
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'zackhsi/fzf-tags'

call plug#end()

filetype plugin indent on

let g:markdown_include_jekyll_support = 1
let g:markdown_enable_folding = 0
let g:markdown_enable_conceal = 1
let g:markdown_enable_spell_checking = 0

let g:mkdp_auto_start = 1
let g:mkdp_auto_close = 1
let g:mkdp_port = "1234"


