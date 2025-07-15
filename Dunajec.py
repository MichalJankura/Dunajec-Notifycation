import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import csv
import os
from dotenv import load_dotenv



# 1. Stiahnutie dát z SHMU
url = "https://www.shmu.sk/sk/?page=765&station_id=7950"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="dynamictable w600 center stripped")

first_row = table.find("tbody").find("tr")
cells = first_row.find_all("td")
data = [cell.get_text(strip=True) for cell in cells]

#message = f"Dátum: {data[0]}\nHladina: {data[1]} cm\nTeplota: {data[2]} °C"

# 2. Načítanie príjemcov z CSV
with open("prijemci.csv", "r") as file:
    reader = csv.reader(file)
    recipients = [row[0] for row in reader if row]

# 3. Nastavenie emailu
sprava = EmailMessage()
sprava["Subject"] = f"📢 Upozornenie: 🌊 Hladina Dunajca je {data[1]} cm!"
sprava["From"] = os.environ.get("GMAIL_USER")
sprava["To"] = ", ".join(recipients)
#sprava.set_content(message)

# 4. Odoslanie emailu
smtp_server = "smtp.gmail.com"
smtp_port = 587
load_dotenv()
your_email = os.environ.get("GMAIL_USER")
your_password = os.environ.get("GMAIL_PASSWORD")

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(your_email, your_password)
    server.send_message()

print("✅ Email odoslaný na adresy:", ", ".join(recipients))
