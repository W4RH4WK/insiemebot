import io
import re
import requests
import logging

from PyPDF2 import PdfFileReader
from datetime import datetime, date


MENU_URL = 'http://www.cafe-froschkoenig.at/wp-content/uploads/pdf/froschkoenig_woche.pdf'


def get_menu():

    logger.info("Getting FK Menu PDF")
    r = requests.get(MENU_URL)
    pdf = io.BytesIO()
    pdf.write(r.content)

    logger.info("Extracting Text")
    reader = PdfFileReader(pdf)
    page = reader.getPage(0)

    week = page.extractText()
    week = re.split('Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag', week)[1:]
    return [clean_day(x) for x in week]


def clean_day(day):
    day = re.sub("^[A-Z ]*$", "", day, flags=re.M)
    day = day.replace("\n", "")
    day = day.replace("Ł", "\n- ")
    day = day.replace("—", "")
    day = re.sub("  +", " ", day)
    day = day.strip()
    return day


def today():
    w = date.weekday(datetime.now())
    return get_menu()[w]
