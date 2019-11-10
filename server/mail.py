from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_smtp_server(host: str, port: int, address: str, password: str):
    s = SMTP_SSL(host=host, port=port)
    s.login(address, password)
    return s


def create_message(sender: str, recipient: str, subject: str, message: str, is_html: bool = False):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html' if is_html else 'plain'))
    return msg


def send_message(message: MIMEMultipart, server: SMTP):
    server.send_message(message)


host = 'smtp.gmail.com'
port = 465
address = "my.series.no.reply@gmail.com"
password = "test1234@"
server = create_smtp_server(host, port, address, password)
sender = address
recipient = "edouard.benauw@student.ecp.fr"
subject = "TEST"
message = "BLABLABLA"
msg = create_message(sender, recipient, subject, message)
send_message(msg, server)
