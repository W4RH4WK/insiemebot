import io
import re
import requests
import logging

from PyPDF2 import PdfFileReader
from datetime import datetime, date


MENU_URL = 'http://www.cafe-froschkoenig.at/wp-content/uploads/pdf/froschkoenig_woche.pdf'


def get_weekdays():
    return ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def get_pdf_text():
    logging.info("Getting FK Menu PDF")
    r = requests.get(MENU_URL)
    pdf = io.BytesIO()
    pdf.write(r.content)

    logging.info("Extracting Text")
    reader = PdfFileReader(pdf)
    page = reader.getPage(0)

    return page.extractText()


def get_menu():
    week = get_pdf_text()
    week = clean_week(week)
    day_re = "|".join(get_weekdays())
    week = re.split(day_re, week)[1:]
    return [clean_day(x) for x in week]


def clean_week(week):
    #week = re.sub("^[A-Z ]*$", "", week, flags=re.M)
    week = week.replace("\n", "")
    return week


def clean_day(day):
    day = day.strip()
    day = day.replace("Ł", "\n- ")
    day = re.sub("[A-Z]{2,}", "", day)
    day = re.sub(" +", " ", day)
    #day = day.replace("—", "")
    return day


def today():
    w = date.weekday(datetime.now())
    return get_menu()[w]
