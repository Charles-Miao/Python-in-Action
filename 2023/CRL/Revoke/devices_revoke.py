import configparser
from process_csv import CsvFile
from http_request import MyAPI
from revoke import revoke

if __name__=='__main__':
    #初始化api相關的值
    api=MyAPI(
       username="CIMAPI",
       password="123456",
       token_url="http://172.30.40.118:9999/cimapi/gettoken",
       api_url="http://172.30.40.118:9999/CIMAPI/DynamicInterfaceORA"
    )
    api_data={"SYSTEM": "SFCFA","ACTION": "GET","FUNCTIONNAME": "FUNC_GETCAMSN","PLANT":"F232","sss":"123" }
    #初始化csv文件
    source_file = CsvFile('devices_revoke_list.csv')
    destination_file = CsvFile('cacn_revoke_list.csv')
    #read ini config
    config=configparser.ConfigParser()
    config.read(r'D:\CRL\Revoke\config.ini')
    tool=config.get("revoke","tool")
    ip=config.get("revoke","server_ip")
    #讀取需要注銷的SN信息，並透過API查詢CASN，最終將查詢的結果and revoke result write into CSV文件
    source_data = source_file.read()
    destination_data=[]
    destination_data.append(["sn","CASN","revoke_reason","post","response"])
    for i in range(len(source_data)):
        if source_data[i][0]=="sn":
            pass
        else:
            #更新api查詢data中的SN信息
            api_data["sss"]=source_data[i][0]
            #透過API查詢CASN值
            CASN=api.call_api(data=api_data)['CAMUSN']
            #revoke the devices
            revoke_result=revoke(tool,ip,CASN,source_data[i][1])
            #將SN，CASN，revoke reason,revoke result寫入數組
            destination_data.append([source_data[i][0],CASN,source_data[i][1],revoke_result[0],revoke_result[1]])
    destination_file.write(destination_data)
