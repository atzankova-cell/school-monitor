import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

SCHOOLS = [
    "https://npmg.org",
    "https://www.smg.bg",
    "https://www.91ng.org",
    "https://www.1agebg.com",
    "https://2age.bg",
    "https://35su.bg",
    "https://73su.bg",
    "https://125su.bg",
    "https://7su.bg",
    "https://18su.bg",
    "https://22su.bg",
    "https://32su.bg",
    "https://ruo-sofia-grad.com"
]

KEYWORDS = [
    "свободни места",
    "9 клас",
    "IX клас",
    "преместване",
    "прием",
    "старши класове"
]

EMAIL = "a.tzankova@gmail.com"
PASSWORD = "nbpzzqbrrhlpxixz"
TO_EMAIL = "a.tzankova@gmail.com"


def send_email(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


def check_site(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        text = r.text.lower()

        for word in KEYWORDS:
            if word.lower() in text:
                return True, word, url

    except Exception as e:
        print(f"Error {url}: {e}")

    return False, None, url


def run_check():
    results = []

    for site in SCHOOLS:
        found, word, url = check_site(site)
        if found:
            results.append(f"🔔 Намерено: {word}\n{url}")

    if results:
        send_email(
            "School Monitor - нова обява",
            "\n\n".join(results)
        )


if __name__ == "__main__":
    run_check()
