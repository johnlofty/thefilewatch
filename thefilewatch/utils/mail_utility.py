import smtplib
from email.message import EmailMessage

def send_email(host, port, username, password, from_addr, to_addr, subject, content):
    smtp = smtplib.SMTP_SSL(host, port)
    smtp.login(user=username, password = password)
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr)
    msg.set_content(content)
    result = stmp.send_messages(msg, from_addr, to_addr)
    smtp.quit()
    return result





