from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import time
from tmdb_api import get_tv_serie
from models import User, Serie, Notification


def init_mailing_context(app):
    MailingContext.init_mailing_context(app)


class MailingContext:
    __has_been_initialized = False
    __mailing_host = None
    __mailing_port = None
    __mailing_address = None
    __mailing_password = None

    @classmethod
    def init_mailing_context(cls, app):
        try:
            cls.__has_been_initialized = True
            cls.__mailing_host = app.config['MAILING_HOST']
            cls.__mailing_port = app.config['MAILING_PORT']
            cls.__mailing_address = app.config['MAILING_ADDRESS']
            cls.__mailing_password = app.config['MAILING_PASSWORD']
        except RuntimeError:
            raise AttributeError(
                "Cannot instantiate MailingContext without a proper app configuration")

    @classmethod
    def get_mailing_host(cls):
        if not cls.__has_been_initialized:
            raise AttributeError("Mailing Context not initialized")
        return cls.__mailing_host

    @classmethod
    def get_mailing_port(cls):
        if not cls.__has_been_initialized:
            raise AttributeError("Mailing Context not initialized")
        return cls.__mailing_port

    @classmethod
    def get_mailing_address(cls):
        if not cls.__has_been_initialized:
            raise AttributeError("Mailing Context not initialized")
        return cls.__mailing_address

    @classmethod
    def get_mailing_password(cls):
        if not cls.__has_been_initialized:
            raise AttributeError("Mailing Context not initialized")
        return cls.__mailing_password


class MailingServer:

    def __init__(self, host: str = MailingContext.get_mailing_host(), port: int = MailingContext.get_mailing_port(),
                 address: str = MailingContext.get_mailing_address(),
                 password: str = MailingContext.get_mailing_password()):
        self.__host = host
        self.__port = port
        self.__address = address
        self.__password = password
        self.__smtp_server = MailingServer.create_smtp_server(host, port, address, password)

    @staticmethod
    def create_smtp_server(host: str, port: int, address: str, password: str):
        s = SMTP_SSL(host=host, port=port)
        s.login(address, password)
        return s

    @staticmethod
    def create_message(sender: str, recipient: str, subject: str, message: str, is_html: bool = False):
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html' if is_html else 'plain'))
        return msg

    def send_message(self, message: MIMEMultipart):
        self.__smtp_server.send_message(message)

    def send_notification(self, notification: Notification, sent_from: str = MailingContext.get_mailing_address()):
        user = User.get_user_by_id(notification.user_id)
        message = f'A new episode is going to be released for "{notification.serie_name}" on {notification.next_air_date}. Check our website for more info !'
        subject = f'Some news for "{notification.serie_name}"'
        msg = MailingServer.create_message(sent_from, user.email, subject, message)
        self.send_message(msg)

    @staticmethod
    def update_all_series():
        mailing_server = MailingServer()
        series = Serie.get_all_series()
        for serie in series:
            old_last_diff = serie.next_episode_air_date
            new_serie_json = get_tv_serie(serie.tmdb_id_serie)
            serie.update_from_json(new_serie_json)  # update serie information
            if old_last_diff != serie.next_episode_air_date and serie.next_episode_air_date != "null":
                for user in serie.users:
                    try:
                        notif = Notification.create_from_serie(user.id,
                                                               serie)  # create notification, Might rise a value error
                        mailing_server.send_notification(notif)
                    except ValueError:
                        pass
