import os
from send_mail2 import send_mail
from myFTP import myFtp

if __name__ == '__main__':
	mailto_list = ['charles_miao@wistron.com','joshua_su@wistron.com']
	mail_host = '10.66.222.50'
	mail_user = 'k000800@wistron.local'
	file_path=r'D:\python_script\get_CRL\CRL'
	attachments=os.listdir(file_path)
	localfolder=r'D:\python_script\get_CRL\CRL\LVR5-crl.crl'
		
	if os.path.exists(localfolder):
		#upload CRL to IT FTP
		ftp = myFtp('192.168.66.38')
		ftp.Login('WKS_TE_CRL', '8K21g93w')
		ftpfolder='/CRL'
		ftp.DeleteFiles(ftpfolder)
		ftp.uploadFile(localfolder,ftpfolder)
		ftp.close()
		#send mail to server administrator
		sub='Get CRL Success'
		content = '''
		<p>Server Administrators:</p>
		<p>TE Server has uploaded the CRL to the IT's FTP.</p>
		<p>You can check on ftp://192.168.66.38/CRL</p>
		<p>Account:WKS_TE_CRL</p>
		<p>Password:8K21g93w</p>
		<p>Best Regards!</p>
		<P>P5 FTP Server</p>
		'''
		send_mail(sub, content, attachments, file_path, mailto_list, mail_host, mail_user)
	else:
		#send mail to server administrator
		sub='Get CRL Failed'
		content = '''
		<p>Server Administrators:</p>
		<p>TE Server does not find the CRL file.</p>
		<p>So there is no way to upload it to IT's FTP.</p>
		<p>Can you help me check where is the problem?</p>
		<p>Best Regards!</p>
		<P>P5 FTP Server</p>
		'''
		send_mail(sub, content, attachments, file_path, mailto_list, mail_host, mail_user)