import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#设置登录及服务器信息
mail_host = '10.66.222.50'
sender = 'k000800@wistron.local'
receivers = ['Layla_Zhang@wistron.com','charles_miao@wistron.com']

#设置eamil信息
#添加一个MIMEmultipart类，处理正文及附件
message = MIMEMultipart()
message['From'] = sender

message['Subject'] = 'The List of newest PRS file'
#推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
content = '''
    <p>Hi, the attachment file is the list of newest PRS file.</p>
    <p>Best Regards!</p>
    <p>P5TE Server</p>
    '''
#设置html格式参数
part1 = MIMEText(content,'html','utf-8')
#添加一个csv文本附件
with open(r'D:\python_script\PRS_Monitor\prs.csv','r')as h:
    content2 = h.read()
#设置csv参数
part2 = MIMEText(content2,'plain','utf-8')
#附件设置内容类型，方便起见，设置为二进制流
part2['Content-Type'] = 'application/octet-stream'
#设置附件头，添加文件名
part2['Content-Disposition'] = 'attachment;filename="prs.csv"'

#将内容附加到邮件主体中
message.attach(part1)
message.attach(part2)

#登录并发送
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host,25)
    for index in range(len(receivers)):
        message['To'] = receivers[index]
    smtpObj.sendmail(sender,receivers,message.as_string())
    print('success')
    smtpObj.quit()
except smtplib.SMTPException as e:
    print('error',e)