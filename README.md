简单Python脚本收集
===

2025
---

[Remote](https://github.com/Charles-Miao/Python-in-Action/tree/master/remote)

- This was designed by David Ge, and used for remote server to execute command on agent pc and get result

[Zabbix_Agent](https://github.com/Charles-Miao/Python-in-Action/tree/master/Zabbix_Agent)

- 使用[syncFileServer](https://github.com/Charles-Miao/Batch-in-Action/tree/master/2025/syncFileServer)中的批处理脚本，同步文件服务器上的文件到备份服务器
- 使用[Zabbix_Agent](https://github.com/Charles-Miao/Python-in-Action/tree/master/Zabbix_Agent)中的python脚本和Zabbix工具，监控同步结果
- IT监控平台Zabbix添加Sync Files模板，此模板添加了一个Sync Files监控项，以及一个触发器（同步失败则触发）
- 主机JS2P-FS-SRV01，添加Sync Files模板
- IT维护Email媒介：SMTP服务器和发送邮件的电子邮件
- IT添加SWDL群组和用户，并添加Email报警媒介
- 添加一个触发器动作，当文件同步异常时透过Email发送给SWDL群组

2024
---

[log_to_xml](https://github.com/Charles-Miao/Python-in-Action/tree/master/log_to_xml)

- 实现方法.md：实现架构说明，以及 offline & online测试的问题点记录
- Config.ini：配置档用于定义原始log目录/Temp目录/EDA log 目录
- Log_to_xml.py：log转换xml主函数
- Empty_temp.py：清空目录函数
- Log_fit.py：筛选log函数
- Py_test_modify_V03.py：log 转化xml函数

2023
---

[CRL](https://github.com/Charles-Miao/Python-in-Action/tree/master/CRL)

- GetCRL，获取CRL文件，并将其上传到FTP上
- revoke_file，讀取需要注銷的SN信息，並透過API查詢CASN，最終將查詢的結果，以及revoke结果写入CSV文件

[get_CRL](https://github.com/Charles-Miao/Python-in-Action/tree/master/get_CRL)

- get_CRL，将CRL文件上传到FTP中，并发送邮件
- get_revoke_file，确认FTP文件中是否有需要revoke的文件，如果有则下载下来

2022
---

[AIS_Backup_Result](https://github.com/Charles-Miao/Python-in-Action/tree/master/AIS_Backup_Result)

- 用途：将AIS备份的log汇总成新的txt文本，并用mail发给AFTE，以方便了解产线程式同步的状况

[PRS_Monitor](https://github.com/Charles-Miao/Python-in-Action/tree/master/PRS_Monitor)

- 用途：将PRS视频文件的最新数据整理正csv文件，方便UI PATH处理原始数据

[SVN_weekly_report](https://github.com/Charles-Miao/Python-in-Action/tree/master/SVN_weekly_report)

- 用途：将SVN的log汇总成EXCEL文件，方便UI PATH定期发送邮件和展示SVN修改纪录

[Wallaby_Download_Fail_Monitor](https://github.com/Charles-Miao/Python-in-Action/tree/master/Wallaby_Download_Fail_Monitor)

- 用途：将wallaby测试生成的UI log中download fail的信息整理成CSV文件，并发送给RPA开发者，以便RPA整理成图表
- 优缺点：UI Path不适用处理小文件，故先使用python脚本先对log做个汇总，最后由UI Path做个展示

2021
---

[Auto_FTP](https://github.com/Charles-Miao/Python-in-Action/tree/master/Auto_FTP)

- 用途：将QCN文件上传到FTP中，同时纪录传输log，方便查询
- 优缺点：商用软件可以实现断点续传，但是没有一个好的log，这个脚本无法实现断点续传，传输小文件很不方便，断了需要重新运行
- 使用方法：先用商用软件完整传输一次，最后再用这个脚本运行纪录log

[rsync](https://github.com/Charles-Miao/Python-in-Action/tree/master/rsync)

- 用途：透过python脚本实现sersync功能，将Windows中测试log实时同步到NAS Server中，详细说明参见博客文章：[Windows实时同步文件至NAS](https://charles-miao.github.io/post/windows-rsync-realtime/)

[fixture_utilization](https://github.com/Charles-Miao/Python-in-Action/tree/master/fixture_utilization)

- 用途：用于计算RF设备稼动率
- 綫體（同一個儀器，count最多的綫體名）
- 站別（同一個儀器，count最多的站別名）
- 平均時間（時間排序，逐一遞減，剔除最大和最小的20%的數據，中間數值取平均）
- 上抛數量（同一個儀器，count所有上抛數據）
- 稼動率（最大的時間-最小的時間）/24hour

2020
---

[CheckComputer](https://github.com/Charles-Miao/Python-in-Action/tree/master/CheckComputer)

- 用途：用python重构，检查电脑激活和officescan状态
- 检查电脑是否激活，若没有激活则自己激活一遍，并显示异常
- 检查电脑officescan病毒码版本是否和服务器类似，若不相同，则显示异常
- tool可以最小化到桌面右下角

[filt_compress_log](https://github.com/Charles-Miao/Python-in-Action/tree/master/filt_compress_log)

- 用途：用于筛选和压缩文本log
- 将文本放到以修改日期为目录的文件内，并将此文件夹进行压缩
- 第二版使用多进程作业，加快了处理速度

[UI_log](https://github.com/Charles-Miao/Python-in-Action/tree/master/UI_log)

- 用途：透过ui log获取每个机台的测试时间

2019
---

[Lean_Report_Auto](https://github.com/Charles-Miao/Python-in-Action/tree/master/Lean_Report_Auto)

- 用途：重构了自动生成lean report的脚本
- 使用pandas模块筛选Excel
- 使用pptx模块自动生成pptx

2018
---

[OfficeScan](https://github.com/Charles-Miao/Python-in-Action/tree/master/OfficeScan)

- 用途：筛选excel数据
- officescan，从产线online电脑中挑选出未安装officescan的电脑

[SFCS Web Service](https://github.com/Charles-Miao/Python-in-Action/tree/master/WistronSFCS)

- 用途：用于和SFCS沟通
- 上抛SFCS可以使用zeep模块或者urllib模块，但是zeep模块更好用
- JSON数据交互格式比XML更好用
- 上抛NG时，修护需要定义ErrorCode和NG流程

2017
---

[txt2excel](https://github.com/Charles-Miao/Python-in-Action/tree/master/txt2excel)

- 用途：将txt log整理至excel中
- handle_P_sensor_Log，将p-sensor txt log整理转化为excel文件
- handle_Asimov_test_log，将Asimov测试log整理为excel

2016
---

[excel2sqlite](https://github.com/Charles-Miao/Python-in-Action/tree/master/excel2sqlite)

- 用途：简化提案改善步骤
- Excel2sqlite，将提案改善excel数据导入sqlite中
- SQLite2Excel，将提案改善sqlite中的数据筛选并整理成excel文件
