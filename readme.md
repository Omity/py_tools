# 仓库描述
此仓库旨在制作一些程序员方便的小工具, 目前仍旧存在很多的bug, 但是大体上可以使用, 希望  
能够有大神指导加入一些好的想法
## 仓库使用
使用*git clone*进行代码复制并提交想法, 然后发起*pull request*
### 代码提交
* 本仓库有自动提交版本, 提交时需要提交到*release*分支
* 开发版本请提交到*develop*分支
### 一些工具
* *git_push* 可用于提交代码到*release*分支进行版本发布, 只需要修改其中的COMMIT_INFO
* *git_test* 可用于提交到*develop*分支进行自动化测试
### **注意事项**
* 在提交*release*版本时, 请注意版本号, 不要低于当前发布版本, 不然虽然能够发布, 但实际运行的版本  
  会低于最新版本