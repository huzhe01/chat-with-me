from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_email_with_attachment(smtp_server, smtp_port, username, password, recipient, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = _format_addr('Python爱好者 <%s>' % username)
    msg['To'] = _format_addr('管理员 <%s>' % recipient)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Attach file
    filename = os.path.basename(attachment_path)
    attachment = open(attachment_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)
    server.login(username, password)
    server.sendmail(username, [recipient], msg.as_string())
    server.quit()

# Use your own info here
smtp_server = "smtp.qq.com"
smtp_port = 587  # Use port 25 for SMTP
username = input('From: ')
password = input('Password: ')
recipient = input('To: ')
subject = "Subject"
body = "Body text"
attachment_path = "readme_summaries.txt"

send_email_with_attachment(smtp_server, smtp_port, username, password, recipient, subject, body, attachment_path)
