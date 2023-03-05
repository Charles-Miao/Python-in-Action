import os
import re
import configparser

def revoke(tool,ip,casn,revoke_reason):
	command=tool+" -ip "+ip+" -action revoke -revoke_ca_sn "+casn+" -revoke_reason "+revoke_reason
	conent=os.popen(command).readlines()
	for index in range(len(conent)):
		if "post" in conent[index]:
			post=' '.join(re.split(r' ',conent[index])[2:]).strip()	
		if "response" in conent[index]:
			response=' '.join(re.split(r' ',conent[index])[2:]).strip()	
	return(post,response)
			
if __name__ == '__main__':
	config=configparser.ConfigParser()
	config.read(r'D:\CRL\Revoke\config.ini')
	tool=config.get("revoke","tool")
	ip=config.get("revoke","server_ip")
	
	print(revoke(tool,ip,"25","1")[0:])