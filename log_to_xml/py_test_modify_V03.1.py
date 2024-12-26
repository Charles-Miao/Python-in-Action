# ------------------------------
# Written by: Willson Chiang
# Modified by: Charles Miao
# Company: Wistron Corporation
# Date: 2024-10-12
# version:Python3.9
# 修改记录：
# 2024-10-24: 将原始脚本转换为函数，以便其他脚本调用 
# 2024-10-31: 将Willson修改的内容添加到最新脚本中，并完善determine_model_name函数，以便得到正确的ModelName
# 2024-11-06：加入获取Error信息的功能
# 2024-11-07: 加入获取DutSwVersion的功能
# 2024-11-09：修正MeasurementData Name=" EXT_MP_PMIC_AI_UG5V8 adc feedback at 6.5v""存在两个冒号，EDA系统无法正常解析的问题
# 2024-11-09: 修正XML文件名格式不正确问题，日期和时间需要“_”隔开
# 2024-11-14：修正CompType，单位是"boolean" "string" ""的CompType为LOG，其他如果上线相等则为EQ，上下限不相等则为GELE，其他为NA
# 2024-11-15：MeasurementData中添加LogTime
# 2024-11-15：修正测试FAIL时TestData中的TestTime不准确的问题
# 2024-12-04: 增加TV measurements的正则表达式
# 2024-12-05：修正MeasurementData Name中的特殊字符'&','<','>','"',"'"，弃用2024-11-09的修正方式
# 2024-12-09：修正ErrorFullTestName="TestData Name"+"_"+"MeasurementData Name"
# 2024-12-10：将所有测试item中的空格替换为"_"，测试无法解决top issue无法list的问题
# ------------------------------
import re
import os
import time  # Import time module for execution timing
from datetime import datetime, timezone, timedelta
from dateutil import parser # pip install python-dateutil

def convert_suptestname_string(input_str):
    """
    将 "Test XXX - XXX" 转换为 "Test ID XXX - XXX"
    
    :param input_str: 需要转换的字符串
    :return: 转换后的字符串
    """
    if input_str.startswith("Test "):
        parts = input_str.split(" ", 1)
        if len(parts) == 2:
            return f"Test ID {parts[1]}"
    return input_str

def escape_xml_special_chars(s):
    """
    Escape special XML characters in the input string.

    Args:
    s (str): The input string to be escaped.

    Returns:
    str: The escaped string.
    """
    special_chars = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }
    escaped_str = ''.join(special_chars.get(char, char) for char in s)
    return escaped_str

def convert_timestamp(timestamp_str):
    # 解析原始时间字符串
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
    
    # 设置时区为东八区（北京时间）
    tz = timezone(timedelta(hours=8))
    
    # 将时间转换为带时区的信息
    dt_with_tz = dt.replace(tzinfo=tz)
    
    # 格式化为所需的字符串格式，并去掉多余的微秒零
    formatted_timestamp = dt_with_tz.isoformat(timespec='milliseconds')
    
    return formatted_timestamp

# Define a function to format the date and add a timezone
def format_date_with_timezone(date_str):
    """Convert ISO date string to 'YYYY-MM-DDTHH:MM:SS.sss+08:00' format"""
    try:
        #dt = datetime.fromisoformat(date_str)  # Parse the original date string
        dt = parser.isoparse(date_str)
        formatted_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # Keep milliseconds up to 3 decimal places
        return formatted_date + "+08:00"  # Append the +08:00 timezone
    except ValueError:
        return date_str  # Return the original string if parsing fails

# Define a function to determine the ModelName
def determine_model_name(region_str):
    """Determine ModelName based on the region string"""
    if 'nperear' in region_str:
        return 'NPE_REAR'
    elif 'npefront' in region_str:
        return 'NPE_FRONT'
    elif 'niorear' in region_str or 'fct_rearfct' in region_str or 'fatp_reareol' in region_str or 'dsos_rear' in region_str or 'npdrear' in region_str:
        return 'NPD_REAR'
    elif 'niofront' in region_str or 'fct_frontfct' in region_str or 'fatp_fronteol' in region_str or 'dsos_front' in region_str or 'npdfront' in region_str:
        return 'NPD_FRONT'
    else:
        return 'NA'  # Default NA

