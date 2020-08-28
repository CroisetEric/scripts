#!/usr/bin/env python3
import os, smtplib, ssl

hostname = "192.168.60.5"
response = os.system("ping -c 1 " + hostname)

if response == 0:
	message = "Subject: NPLUS1 Server " + hostname + " ist erreichbar!"
	port = 587
	password = "ICT_81ct"
	sender_email = "system@bict.ch"
	receiver_email = "eric.croiset@bict.ch"
	context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	connection = smtplib.SMTP("82.195.237.188", port)
	connection.starttls(context=context)
	connection.login("system@bict.ch", password)
	connection.sendmail(sender_email, receiver_email, message)
else:
	message = "Subject: NPLUS1 Server " + hostname + " ist nicht erreichbar!"
	port = 587
	password = "ICT_81ct"
	sender_email = "system@bict.ch"
	receiver_email = "eric.croiset@bict.ch"
	context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	connection = smtplib.SMTP("82.195.237.188", port)
	connection.starttls(context=context)
	connection.login("system@bict.ch", password)
	connection.sendmail(sender_email, receiver_email, message)
