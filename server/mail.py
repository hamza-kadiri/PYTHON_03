from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import User, Serie, Notification

DEFAULT_HOST = 'smtp.gmail.com'
DEFAULT_PORT = 465
DEFAULT_ADDRESS = "my.series.no.reply@gmail.com"
DEFAULT_PASSWORD = "test1234@"

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

def send_notifications(server: SMTP, notification:Notification):
    user = User.get_user_by_id(notification.user_id)

    msg = create_message(sender, recipient, subject, message)
    send_message(msg, server)


server = create_smtp_server(host, port, address, password)

