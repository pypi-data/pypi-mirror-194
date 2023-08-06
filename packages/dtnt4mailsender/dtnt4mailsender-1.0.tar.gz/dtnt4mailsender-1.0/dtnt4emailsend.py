#!/usr/bin/python3
# dtnt4emailsend.py
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:

    def __init__(self, sender, password):
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587
        self.EMAIL_FROM = sender
        self.EMAIL_FROM_PSWD = password

    def create_message(self, body, file, subject):
        # Make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = self.EMAIL_FROM
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        text = file

        # Open the file in python as a binary
        with open(text, 'rb') as attachment:  # r for read and b for binary

            # Encode as base 64
            attachment_package = MIMEBase('application', 'octet-strem')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition',
                                         "attachment; filename=" + text)
            msg.attach(attachment_package)

        return msg

    def send_emails(self, EMAIL_TO, body, file, subject):
        for person in EMAIL_TO:
            msg = self.create_message(body, file, subject)
            msg['To'] = person

            # Cast as string
            text = msg.as_string()

            # Connect with the server
            print("Connecting to server...")
            TIE_server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            TIE_server.starttls()
            TIE_server.login(self.EMAIL_FROM, self.EMAIL_FROM_PSWD)
            print("Successfully connected to server")
            print()
            # Send emails to "person" as list is iterated
            print(f"Sending email to: {person}...")
            TIE_server.sendmail(self.EMAIL_FROM, person, text)
            print(f"Email sent to: {person}")
            print()
        TIE_server.quit()

