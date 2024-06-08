set shiftwidth=2
set tabstop=2
set softtabstop=2
set expandtab
set nobackup
set incsearch
set ignorecase
set smartcase
set showmatch
set hlsearch
set backupcopy=yes
syntax enable

" Install vim-plug if not found
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
endif

" Run PlugInstall if there are missing plugins
autocmd VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
  \| PlugInstall --sync | source $MYVIMRC
\| endif

let g:polyglot_disabled = ['autoindent', 'markdown']
let g:python_recommended_style = 0
autocmd BufEnter *.py colorscheme base16-3024
autocmd BufEnter *.py highlight Normal guibg=NONE ctermbg=NONE
autocmd FileType python setlocal shiftwidth=2 tabstop=2 softtabstop=2 expandtab

call plug#begin()

Plug 'gabrielelana/vim-markdown'
Plug 'godlygeek/tabular'
Plug 'iamcco/markdown-preview.nvim', { 'do': { -> mkdp#util#install() }, 'for': ['markdown', 'vim-plug']}
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'junegunn/rainbow_parentheses.vim'
Plug 'junegunn/vim-easy-align'
Plug 'zackhsi/fzf-tags'
Plug 'markonm/traces.vim'
Plug 'bounceme/poppy.vim'
Plug 'ap/vim-css-color'
Plug 'dense-analysis/ale'
Plug 'rust-lang/rust.vim'
Plug 'rust-lang/rustfmt'
Plug 'rust-lang/rust-analyzer'
Plug 'rust-lang/rust-clippy'
Plug 'cespare/vim-toml'
Plug 'Yggdroot/indentLine'
Plug 'mattn/emmet-vim'
Plug 'vim-airline/vim-airline'
Plug 'prettier/vim-prettier', { 'do': 'yarn install --frozen-lockfile --production' }
Plug 'majutsushi/tagbar'
Plug 'universal-ctags/ctags'
Plug 'rstacruz/vim-closer'
Plug 'tpope/vim-commentary'
Plug 'catppuccin/vim', { 'as': 'catppuccin' }
Plug 'rsaraf/vim-advanced-lint'
Plug 'sheerun/vim-polyglot'
Plug 'chriskempson/base16-vim'

call plug#end()

set nocompatible
set completeopt=menu,menuone,preview,noselect,noinsert
filetype plugin indent on

nnoremap <silent> <C-f> :Files<CR>

let g:markdown_include_jekyll_support = 1
let g:markdown_enable_folding = 0
let g:markdown_enable_conceal = 1
let g:markdown_enable_spell_checking = 0

let g:mkdp_auto_start = 0
let g:mkdp_auto_close = 1
let g:mkdp_port = "1234"

let g:ale_set_signs = 0
let g:all_completion_enabled = 1
let g:ale_linters = { 'rust': ['analyzer', 'cargo'], 'c': 'all' }
let g:ale_fixers = { 'rust': ['rustfmt', 'trim_whitespace', 'remove_trailing_lines'] }
let b:ale_linters = 'all'

let g:rustfmt_autosave = 1
let g:rust_recommended_style = 0

let g:airline_theme = 'catppuccin_mocha'

au! cursormoved * call PoppyInit()

xmap ga <Plug>(EasyAlign)
nmap ga <Plug>(EasyAlign)
nmap <F8> :TagbarToggle<CR>
map ; :Files<CR>

colorscheme catppuccin_mocha
autocmd ColorScheme * highlight Normal guibg=NONE ctermbg=NONE

hi SpellBad cterm=underline ctermfg=red ctermbg=NONE
hi ALEWarning cterm=underline ctermfg=red ctermbg=NONE
