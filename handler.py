import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from variables import sender
from variables import token
from variables import password

def hello(event, context):
    body = {
        'message': 'Lambda is working.',
    }
    response = {'statusCode': 200, 'body': json.dumps(body)}
    return response

def send_mail(event, context):
    if 'authorization' not in event['headers']:
        return {'statusCode': 403, 'body': 'Not authorized.'}
    auth = event['headers']['authorization']
    if auth != token:
        return {'statusCode': 403, 'body': 'Not authorized.'}

    if not event['body']:
        return {'statusCode': 400, 'body': 'Data incomplete.'}
    body = json.loads(event['body'])
    if 'receiver' not in body or 'subject' not in body or 'message' not in body:
        return {'statusCode': 400, 'body': 'Data incomplete.'}
    sender_email = sender
    receiver_email = body['receiver']

    message = MIMEMultipart('alternative')
    message['Subject'] = body['subject']
    message['From'] = sender_email
    message['To'] = receiver_email

    html ="""
    <html>
        <body>
        <div style="font-family: Roboto, sans-serif;text-align: center;background-color: #eeeeee">
            <div style="width: 500px;margin:0px auto;">
                <div style="padding-bottom: 1rem;padding-top: 1rem;width: 37.5rem;">
                    <a href="https://genxapp.co"><img style="display: flex;justify-content: center;width: 10rem;" src="cid:logo"></a>
                </div>
                <div style="font-size:14px;background: #fff;border: 1px solid #181f39;border-radius: 13px; text-align:justify;padding: 1rem;">
                    <div style="text-align:center;">
                        <h2>{}</h2>
                    </div>
                    <div style="padding-botton: 1rem;">{}</div>
                </div>
                <div style="margin-top: 2rem;padding-bottom: 2rem;width: 37.5rem;font-weight: 200;text-align: center;font-size: 12px;color: #706a7c;">
                <div>
                    <a href=""><img src="cid:fb" style="padding: 0.5rem;"></a>
                    <a href=""><img src="cid:linkedin" style="padding: 0.5rem;width: 22px;"></a>
                    <a href=""><img src="cid:twitter" style="padding: 0.5rem;"></a>
                </div>
                <a style="color: #181f39;font-weight: 600;text-decoration: none;" href=""></a><br>
                Colombia
                </div>
            </div>
        </div>
        </body>
    </html>
    """.format(body['subject'], body['message'])
    part = MIMEText(html, 'html')
    message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    response = {'statusCode': 200, 'body': 'Email sended successfully'}

    return response
