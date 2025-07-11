import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import csv
import os



url = "https://www.shmu.sk/sk/?page=765&station_id=7950"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")
table = soup.find("table", class_="dynamictable w600 center stripped")

first_row = table.find("tbody").find("tr")
cells = first_row.find_all("td")
data = [cell.get_text(strip=True) for cell in cells]

message = f"Dátum: {data[0]} Hladina: {data[1]} Teplota: {data[2]}"
# print(message)

# Email configuration
with open("prijemci.csv","r") as file:
    reader = csv.reader(file)
    recipients = [row[0] for row in reader if row]  # Read email addresses from CSV

    sprava = EmailMessage()
    sprava["Subject"] = f"📢 Upozornenie: 🌊Hladina Dunajca je {data[1]} cm!"
    sprava["From"] = "noreplydunajec@gmail.com"
    sprava["To"] = recipients

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    your_email = os.getenv("GMAIL_USER")
    your_password = os.getenv("GMAIL_PASSWORD")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(your_email, your_password)
        server.send_message(sprava)

