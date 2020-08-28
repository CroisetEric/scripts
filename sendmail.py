import smtplib, ssl

port = 587
password = "ICT_81ct"
sender_email = "system@bict.ch"
receiver_email = "eric.croiset@bict.ch"
message = """\
Subject: Testing
This msg is sent from python."""

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
connection = smtplib.SMTP("82.195.237.188", port)
connection.ehlo()
connection.starttls(context=context)
connection.ehlo()
connection.login("system@bict.ch", password)
connection.sendmail(sender_email, receiver_email, message)