# Define a function to convert time string to seconds
def convert_time_to_seconds(time_str):
    """Convert time string to seconds"""
    hours = minutes = seconds = 0
    match = re.search(r'(\d+)h', time_str)
    if match:
        hours = int(match.group(1))
    match = re.search(r'(\d+)m', time_str)
    if match:
        minutes = int(match.group(1))
    match = re.search(r'(\d+)s', time_str)
    if match:
        seconds = int(match.group(1))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def get_ship_version(log_content):
    lines = log_content.splitlines()
    check_ship_found = False
    for i, line in enumerate(lines):
        if "GUI Progress:  check Ship switch version" in line:
            check_ship_found = True
            # 在接下来的几行中查找“nioswtool - INFO”
            for j in range(i + 1, i + 21):
                if "Alive, info" in lines[j]:
                    match = re.search(r'Alive, info\s*:(.*)', lines[j])
                    if match:
                        info = match.group(1).strip()
                        return info
    if not check_ship_found:
        return None
    #return None

# 示例"20241105082202245147" 转换为 "2024-11-05_08-22-02"
def convert_time_format(time_str):
    year = time_str[:4]
    month = time_str[4:6]
    day = time_str[6:8]
    hour = time_str[8:10]
    minute = time_str[10:12]
    second = time_str[12:14]

    formatted_time = f"{year}-{month}-{day}_{hour}-{minute}-{second}"
    return formatted_time


