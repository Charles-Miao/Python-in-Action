简单Python脚本收集
===

txt2excel
---

**handle_P_sensor_Log**，将p-sensor txt log整理转化为excel文件

**handle_Asimov_test_log**，将Asimov测试log整理为excel

excel2sqlite
---

**Excel2sqlite**，将提案改善excel数据导入sqlite中
**SQLite2Excel**，将提案改善sqlite中的数据筛选并整理成excel文件

OfficeScan
---

**officescan**，从产线online电脑中挑选出未安装officescan的电脑


SFCS Web Service
---

- 上抛SFCS可以使用zeep模块或者urllib模块，但是zeep模块更好用

- JSON数据交互格式比XML更好用

- 上抛NG时，修护需要定义ErrorCode和NG流程
