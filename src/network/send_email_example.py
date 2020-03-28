import smtplib
import logging
from email.message import Message
from smtplib import SMTPServerDisconnected as ServerDisconnectedError
from smtplib import SMTPAuthenticationError as AuthError

# -------------------------------------------------------------------

server = smtplib.SMTP('smtp.gmail.com', port=587)

server.starttls()

# Input your email & password
try:
    server.login("kevoemail@gmail.com", "password")
except (ServerDisconnectedError, AuthError) as e:
    logging.exception("Authentication Error - Invalid username or password!")
    # exit()

from_address = "randomjunkemailaddress@nowhere.com"
to_list = ["kevotest@live.com"]
message = "Test Message from Kevin"

message = '''\\
From: Me@my.org
Subject: testing...

This is a test '''

# email, receiver..
server.sendmail(from_addr=from_address, to_addrs=to_list, msg=message)

# IMPORTANT
server.quit()
