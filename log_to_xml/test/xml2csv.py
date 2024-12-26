import os
import re
import csv
from lxml import etree

def xml_to_csv(xml_file_path, csv_file_path):
    for filename in os.listdir(xml_file_path):
        filename_split=re.split(r'[_.]',filename)
        SN=filename_split[0]
        test_time=filename_split[1]+"_"+filename_split[2]

        file_path=xml_file_path+'\%s' %filename
        
        # 解析XML文件
        tree = etree.parse(file_path)
        root = tree.getroot()

        # 提取基本信息
        result = root.xpath('//Result/text()')[0]
        # unit_serial_number = root.xpath('//UnitSerialNumber/text()')[0]
        # start_date = root.xpath('//StartDate/text()')[0]
        model_name = root.xpath('//ModelName/text()')[0]
        station_type = root.xpath('//StationType/text()')[0]

        # 提取测试数据
        test_data_list = []
        for test_data in root.xpath('//TestData'):
            test_data_name = test_data.attrib['Name']
            test_data_status = test_data.attrib['Status']
            test_data_time = test_data.attrib['TestTime']
            
            for measurement in test_data.xpath('.//MeasurementData'):
                measurement_name = measurement.attrib['Name']
                measurement_status = measurement.attrib['Status']
                measurement_result = measurement.attrib['Result']
                measurement_lower_limit = measurement.attrib['LowerLimit']
                measurement_upper_limit = measurement.attrib['UpperLimit']
                measurement_units = measurement.attrib['Units']
                measurement_comptype = measurement.attrib['CompType']
                measurement_logtime = measurement.attrib['LogTime']
                
                
                test_data_list.append({
                    # 'Result': result,
                    # 'UnitSerialNumber': unit_serial_number,
                    # 'StartDate': start_date,
                    # 'ModelName': model_name,
                    # 'StationType': station_type,
                    'TestName': test_data_name,
                    'TestStatus': test_data_status,
                    'TestTime': test_data_time,
                    'MeasurementName': measurement_name,
                    'MeasurementStatus': measurement_status,
                    'MeasurementResult': measurement_result,
                    'LowerLimit': measurement_lower_limit,
                    'UpperLimit': measurement_upper_limit,
                    'Units': measurement_units,
                    'CompType': measurement_comptype,
                    'LogTime': measurement_logtime
                })
        
        # 写入CSV文件
        with open(csv_file_path+"\\"+test_time+"_"+SN+"_"+model_name+"_"+station_type+"_"+result+".csv", mode='w', newline='', encoding='utf-8') as file:
            if test_data_list:
                writer = csv.DictWriter(file, fieldnames=test_data_list[0].keys())
                writer.writeheader()
                writer.writerows(test_data_list)
            else:
                print("Warning: test_data_list is empty, no data to write to "+test_time+"_"+SN+"_"+model_name+"_"+station_type+"_"+result+".csv")

        # print(f'CSV file has been created successfully')

if __name__ == "__main__":
    # 示例调用
    xml_file_path = r'C:\Users\Administrator\Desktop\EDA\XML_EDA'
    csv_file_path = r'C:\Users\Administrator\Desktop\CSV_Log'
    # if os.path.exists(csv_file_path):
    #     os.remove(csv_file_path)
    xml_to_csv(xml_file_path, csv_file_path)