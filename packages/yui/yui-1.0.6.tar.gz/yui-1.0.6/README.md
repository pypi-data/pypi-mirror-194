# Yui - personal task manager
Git based personal task manager.
100% command line.
(also, Japanese girl name)

> According to TDD as described in "Extreme Programming: Test Driven Development" by Kent Beck,
we need to start every day with blank sheet of paper, white down small tasks
and stroke out what is done. This is digital replacement for that paper sheets.

## Install
### Pip 3
```
pip3 install yui
```


## 4 dummies
 0. `yui` without arguments will display help

Workflow:
 1. Add task to the heap `yui create task name or short descriprion`
    1. Show tasks in heap `yui list heap`
 2. Pick the task to current day schedule `yui pick %taskId%` 
    1. Show tasks for current day `yui list cur`
 3. Open task in text editor  `yui open %taskId%`
    1. Task file is just md file with yaml header
    2. Adjust status in header
    3. Write any notes below
    4. Save
 4. When you done working, or before next day
    1. Move unfinished tasks back to heap `yui reset all`
    2. Archive tasks with status *done*  `yui archive today`
 5. View archive for specific date `yui list 2023-01-11`
 6. Run manual git command on task list `yui git %git_command% %git_command_args%`
 7. Adjust visible scope with `yui scope`
 
Optional configuration:
`.yui/config.yaml`
`.yui/projects/%projectName%.yaml`
 
## How it works
 1. There is git repository behind the scenes. So you have history and you can sync tasks using any git server. History, branches, etc.
    1. Create/pick/reset/archive commands will invoke `git add` + `git commit` commands automatically.
 2. Task data stored in plain text files.
    1. Format markdown(.md) with yaml header.
    2. You work with single task using plain text editor, like kate
 3. yui tool is used to organize and navigate .md files
 
## The method
### Step 1: Write it down and forget. 
Once you spot new task or idea - you just add it to the heap, and continue with your current work. So you stay focused.
```
yui create
```
*Heap* is the most chaotic, unorganised, unsorted, *backlog* you can imagine.
Do not waste your time on details, just stock pile it in the heap as is.

Imagine that you are working with paper stickers and you have a big box of chaotic notes written on stickers - that's the heap.
```
yui list heap
```
Will show you tasks in the heap in form of table
```
 id | context  | project    | name                                                                   | status
----|----------|------------|------------------------------------------------------------------------|-------
 7  | personal | yui        | show creation date column in task list                                 | new   
 15 | personal | yui        | sanitize slashes in task filename                                      | new
```
First column is *taskId* you will need it to manipulate the task

### Step 2: pick the task into daily plan
Pick all tasks you are planning to work with today. 
```
yui pick %taskId%
```
Will pick the task
```
yui list cur
```
Will display tasks for current day.

If you made a mistake, you can return the task back to heap
```
yui reset %taskId%
```

### Step 3: open the task in text editor
```
yui open %taskId%
```
### Step 4: change status to *work*
Adjust yaml header, simple replace `status: new` with `status: work`.

You can use any custom statuses, but buildin - *new*, *work*, *done* will be highlighted in `yui list` output.

### Step 5: Make notes while you are working on the task
As for it's just .md file, you can make any notes behind yaml header.

### Note: you can work with as many tasks at once as you want
That's just plain text files, after all.

### Step 6: change task status to *done*
In yaml header, replace `status: work` with `status: work`.

### Step 7: check your progress
```
yui list cur
```
Will get more green lines while you complete the tasks.

### Step 8: Cleanup workspace
```
yui reset all
```
Will return unfinished tasks back to the heap
```
yui archive today
```
Will move only *done* tasks to archive folder with current day. You can also use "yesterday" or specify date as "YYYY-MM-DD", or anything else recognized by php `strtotime()` function.

To view archived tasks use:
```
yui list YYYY-MM-DD
```

### Step 9: apply git
All git commands are mapped with `yui git`.

Most used:
    - `yui git log` history of changes in tasks
    - `yui git remote add origin %link%` link your task list with remote repository
    - `yui git push` save local changes to remote repository
    - `yui git pull` load fresh changes from remote repository
   
## Apllication working folder
Defaut:
 - Linux: `~/.yui`
 - Windows: `c:\Userts\%username%\AppData\yui`
Can be overwriten with `YUI_HOME` environment variable, like `YUI_HOME=mypath yui list heap`


## config.yaml
> Location: %application-working-folder%/config.yaml

Example:
```yaml
---
# % will be replaced with filename
# Examples:
#   To run gui editor: nohup kate % > /dev/null 2>&1 &
#   To run in terminal: mcedit %
# You can use nano, vi, mcedit etc
# If not specified, tsk will try EDITOR environment variable and then mcedit, nano, vim, vi, ee in that order
editor: nohup kate % > /dev/null 2>&1 &
---
```

## Project configuration
> Location: %application-working-folder%/projects/%projectName%.yaml

Example file:projects/myProject.yaml:
```yaml
---
# this will make YUI_PROJECT=myProject yui create test
# work the same way as YUI_PROJECT=myProject YUI_CONTEXT=myContext yui create test
defaultContext: myContext
---
```

## View archives
```
yui list_archives
```
Will display list of existing archives, from application working folder

To view tasks in single archive use
```
yui list %archiveName%
```

## Advanced options
You can pick range of items like so `pick 141,142,143..154`
