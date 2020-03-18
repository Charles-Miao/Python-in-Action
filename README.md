简单Python脚本收集
===

2016
---

[excel2sqlite](https://github.com/Charles-Miao/Python-in-Action/tree/master/excel2sqlite)，简化提案改善步骤
---

- **Excel2sqlite**，将提案改善excel数据导入sqlite中
- **SQLite2Excel**，将提案改善sqlite中的数据筛选并整理成excel文件

2017
---

[txt2excel](https://github.com/Charles-Miao/Python-in-Action/tree/master/txt2excel)，将txt log整理至excel中
---

- **handle_P_sensor_Log**，将p-sensor txt log整理转化为excel文件

- **handle_Asimov_test_log**，将Asimov测试log整理为excel

2018
---

[OfficeScan](https://github.com/Charles-Miao/Python-in-Action/tree/master/OfficeScan)，筛选excel数据
---

- **officescan**，从产线online电脑中挑选出未安装officescan的电脑


[SFCS Web Service](https://github.com/Charles-Miao/Python-in-Action/tree/master/WistronSFCS)，上抛SFCS
---

- 上抛SFCS可以使用zeep模块或者urllib模块，但是zeep模块更好用

- JSON数据交互格式比XML更好用

- 上抛NG时，修护需要定义ErrorCode和NG流程

2019
---

[Lean_Report_Auto](https://github.com/Charles-Miao/Python-in-Action/tree/master/Lean_Report_Auto),重构了自动生成lean report的脚本
---

- 使用pandas模块筛选Excel
- 使用pptx模块自动生成pptx

2020
---

[CheckComputer](https://github.com/Charles-Miao/Python-in-Action/tree/master/CheckComputer)，用python重构，主要可以实现如下功能：
---

- 检查电脑是否激活，若没有激活则自己激活一遍，并显示异常
- 检查电脑officescan病毒码版本是否和服务器类似，若不相同，则显示异常
- tool可以最小化到桌面右下角