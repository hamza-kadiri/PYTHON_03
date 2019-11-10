from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import time
from tmdb_api import get_tv_serie
from models import User, Serie, Notification
from flask import current_app as app

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


def send_notifications(server: SMTP, notification: Notification):
    user = User.get_user_by_id(notification.user_id)
    message = f'A new episode is going to be released for "{notification.serie_name}" on {notification.next_air_date}. Check our website for more info !'
    subject = f'Some news for "{notification.serie_name}"'
    msg = create_message(DEFAULT_ADDRESS, user.email, subject, message)
    send_message(msg, server)


def update_all_series():
    smtp_server = create_smtp_server(DEFAULT_HOST, DEFAULT_PORT, DEFAULT_ADDRESS, DEFAULT_PASSWORD)
    series = Serie.get_all_series()
    current_time = time()
    for serie in series:
        if serie.last_update < current_time - 24 * 3600:
            old_last_diff = serie.next_episode_air_date
            new_serie_json = get_tv_serie(serie.tmdb_id_serie)
            serie.update_from_json(new_serie_json)  # update serie information
            if old_last_diff != serie.next_episode_air_date and serie.next_episode_air_date != "null":
                for user in serie.users:
                    notif = Notification.create_from_serie(user.id, serie)  # create notification
                    send_notifications(smtp_server, notif)