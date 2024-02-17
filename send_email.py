import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import requests
import json


def send_email_with_attachment(smtp_server, smtp_port, username, password, recipient, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path is not None:
    # Setup the attachment
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Attach the attachment to the MIMEMultipart object
        msg.attach(part)
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    text = msg.as_string()
    server.sendmail(username, recipient, text)
    server.quit()



def gemini_generate(text):
    url_gemini = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + YOUR_API_KEY
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        ]
    }
    response = requests.post(url_gemini, headers=headers, data=json.dumps(data))
    return response


import time
if __name__ == "__main__":
    # Use your own info here
    username = "545088576@qq.com"
    password = "dazeggjclhmibdcf"
    recipient = "zhuhuiqing13@163.com"
    smtp_server = "smtp.qq.com" # change this if you are not using Gmail
    smtp_port = 587 # change this if needed
    subject = "Hello! Greeting from 小哲同学"
    
    promot = f'''
    测试一下
    '''
    response = gemini_generate(promot)
    import pdb;pdb.set_trace()
    print(response.json())
    ai_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    text = f"今天是{time.strftime('%Y-%m-%d', time.localtime())}，{time.strftime('%A', time.localtime())}"
    body = text + '\n' + ai_response
    # attachment_path = "readme_summaries.txt"

    send_email_with_attachment(smtp_server, smtp_port, username, password, recipient, subject, body) 