import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import os



# 参数：收件人，主题，正文，文件名集合（可发送多个文件），文件路径（文件在同一个路径）
def send_mail(sub, content, files, path, mailto_list, mail_host, mail_user):
    me = sub + "<" + mail_user + ">"
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ",".join(mailto_list)  # 将收件人列表以‘,’分隔
    for file in files:
        if os.path.isfile(path + '/' + file):
            # 构造附件
            att = MIMEText(open(path + '/' + file, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att.add_header("Content-Disposition", "attachment", filename=("gbk", "", file))
            msg.attach(att)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host,25)
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        print('Mail sent successfully')
        return True
    except Exception as e:
        print('Mail sent failed')
        print(sys.exc_info()[0], sys.exc_info()[1])
        return False

if __name__ == '__main__':
    mailto_list = ['charles_miao@wistron.com']  # 收件人列表，以英文逗号分隔
    mail_host = '10.66.222.50'  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
    mail_user = 'k000800@wistron.local'  # 用户名
    file_path=r'D:\python_script\get_CRL\revoke_file'
    files=os.listdir(file_path)
    sub='Revoke Files'
    content = '''
    <p>Dear Sir Or Madam:</p>
    <p>These devices in the attachment need to be revoked.</p>
    <p>Could you confirm it, thanks!</p>
    <p>Best Regards!</p>
    '''
    send_mail(sub, content, files, file_path, mailto_list, mail_host, mail_user)  # 发送file_path文件夹下面的文件