# ------------------------------
# Written by: Charles Miao
# Company: Wistron Corporation
# Date: 2024-10-25
# version:Python3.9
# ------------------------------
import shutil
import os
import configparser
import time

def empty_folder(folder):
    """
    清空文件夹。

    Args:
        folder (str): 需要清空的文件夹路径。

    Returns:
        None

    """
    try:
        shutil.rmtree(folder)
        # 如果需要确保操作系统有足够的时间来处理删除操作，可以加上sleep，但通常不必要
        # time.sleep(2.1) 
    except Exception as e:
        print(f"Error while deleting folder {folder}: {e}")
        return
    
    # 在创建文件夹之前检查文件夹是否存在，以避免FileExistsError
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        print(f"Folder {folder} already exists. Not creating again.")

if __name__ == '__main__':
	config=configparser.ConfigParser()
	config_file=os.getcwd()+"\config.ini"
	config.read(config_file)
	temp_folder=config.get("config","temp_folder")
	
	
	try:
		empty_folder(temp_folder)
	finally:
		if not os.listdir(temp_folder):
			print("temp folder is empty")
		else:
			print("temp folder is not empty")
	