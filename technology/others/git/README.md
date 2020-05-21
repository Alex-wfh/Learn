# Git 命令小记

* git rebase    直接覆盖的merge

* git rebase -i    交互式变基

  * reward    修改提交信息
  * edit    修改此提交
  * squash    将提交融合到前一个提交中
  * fixup    将提交融合到前一个提交中，不保留该提交的日志信息
  * exec    每个提交上运行指定的rebase命令
  * drop    移除该提交

* git reset    撤回未commit的内容

  git reset —soft    软重置，将HEAD移至指定的提交，而不会移除该提交之后的修改

  git reset —hard    硬重置，将HEAD移至指定的提交，并移除该提交之后的修改

* git revert    还原，撤销某次提交的修改

* git cherry-pick    拣选，拣选特定的提交合入当前分钟

* git fetch    取回，下载远程分支，= git pull - git merge

* git reflog    展示已经执行过的所有动作的日志，并支持许多修改操作

- git clone

- git log
- git merge
  - fast-forward
  - no-fast-forward

* git pull
* git add
* git commit 
* git push
* git diff
* git stash