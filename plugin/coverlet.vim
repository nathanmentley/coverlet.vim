" coverlet.vim
" A vim plugin to display coverlet code coverage info.
" Copyright 2020 Nathan Mentley

" variable defaults
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

" load python code
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

_coverlet = Coverlet(coverlet_file_name, fg_color, u_color, c_color)
EOF

" create vim functions for the python api
function! CoverletClear()
    python3 _coverlet.clear_highlights()
endfunction

function! CoverletRefresh()
    python3 _coverlet.refresh_coverlet()
endfunction

" refresh when entering a new buffer
 autocmd BufLeave * call CoverletClear()
 autocmd BufEnter * call CoverletRefresh()
