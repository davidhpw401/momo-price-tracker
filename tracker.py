import re
import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage

URL = "https://www.momoshop.com.tw/product/13525646"

HEADERS = {
    "User-Agent":
    "Mozilla/5.0"
}

html = requests.get(URL, headers=HEADERS).text

soup = BeautifulSoup(html, "lxml")

text = soup.get_text(" ", strip=True)

discount = None

m = re.search(r'([0-9]{2})折', text)

if m:
    discount = int(m.group(1))

if discount is None:
    print("Couldn't find discount.")
    exit()

print("Current discount:", discount)

if discount <= 70:

    sender = os.environ["EMAIL"]
    password = os.environ["EMAIL_PASSWORD"]
    receiver = os.environ["TO_EMAIL"]

    msg = EmailMessage()
    msg["Subject"] = f"Momo Discount Alert! {discount}折"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content(
        f"The product is now {discount}折!\n\n{URL}"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(sender,password)
        smtp.send_message(msg)

    print("Alert sent!")

else:
    print("Not cheap enough.")
