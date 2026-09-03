import csv
import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "birthdays.csv")


def send_telegram(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, data=data, timeout=30)

    print("Telegram response:", response.text)

    if response.ok:
        print("Telegram message sent successfully")
    else:
        print("Telegram error:", response.text)


today = datetime.now(ZoneInfo("Asia/Kolkata"))

print("Today:", today.strftime("%d.%m.%Y"))

with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["Name"].strip()
        dob = row["DOB"].strip()
        chat_id = row["TelegramChatID"].strip()

        try:
            birthday = datetime.strptime(dob, "%d.%m.%Y")
        except ValueError:
            print(f"Invalid DOB for {name}: {dob}")
            continue

        if birthday.day == today.day and birthday.month == today.month:
            print(f"Birthday found: {name}")
            print(f"Chat ID: {chat_id}")

            message = (
                f"🎂 Happy Birthday, {name}! 🎉\n\n"
                f"Wishing you a very Happy Birthday!\n"
                f"May your day be filled with happiness, "
                f"success and wonderful moments. 🎁🎈"
            )

            send_telegram(chat_id, message)

        else:
            print(f"No birthday today for {name}")
