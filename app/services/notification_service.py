import asyncio
import smtplib
from email.mime.text import MIMEText
from typing import List
from app.models.patient import Patient
from abc import ABC, abstractmethod
from settings import settings

class Notifier(ABC):
    @abstractmethod
    async def send(self, patient: Patient):
        pass

message = "Patient created successfully!"

class EmailNotifier:
    async def send(self, recipient: Patient, message: str):
        msg = MIMEText(message)
        msg["Subject"] = "Patient Registration Confirmation"
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = recipient.email_address

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_email, recipient.email_address, msg)

    def _send_email(self, recipient: str, msg: MIMEText):
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.esmtp_features['auth'] = 'LOGIN PLAIN'
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, recipient, msg.as_string())

class SMSNotifier:
    async def send(self, patient: Patient, message: str):
        print("SMS Notifier not ready yet.")

class NotificationService:
    def __init__(self):
        self.notifiers = {
            "email": EmailNotifier(),
            "sms": SMSNotifier(),
        }

    async def send(self, patient: Patient, channels: List[str]):
        tasks = []
        for channel in channels:
            notifier = self.notifiers.get(channel)
            if notifier:
                tasks.append(notifier.send(patient, message))
        await asyncio.gather(*tasks)

notification_service = NotificationService()

def get_notification_service():
    return notification_service