def process_log_file(log_file_path,xml_file_path):
    # Open and read the content of the log file
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()  # Read the log content
    except FileNotFoundError:
        print(f"The file {log_file_path} does not exist. Please check the file path.")
        exit()

    # Parse the model name from the log file name
    try:
        log_file_name1 = os.path.split(log_file_path)[-1]  # Get the file name
        region_str = log_file_name1.split('_')[3]  # Extract the region part
        model_name = determine_model_name(log_file_name1)  # Determine the model name
        
        if not model_name:
            print(f"Cannot determine ModelName, file: {log_file_name1}")

    except Exception as e:
        print(f"Error while processing {log_file_path}: {e}")

    # Define regex patterns to match specific information in the log
    status_pattern = r"runner\s+-\s+INFO\s+-\s+Status:\s+(PASS|FAIL)"
    serial_number_pattern = r"runner\s+-\s+INFO\s+-\s+Serial\s+Number:\s+(\S+)"
    start_time_pattern = r"runner\s+-\s+INFO\s+-\s+Start\s+Time:\s+(\S+)"
    test_time_pattern = r"runner\s+-\s+INFO\s+-\s+Test\s+Time:\s+(\S+)"
    end_time_pattern = r"runner\s+-\s+INFO\s+-\s+End\s+Time:\s+(\S+)"
    computer_name_pattern = r"runner\s+-\s+INFO\s+-\s+Test\s+Station\s+Name:\s+(\S+)"
    update_mes_info_pattern = r"runner\s+-\s+INFO\s+-\s+update\s+mes\s+info:(\S+)(?:\s+(\S+))?(?:\s+(\S+))?(?:\s+(\S+))?(?:\s+(\S+))?"
    # version_pattern = r"NVOS_SW_VERSION\s+:\s+(v[\d.]+)"
    version_pattern = r"Build at\s+:\s+(\w+\s+\d+\s+\d{4},\s+\d{2}:\d{2}:\d{2})"
    test_data_pattern = r"runner\s+-\s+INFO\s+-\s+Test\s+(\d+)\s+-\s+([\w\-_.]+)\s+\(.*?\)\s+\.\.\.\s+(pass|fail)\s+\(([\dhms]+)\)"
    measurement_pattern = r"runner\s+-\s+INFO\s+-\s+teststep:(\S+)\s+testname:(.*?)\s+value:(\S+)\s+unit:(\S+)\s+judgetype:(\S+)\s+lowlimit:(\S+)\s+uplimit:(\S+)\s+datatype:(\S+)"
    errorcode_pattern = r'find errorcode\..*?errorcode:(\w+)'
    errormessage_pattern = r'ERROR - Failing test due to: (.*?):'
    errordetails_pattern = r'ERROR - Failing test due to: (.*)'
    #errortestname_pattern = r'find errorcode\. testname:(.*?) errorcode:'
    errortestname_pattern = r'INFO - Testname: (.*)'
    errorsuptestname_pattern = r'Failing test due to:(.*?)\n.*? - +INFO - (.*?)\(.*?\)'

    # Search for matches in the log content
    status_match = re.search(status_pattern, log_content)
    serial_number_match = re.search(serial_number_pattern, log_content)
    start_time_match = re.search(start_time_pattern, log_content)
    test_time_match = re.search(test_time_pattern, log_content)
    end_time_match = re.search(end_time_pattern, log_content)
    computer_name_match = re.search(computer_name_pattern, log_content)
    update_mes_info_match = re.search(update_mes_info_pattern, log_content)
    version_match = re.search(version_pattern, log_content)
    test_data_matches = re.findall(test_data_pattern, log_content)  # Match all test data lines
    measurement_matches = re.findall(measurement_pattern, log_content)  # Match all measurement data
    errorcode_match = re.search(errorcode_pattern, log_content)  # Match errorcode
    errormessage_match = re.search(errormessage_pattern, log_content)  # Match error message
    errordetails_match = re.search(errordetails_pattern, log_content)  # Match error details
    errortestname_match = re.search(errortestname_pattern, log_content)  # Match error testname
    errorsuptestname_match = re.search(errorsuptestname_pattern, log_content)


    # Extract the matched data, set to None if no match found
    status = status_match.group(1) if status_match else None
    serial_number = serial_number_match.group(1) if serial_number_match else None
    start_time = start_time_match.group(1) if start_time_match else None
    test_time = test_time_match.group(1) if test_time_match else None
    end_time = end_time_match.group(1) if end_time_match else None
    computer_name = computer_name_match.group(1) if computer_name_match else None
    
    #get DutSwVersion
    factory_version = version_match.group(1) if version_match else None
    shipping_version = get_ship_version(log_content)
    
    if factory_version is None and shipping_version is None:
        version_name = "NA"
    elif factory_version is not None and shipping_version is None:
        version_name = factory_version
    elif factory_version is None and shipping_version is not None:
        version_name = shipping_version
    else:
        version_name = factory_version +";"+ shipping_version

    # Error message
    errorcode=errorcode_match.group(1) if errorcode_match else ""
    errormessage=errormessage_match.group(1) if errormessage_match else ""
    errordetails=errordetails_match.group(1) if errordetails_match else ""
    errortestname=errortestname_match.group(1).replace(' ', '_') if errortestname_match else ""
    errorsuptestname=convert_suptestname_string(errorsuptestname_match.group(2)).strip().replace(' ', '_') if errorsuptestname_match else ""
    errorfulltestname=errorsuptestname+"_"+errortestname if errorsuptestname_match else ""


    # Process MES info
    unit_serial_number = update_mes_info_match.group(1) if update_mes_info_match else None
    station_line = update_mes_info_match.group(2) if update_mes_info_match and update_mes_info_match.group(2) else None
    station_type = update_mes_info_match.group(3) if update_mes_info_match and update_mes_info_match.group(3) else None
    station_id = update_mes_info_match.group(4) if update_mes_info_match and update_mes_info_match.group(4) else None
    user = update_mes_info_match.group(5) if update_mes_info_match and update_mes_info_match.group(5) else None

    try:
        # Generate XML file name based on file serial number and date
        log_file_name = os.path.split(log_file_path)[-1]
        log_datetime_str = log_file_name.split('_')[0]  # Date-time part
        unit_serial_number = log_file_name.split('_')[-1].replace('.log', '')  # Get the serial number part
        
        file_name = "{}_{}.xml".format(unit_serial_number, convert_time_format(log_datetime_str))  # Generate XML file name
        #file_name = "{}_{}.xml".format(log_datetime_str, unit_serial_number)  # Generate XML file name
        # print(f"Generated XML file name: {file_name}")

    except Exception as e:
        print(f"Error: {e}")

    # Start writing to the XML file
    with open(xml_file_path+"\\"+file_name, 'w', encoding='utf-8') as output_file:
        output_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        output_file.write("<?xml-stylesheet type='text/xsl' href='C:\\Wistron_TDC\\TDCXSL.xsl'?>\n")
        output_file.write("<TestResults>\n")
        
        # Overall test result block
        output_file.write("  <OverallResult>\n")
        output_file.write(f"    <Result>{'Pass' if status == 'PASS' else 'Fail'}</Result>\n")
        output_file.write(f"    <ErrorCode>{errorcode}</ErrorCode>\n")
        output_file.write(f"    <LogErrorMessage>{errormessage}</LogErrorMessage>\n")
        output_file.write(f"    <ErrorTestName>{errortestname}</ErrorTestName>\n")
        output_file.write(f"    <ErrorFullTestName>{errorfulltestname}</ErrorFullTestName>\n")
        output_file.write(f"    <ErrorDetails>{errordetails}</ErrorDetails>\n")
        output_file.write("  </OverallResult>\n")
        
        # Device info and test parameters
        output_file.write(f"  <UnitSerialNumber>{unit_serial_number}</UnitSerialNumber>\n")
        output_file.write(f"  <StartDate>{format_date_with_timezone(start_time)}</StartDate>\n")
        output_file.write(f"  <StopDate>{format_date_with_timezone(end_time)}</StopDate>\n")
        output_file.write(f"  <TestCycleTime>{test_time}</TestCycleTime>\n")
        output_file.write("  <MoNumber>NA</MoNumber>\n")
        output_file.write(f"  <ModelName>{model_name}</ModelName>\n")
        output_file.write("  <BOMVersion>NA</BOMVersion>\n")
        output_file.write(f"  <User>{user}</User>\n")
        output_file.write(f"  <ComputerName>{computer_name}</ComputerName>\n")
        output_file.write(f"  <StationType>{station_type}</StationType>\n")
        output_file.write(f"  <StationId>{station_id}</StationId>\n")
        output_file.write(f"  <StationLine>{station_line}</StationLine>\n")
        output_file.write("  <TestBundleVersion>NA</TestBundleVersion>\n")
        output_file.write(f"  <DutSwVersion>{version_name}</DutSwVersion>\n")
        output_file.write("  <FlowCheckResults>True</FlowCheckResults>\n")
        output_file.write("  <ProberUseTimes>0</ProberUseTimes>\n")
        output_file.write("  <CameraVideo>False</CameraVideo>\n")
        output_file.write("  <GRRTest>False</GRRTest>\n")
        output_file.write("  <StrainGageTest>False</StrainGageTest>\n")
        output_file.write("  <RFCableLoss>False</RFCableLoss>\n")
        output_file.write("  <CoFixtureTest>False</CoFixtureTest>\n")
        output_file.write("  <CameraCal>False</CameraCal>\n")
        output_file.write("  <AcousticCal>False</AcousticCal>\n")
        output_file.write("  <XMLVersion>V1.0.6</XMLVersion>\n")
        
        # Start writing the test data block
        output_file.write("  <TestDatas>\n")

        # Match the starting positions of all Test IDs
        test_pattern = r"runner\s+-\s+INFO\s+-\s+Test\s+(\d+)\s+-\s+Test\s+ID\s+\d+\s+-\s+(.*?)\s+"
        test_matches = list(re.finditer(test_pattern, log_content))
    
        # Confirm the number of matched Test IDs
        # print(f"Found {len(test_matches)} Test IDs.")

        # Iterate through each Test ID
        for i, match in enumerate(test_matches):
            test_id = match.group(1)  # Extract Test ID
            test_name = match.group(2)  # Extract Test name

            # Get the range of this Test ID
            start_pos = match.end()
            end_pos = test_matches[i + 1].start() if i + 1 < len(test_matches) else len(log_content)
            test_log_section = log_content[start_pos:end_pos]

            # Find test time, "fail" needs to be capitalized
            test_time_match = re.search(r"runner\s+-\s+INFO\s+-\s+Test\s+\d+\s+-\s+.*?\s+\.\.\.\s+(pass|FAIL|skip)\s+\(([\dhms]+)\)", test_log_section)
            test_time_str = "0h0m0s"  # Default to 0h0m0s
            test_status = "Fail"  # Default to Fail

            # Extract test status and time
            if test_time_match:
                status_keyword = test_time_match.group(1)
                test_time_str = test_time_match.group(2)
                if status_keyword == "pass":
                    test_status = "Pass"
                elif status_keyword == "fail":
                    test_status = "Fail"
                elif status_keyword == "error":
                    test_status = "Error"
                elif status_keyword == "skip":
                    test_status = "Skip"

            test_time_seconds = convert_time_to_seconds(test_time_str)
            test_item=("Test ID "+test_id+" - "+test_name).replace(' ', '_')

            # Write test data to XML
            output_file.write(f"    <TestData Name=\"{test_item}\" Status=\"{test_status}\" TestTime=\"{test_time_seconds}\">\n")
            output_file.write("      <Measurements>\n")

            # Match measurement data
            
            # measurements_pattern=r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+-\s+runner\s+-\s+INFO\s+-\s+teststep:(\S+)\s+testname:(.*?)\s+value:(\S+)\s+unit:(\S*)\s+judgetype:(\S+)\s+lowlimit:(\S*)\s+uplimit:(\S*)\s+datatype:(\S+)"
            # measurements_for_test = re.finditer(measurements_pattern,test_log_section)
            
            # 2023-09-17 11:05:39,772 -   runner -     INFO - teststep:TS8202.008015 testname:H Bridge J2600-1-25-27 forward value:True unit:boolean judgetype:judgetype.equal lowlimit:True uplimit:True datatype:datatypetype.boolean
            measurements_pattern_1=r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+-\s+runner\s+-\s+INFO\s+-\s+teststep:(\S+)\s+testname:(.*?)\s+value:(\S+)\s+unit:(\S*)\s+judgetype:(\S+)\s+lowlimit:(\S*)\s+uplimit:(\S*)\s+datatype:(\S+)"
            # 2024-12-04 10:05:34,608 - rack1 -  runner -     INFO - teststep:TS8202.000700 testname:check CM switch version value:True unit:boolean judgetype:judgetype.equal lowlimit:True uplimit:True datatype:datatypetype.boolean
            measurements_pattern_2=r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+-\s+\S+\s+-\s+runner\s+-\s+INFO\s+-\s+teststep:(\S+)\s+testname:(.*?)\s+value:(\S+)\s+unit:(\S*)\s+judgetype:(\S+)\s+lowlimit:(\S*)\s+uplimit:(\S*)\s+datatype:(\S+)"
            # 尝试使用第一个正则表达式
            measurements_for_test = list(re.finditer(measurements_pattern_1, test_log_section))
            # 如果第一个正则表达式没有匹配到内容，则使用第二个正则表达式
            if not measurements_for_test:
                measurements_for_test = list(re.finditer(measurements_pattern_2, test_log_section))

            found_measurements = False
            measurement_count = 0

            # Iterate through measurement data
            for measurement in measurements_for_test:
                found_measurements = True
                measurement_count += 1
                measurement_time = measurement.group(1)
                measurement_name = measurement.group(3)
                result = measurement.group(4)
                units = measurement.group(5)
                lowlimit = measurement.group(7).strip()
                uplimit = measurement.group(8).strip()
                datatype = measurement.group(9)
                #print(measurement_time,measurement_name,result,units,lowlimit,uplimit,datatype)

                # Determine measurement status
                if datatype == 'datatypetype.boolean':
                    status = 'Pass' if result == lowlimit == uplimit else 'Fail'
                else:
                    try:
                        if lowlimit and uplimit:
                            status = 'Pass' if float(lowlimit) <= float(result) <= float(uplimit) else 'Fail'
                        else:
                            status = 'Pass'
                    except ValueError:
                        status = 'Fail'

                # Determine CompType based on units and values
                if units in ['boolean', 'Boolean', 'boolen', 'string', '']:
                    comp_type = 'LOG'
                # 'unknown', 'digital', 'Hz', 's'如果上下限相等则为EQ
                elif units in ['unknown', 'g', 'A', 'ma', 'v', 'Hz', '%', 's', 'digital']:
                    try:
                        result_val = float(result)
                        lowlimit_val = float(lowlimit) if lowlimit else None
                        uplimit_val = float(uplimit) if uplimit else None

                        if lowlimit_val is not None and uplimit_val is not None:
                            if lowlimit_val == uplimit_val:
                                comp_type = 'EQ'
                            # elif result_val > lowlimit_val and result_val < uplimit_val:
                            #     comp_type = 'GTLT'
                            # elif result_val >= lowlimit_val and result_val <= uplimit_val:
                            #     comp_type = 'GELE'
                            else:
                                comp_type = 'GELE'
                        # elif uplimit_val is not None:
                        #     comp_type = 'EQ' if result_val == uplimit_val else 'NEQ'
                        else:
                            comp_type = 'NA'
                    except ValueError:
                        comp_type = 'NA'
                else:
                    comp_type = 'NA'

                # Write measurement data to XML
                output_file.write(f"        <MeasurementData Name=\"{escape_xml_special_chars(measurement_name).replace(' ', '_')}\" Status=\"{status}\" Result=\"{result}\" LowerLimit=\"{lowlimit}\" UpperLimit=\"{uplimit}\" Units=\"{units}\" CompType=\"{comp_type}\" LogCount=\"0\" LogTime=\"{convert_timestamp(measurement_time)}\"/>\n")

            if not found_measurements:
                output_file.write("        <!-- No matching measurements found -->\n")
                
            output_file.write("      </Measurements>\n")
            output_file.write("    </TestData>\n")

        output_file.write("  </TestDatas>\n")
        output_file.write("</TestResults>\n")
    
    print(f"File '{file_name}' has been successfully generated.")



if __name__ == "__main__":
    # Record the start time of the script
    start_time_exec = time.time()
    # Define the path of the log file
    log_file_path = r'C:\Users\Administrator\Desktop\EDA\Temp_Log\20241101211835915869_zone_fct_rearfct_NRNWXKH009C483.log'
    xml_file_path=r'C:\Users\Administrator\Desktop\EDA\XML_EDA'
    try:
        process_log_file(log_file_path,xml_file_path)
    except Exception as e:
        print(f"Error: {e}")
    # Record the end time of the script
    end_time_exec = time.time()
    # Calculate and print the script execution time
    execution_time = end_time_exec - start_time_exec
    print(f"Execution time: {execution_time:.2f} seconds")