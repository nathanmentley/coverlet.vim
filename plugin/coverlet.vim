" coverlet.vim
" A vim plugin to display coverlet code coverage info.
" Copyright 2020 Nathan Mentley

" variable defaults if they're not set by the user
if !exists("g:coverlet_file_name")
    let g:coverlet_file_name="~/coverlet.json"
endif
if !exists("g:coverlet_foreground_color")
    let g:coverlet_foreground_color="black"
endif
if !exists("g:coverlet_uncovered_color")
    let g:coverlet_uncovered_color="red"
endif
if !exists("g:coverlet_covered_color")
    let g:coverlet_covered_color="green"
endif
if !exists("g:coverlet_branch_color")
    let g:coverlet_branch_color="yellow"
endif

" setup local variables
let s:coverlet_auto_display=0

" load and run the python code
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)

from coverlet import Coverlet

coverlet_file_name = vim.eval('g:coverlet_file_name')
fg_color = vim.eval('g:coverlet_foreground_color')
u_color = vim.eval('g:coverlet_uncovered_color')
c_color = vim.eval('g:coverlet_covered_color')
b_color = vim.eval('g:coverlet_branch_color')

_coverlet = Coverlet(coverlet_file_name, fg_color, u_color, c_color, b_color)
EOF

" local vim function
function! s:CoverletClearIfOn()
    if s:coverlet_auto_display
        python3 _coverlet.clear_highlights()
    endif
endfunction

function! s:CoverletRefreshIfOn()
    if s:coverlet_auto_display
        python3 _coverlet.refresh_coverlet()
    endif
endfunction

" hook into vim events
autocmd BufLeave * call s:CoverletClearIfOn()
autocmd BufWinLeave * call s:CoverletClearIfOn()
autocmd WinLeave * call s:CoverletClearIfOn()
autocmd TabLeave * call s:CoverletClearIfOn()
autocmd BufEnter * call s:CoverletRefreshIfOn()
autocmd BufWinEnter * call s:CoverletRefreshIfOn()
autocmd WinEnter * call s:CoverletRefreshIfOn()
autocmd TabEnter * call s:CoverletRefreshIfOn()

" Create public api global methods for the user to hit
function! g:CoverletToggle()
    if s:coverlet_auto_display
        python3 _coverlet.clear_highlights()
        let s:coverlet_auto_display = 0
    else
        python3 _coverlet.refresh_coverlet()
        let s:coverlet_auto_display = 1
    endif
endfunction

function! g:CoverletRefresh()
    if s:coverlet_auto_display
        python3 _coverlet.refresh_coverlet()
    endif
endfunction

function! g:CoverletList()
    if s:coverlet_auto_display
        python3 _coverlet.clear_highlights()
        let s:coverlet_auto_display = 0
    endif

    python3 _coverlet.display_coverage_info_buffer()
endfunction
