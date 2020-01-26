coverlet.vim
============

A simple vim plugin to display coverlet line coverage in vim.

## Installation

### Plugin

coverlet.vim can be install using most vim plugin managers.

An example using:

https://github.com/junegunn/vim-plug

```
call plug#begin('~/.vim/plugged')
Plug 'nathanmentley/coverlet.vim'
call plug#end()
```

### Global Variables

#### g:coverlet\_file\_name

*Required* - This value must be set for the plugin to function correctly.

Setting g:coverlet\_file\_name will tell coverlet.vim where to read the coverlet json file from. This setting should probably be setup per project.

#### g:coverlet\_foreground\_color

*Optional*

Setting g:coverlet\_foreground\_color will allow you to override the font color for any highlighted text.

#### g:coverlet\_uncovered\_color

*Optional*

Setting g:coverlet\_uncovered\_color will allow you to override the background color for any text that is highlighted because it's uncovered by a unit test.

#### g:coverlet\_covered\_color

*Optional*

Setting g:coverlet\_covered\_color will allow you to override the background color for any text that is highlighted because it's covered by a unit test.

#### g:coverlet\_branch\_color

*Optional*

Setting g:coverlet\_branch\_color will allow you to override the background color for any text that is highlighted because it's a branch that isn't full covered by unit tests.

### Global Functions

#### CoverletToggle()

Chances are you won't want to always display which code is covered and which code isn't. Calling CoverletToggle() will enable and disable the code coverage display. It's recommended to bind that to a key command.

#### CoverletRefresh()

Right now this plugin wont detect changes to the json file and automatically update the coverage information. If you've updated the coverlet file. You should run CoverletRefresh() to update what vim is showing.

#### CoverletList()

Opens an immutable buffer with a list of uncovered lines and uncovered branches.

### Example Setup

```

call plug#begin('~/.vim/plugged')

Plug 'nathanmentley/coverlet.vim'

call plug#end()

let g:coverlet_file_name = "/Users/nathanmentley/Projects/coverlet_tests/coverage.json"
let g:coverlet_foreground_color = "233"
let g:coverlet_uncovered_color = "209"
let g:coverlet_covered_color = "50"
let g:coverlet_branch_color = "222"

nmap <S-t> :call CoverletToggle()<CR>
nmap <S-u> :call CoverletList()<CR>
nmap <S-y> :call CoverletRefresh()<CR>
```

With this configuration you can press Shift-T to enable or disable coverlet.vim, and you can press Shift-U to refresh the data if it's displaying an old test run.

## Usage

This plugin requires a coverlet json file to function. This plugin doesn't help call coverlet or generate that file. You'll need to either setup vim shortcuts to do that for your project or run coverlet outside of vim.
