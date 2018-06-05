set nocompatible
filetype off

" set the runtime path to include Vundle
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'gmarik/Vundle.vim'

" Add all additional Plugins here.
Plugin 'tmhedberg/SimpylFold'
Plugin 'vim-scripts/indentpython.vim'
Plugin 'scrooloose/syntastic'
Plugin 'nvie/vim-flake8'
Plugin 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}
Plugin 'scrooloose/nerdtree'

" Fortran options
let fortran_free_source=1
let fortran_do_enddo=1
filetype plugin indent on
set ruler

" Make vim echo commands as they are being entered
set showcmd

" Make Python code look nice.
let python_highlight_all=1
syntax on

" Enable folding
set foldmethod=indent
set foldlevel=99
nnoremap <space> za

" See docstrings for folded code.
let g:SimpylFold_docstring_preview=1

" UTF8 Support
set encoding=utf-8

" Line numbering
set nu

" Syntax.
syntax enable
set tabstop=4
set softtabstop=4
set smarttab
set expandtab
set cursorline

" Color scheme
colorscheme badwolf 
