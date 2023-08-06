import time
import datetime
import pyotp

totp = pyotp.TOTP('base32secret3232', interval=121)
token = totp.now()
time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
print(time_remaining)
