" coverlet.vim
" A vim plugin to display coverlet code coverage info.
" Copyright 2020 Nathan Mentley

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
_coverlet = Coverlet()
EOF

" create vim functions for the python api
function! CoverletClear()
    python3 _coverlet.clear_highlights()
endfunction

function! CoverletRefresh()
    python3 _coverlet.refresh_coverlet()
endfunction
