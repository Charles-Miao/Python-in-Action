Excel to SQLite
===
模块一
---
[**Excel2SQLite.py**](https://github.com/Charles-Miao/SimpleScript-Python/tree/master/xlsx2sqlite/Excel2sqlite.py)

- createDataBase，创建DB Table（用于存储所有提案）
- createProposalTable，创建Table（用于存储提案部门为MEZ900的提案）
- createExecutorTable，创建Table（用于存储被提案部门为MEZ900的提案）
- readExcel，读取Excel的数据，并存入SQLite DB，若Excel值为空，则赋值为None，若Excel值为日期值，则转换格式再存储，注意事项，SQLite插入语句

模块二
---
[**SQLite2Excel.py**](https://github.com/Charles-Miao/SimpleScript-Python/tree/master/xlsx2sqlite/SQLite2Excel.py)

- createExcel，创建xls格式的EXCEL文件
- insertExcel，插入Excel表头
- 功能1：本月提案，并被厂长Approve（筛选DB，并插入Excel，需要转换日期格式以便判断）
- 功能2：本月有节省人力的提案（筛选DB，并插入Excel，需要转换日期格式以便判断）
- 功能3：正在进行中的提案（筛选DB，并插入Excel）
- 功能4：结案嘉奖提案（筛选DB，并插入Excel）
- 功能5：提案嘉奖提案（筛选DB，并插入Excel）

注意事项
---
- insert语句变量需要使用**"?"**代替

参考
---
[【知乎】一个关于用python进行数据筛选的问题？](https://www.zhihu.com/question/45504799)

**[【CNblogs】Python解析excel文件并存入sqlite数据库](http://www.cnblogs.com/ybjourney/p/5523878.html)**

[【CSDN】python 读取excel表格并写入sqllite数据库](http://blog.csdn.net/cyrabbit/article/details/7634686)

[【个人博客】用python导入Excel数据到Sqlite](http://blog.jonathan-li.cn/post/blog/2014-10-26-using-python-to-import-data-from-excel-to-sqlite)

**[【RUNOOB.COM】SQLite - Python](http://www.runoob.com/sqlite/sqlite-python.html)**

[【10条】Python批量Excel文件数据导入SQLite数据库的优化方案](http://www.10tiao.com/html/383/201702/2247484174/1.html)

**[【CNblogs】python操作excel表格(xlrd/xlwt)](http://www.cnblogs.com/zhoujie/p/python18.html)**