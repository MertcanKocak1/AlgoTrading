import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self):
        self.password = "--"
        self.sender_email = "inuxe99@gmail.com"
        self.receiver_email = "inuxe06@gmail.com"

    def sendEmail(self, message1):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = "ALERT"
        message["Bcc"] = self.receiver_email  # Recommended for mass emails
        body = message1
        # Add body to email
        message.attach(MIMEText(body, "plain"))

        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, text)
