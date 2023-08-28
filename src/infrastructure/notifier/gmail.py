import os
import smtplib
import dataclasses
from email.mime.text import MIMEText
from src.application.dto import NotifyPassengerDTO

@dataclasses.dataclass
class Creds:
    gmail: str
    password: str

@dataclasses.dataclass
class Letter:
    title: str
    html_path: str

class GmailNotifier:
    def __init__(self, creds: Creds, letter: Letter):
        if not self.is_valid_template_path(letter.html_path):
            return
        
        with open(os.path.join("", os.path.normpath(letter.html_path)), "r", encoding="utf-8") as file:
            self.letter_html = file.read()

        self.title = letter.title
        self.creds = creds

    def notify(self, data: NotifyPassengerDTO):
        message = self.generate_letter(
            data.passenger.gmail,
            data.passenger.full_name,
            data.payment_id
        )

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.creds.gmail, self.creds.password)
        server.sendmail(self.creds.gmail, [data.passenger.gmail], message)
        server.quit()

    def generate_letter(self, to: str, full_name: str, payment_id: str):
        body = self.letter_html.replace("PASSENGER_FULL_NAME", full_name)
        body = body.replace("PAYMENT_ID", payment_id)

        message = MIMEText(body, "html", "utf-8")
        message["Subject"] = self.title
        message["From"] = self.creds.gmail
        message["To"] = to
        
        return message.as_string()

    def is_valid_template_path(self, path: str):
        return path.endswith(".html") or path.endswith(".htm")
