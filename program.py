#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
import xmltodict
import urllib.request
import subprocess
import database
from difflib import SequenceMatcher
import urllib.request
import time

global id
import os

os.remove("data.db")
id = 0
connection = database.connect()
database.create_tables(connection)
lis_names = []
lis_description = []
lis_oneplusone = []
lis_price = []
lis_point = []
lis_city = []
lis_link = []
lis_discount = []
city_list = ["אופקים", "כנרת", "אור יהודה", "הרי הגליל", "אור עקיבא", "אילת", "אלעד", "אריאל", "אשדוד", "אשקלון",
             "באר שבע", "בית שאן", "בית שמש", "ביתר עילית", "בני ברק", "בת ים", "גבעת שמואל", "גבעתיים", "דימונה",
             "הוד השרון", "הרצליה", "חדרה", "חולון", "חיפה", "טבריה", "טירת כרמל", "יבנה", "יהוד-מונוסון", "יקנעם",
             "ירושלים", "כפר סבא", "כרמיאל", "לוד", "מגדל העמק", "מודיעין עילית", "מודיעין-מכבים-רעות", "מעלה אדומים",
             "מעלות-תרשיחא", "נהריה", "נס ציונה", "נצרת עילית", "נשר", "נתיבות", "נתניה", "עכו", "עפולה", "ערד",
             "פתח תקווה", "צפת", "קריית אונו", "קריית אתא", "קריית ביאליק", "קריית גת", "קריית ים", "קריית מוצקין",
             "קריית מלאכי", "קריית שמונה", "ראש העין", "ראשון לציון", "רחובות", "רמלה", "רמת גן", "רמת השרון", "רעננה",
             "שדרות", "תל אביב", "אבן יהודה", "אורנית", "אזור", "אליכין", "אלפי מנשה", "אלקנה", "אפרת", "באר יעקב",
             "בית אל", "בית אריה-עופרים", "בית דגן", "בני עיש", "בנימינה-גבעת עדה", "גבעת זאב", "גדרה", "גן יבנה",
             "גני תקווה", "הר אדר", "זכרון יעקב", "חצור הגלילית", "יבנאל", "יסוד המעלה", "ירוחם", "כוכב יאיר-צור יגאל",
             "כפר ורדים", "כפר יונה", "כפר שמריהו", "כפר תבור", "להבים", "מבשרת ציון", "מזכרת בתיה", "מטולה", "מיתר",
             "מעלה אפרים", "מצפה רמון", "סביון", "עומר", "עמנואל", "עתלית", "פרדס חנה-כרכור", "פרדסיה", "קדומים",
             "קדימה-צורן", "קציר-חריש", "קצרין", "קריית ארבע", "קריית טבעון", "קריית יערים", "קריית עקרון",
             "קרני שומרון", "ראש פינה", "רכסים", "רמת ישי", "שוהם", "שלומי", "תל מונד", "אביאל", "אביבים", "אביגדור",
             "אביחיל", "אביטל", "אביעזר", "אבן מנחם", "אבן ספיר", "אבני איתן", "אדירים", "אדרת", "אודים", "אודם",
             "אוהד", "אומץ", "אורה", "אורות", "אחוזם", "אחיהוד", "אחיטוב", "אחיסמך", "אחיעזר", "אילניה", "איתן",
             "אלוני אבא", "אלוני הבשן", "אליעד", "אליפלט", "אלישיב", "אלישמע", "אלמגור", "אלקוש", "אמונים", "אמירים",
             "אמנון", "אמציה", "אניעם", "ארבל", "ארגמן", "אשבול", "אשתאול", "באר טוביה", "באר מילכה", "בארותיים",
             "בוסתן הגליל", "בורגתה", "בטחה", "ביצרון", "בית אלעזרי", "בית גמליאל", "בית הגדי", "בית הלוי", "בית הלל",
             "בית זייד", "בית זית", "בית חלקיה", "בית חנן", "בית חנניה", "בית חרות", "בית יהושע", "בית יוסף",
             "בית ינאי", "בית יצחק", "בית יתיר", "בית לחם הגלילית", "בית מאיר", "בית נחמיה", "בית נקופה", "בית עובד",
             "בית עוזיאל", "בית עזרא", "בית עריף", "בית שקמה", "בית שערים", "ביתן אהרן", "בלפוריה", "בן זכאי", "בן עמי",
             "בן שמן", "בני דרום", "בני דרור", "בני עטרות", "בני ציון", "בני ראם", "בניה", "בצרה", "בצת", "בקוע",
             "בקעות", "בר גיורא", "ברוש", "ברכיה", "ברק", "ברקת", "בת שלמה", "גאולי תימן", "גאולים", "גאליה",
             "גבע כרמל", "גבעולים", "גבעת חן", "גבעת יואב", "גבעת יערים", "גבעת ישעיהו", "גבעת כח", "גבעת נילי",
             "גבעת שפירא", "גבעתי", "גבתון", "גדיש", "גורן", "גיאה", "גילת", "גיתית", "גמזו", "גן הדרום", "גן השומרון",
             "גן חיים", "גן יאשיה", "גן שורק", "גנות", "גני יוחנן", "גני עם", "גנתון", "גפן", "גת רימון", "דבורה",
             "דובב", "דור", "דישון", "דלתון", "דקל", "הבונים", "הדר עם", "הודיה", "הזורעים", "היוגב", "ורד יריחו",
             "זבדיאל", "זוהר", "זיתן", "זכריה", "זמרת", "זנוח", "זרועה", "זרחיה", "זרעית", "חבצלת השרון", "חגור",
             "חדיד", "חוגלה", "חוסן", "חזון", "חיבת ציון", "חלץ", "חמרה", "חניאל", "חצב", "חצבה", "חרב לאת", "חרות",
             "טירת יהודה", "טל שחר", "טפחות", "יבול", "יגל", "יד השמונה", "יד נתן", "יד רמבם", "יובל", "יודפת", "יונתן",
             "יושיביה", "ייטב", "יכיני", "ינוב", "ינון", "יסודות", "יעד", "יערה", "יפית", "יציץ", "ירדנה", "ירחיב",
             "ירקונה", "ישע", "ישעי", "ישרש", "יתד", "כוכב מיכאל", "כחל", "כמהין", "כנף", "כסלון", "כפר אביב",
             "כפר אוריה", "כפר אחים", "כפר ביאליק", "כפר בילו", "כפר בן נון", "כפר ברוך", "כפר גדעון", "כפר דניאל",
             "כפר הנגיד", "כפר הס", "כפר הראה", "כפר הריף", "כפר ויתקין", "כפר ורבורג", "כפר זיתים", "כפר חושן",
             "כפר חיטים", "כפר חיים", "כפר חסידים", "כפר טרומן", "כפר ידידיה", "כפר יהושע", "כפר יחזקאל", "כפר יעבץ",
             "כפר מונש", "כפר מימון", "כפר מלל", "כפר מעש", "כפר מרדכי", "כפר נטר", "כפר סירקין", "כפר פינס", "כפר קיש",
             "כפר רות", "כפר שמאי", "כפר שמואל", "כרם בן זמרה", "כרם מהרל", "כרמל", "לוזית", "לימן", "לכיש", "לפידות",
             "מאור", "מבוא ביתר", "מבטחים", "מבקיעים", "מגדים", "מגן שאול", "מגשימים", "מדרך עוז", "מזור", "מחולה",
             "מחסיה", "מטע", "מי עמי", "מיטב", "מירון", "מישר", "מכורה", "מכמורת", "מלאה", "מלילות", "מנוחה", "מנות",
             "מסילת ציון", "מעון", "מעונה", "מעלה גמלא", "מצליח", "מרגליות", "משגב דב", "משואות יצחק",
             "משמר איילון", "משמר הירדן", "משמר השבעה", "משמרת", "משען", "נאות גולן", "נאות הכיכר", "נבטים", "נהורה",
             "נהלל", "נוב", "נוגה", "נווה אטיב", "נווה אילן", "נווה ימין", "נווה ירק", "נווה מבטח", "נווה מיכאל",
             "נועם", "נורדיה", "נחושה", "נחלה", "נחלים", "נחם", "נטועה", "נטעים", "ניצני עוז", "ניר בנים", "ניר גלים",
             "ניר חן", "ניר ישראל", "ניר משה", "ניר עציון", "ניר עקיבא", "ניר צבי", "נס הרים", "נעמי", "נתיב הגדוד",
             "נתיב העשרה", "נתיב השיירה", "סגולה", "סלעית", "סתריה", "עבדון", "עגור", "עדנים", "עוזה", "עולש", "עופר",
             "עזריאל", "עזריה", "עזריקם", "עידן", "עין אילה", "עין הבשור", "עין ורד", "עין חצבה", "עין יהב", "עין יעקב",
             "עין עירון", "עין שריד", "עין תמר", "עוצם", "עלמה", "עמינדב", "עמיעוז", "עמיקם", "עמקה", "ערוגות", "פארן",
             "פדויים", "פדיה", "פורת", "פטיש", "פצאל", "פעמי תשז", "פקיעין החדשה", "פרזון", "פרי גן", "פתחיה", "צופית",
             "צופר", "צור משה", "צור נתן", "צוריאל", "ציפורי", "צלפון", "צפריה", "צפרירים", "צרופה", "קדמת צבי",
             "קדרון", "קוממיות", "קלחים", "קשת", "רגבה", "רווחה", "רוויה", "רועי", "רחוב", "ריחן", "רינתיה", "רם און",
             "רמות", "רמות מאיר", "רמות נפתלי", "רמת מגשימים", "רמת צבי", "רמת רזיאל", "רנן", "רשפון", "שאר ישוב",
             "שבי ציון", "שדה אילן", "שדה אליעזר", "שדה דוד", "שדה ורבורג", "שדה יעקב", "שדה יצחק", "שדה משה",
             "שדה ניצן", "שדה עוזיהו", "שדה צבי", "שדות מיכה", "שדי אברהם", "שדי חמד", "שדי תרומות", "שדמה",
             "שדמות דבורה", "שדמות מחולה", "שואבה", "שובה", "שומרה", "שוקדה", "שורש", "שזור", "שחר", "שיבולים", "שילת",
             "שלווה", "שעל", "שער אפרים", "שפיר", "שפר", "שקף", "שרונה", "שרשרת", "שתולה", "שתולים", "תאשור", "תדהר",
             "תומר", "תימורים", "תירוש", "תל עדשים", "תלמי אליהו", "תלמי אלעזר", "תלמי בילו", "תלמי יוסף", "תלמי יחיאל",
             "תלמי יפה", "תלמים", "תנובות", "תעוז", "תפרח", "תקומה", "חוף האלמוג הדרומי", "ים המלח", "תרום", "בית זרע",
             "רמת ים", "קיבוץ געש", "גן השלושה", "קרית גת", "ניר דוד"]


def getcallinks():
    url = 'https://www.cal-store.co.il/productlist.php?cid=3FCFD54E-1165-495E-A750-1A48F94FDBB0'
    req = urllib.request.Request(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"})
    # req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")

    startbit = 'https://www.cal-store.co.il'
    links = []
    for link in soup.findAll('a'):
        thislink = str(link.get('href'))
        if thislink.startswith('/product.php'):
            links.append(startbit + thislink)

    url = 'https://www.cal-store.co.il/productlist.php?cid=E0D0497C-B57D-46C8-BE0D-A2BB89306D0F'
    req = urllib.request.Request(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"})
    # req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")

    startbit = 'https://www.cal-store.co.il'
    for link in soup.findAll('a'):
        thislink = str(link.get('href'))
        if thislink.startswith('/product.php'):
            links.append(startbit + thislink)
    del links[1::2]
    return links

def getcallinks2():
    url = 'https://benefits.isracard.co.il/parentcategories/attractions/'
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "htmly.parser")

    startbit = 'https://www.cal-store.co.il/'
    links = []
    for link in soup.findAll('a'):
        thislink = str(link.get('href'))
        if thislink.startswith('product.php'):
            links.append(startbit + thislink)

    return links




def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def nospecial(text):
    text = re.sub("[^a-zA-Z0-9]+", "", text)
    return text

def nospecial2(text):
    text = re.sub("[^0-9]+", "", text)
    return text

def geturl2(base_url, url_link):
    subprocess.call(
        ['curl', 'https://www.leumi.co.il/sitemap_xml/LeumiHebrew/sitemap-benefit.xml', '-o', 'sitemap-benefit.xml'])
    f = open("sitemap-benefit.xml", "r")
    content = f.read()
    data = xmltodict.parse(content)
    numberentries = len(data['urlset']['url'])
    url = []
    for i in range(numberentries):
        data2 = data['urlset']['url'][i]['loc']
        if url_link in data2:
            url.append(str(data2))
    return url


def geturl3():
    subprocess.call(['curl', 'https://cpnclub.co.il/sitemap.xml', '-o', 'sitemap.xml'])
    f = open("sitemap.xml", "r", encoding='utf-8')
    content = f.read()
    data = xmltodict.parse(content)
    numberentries = len(data['documents']['url'])
    url = []
    for i in range(numberentries):
        data2 = data['documents']['url'][i]['loc']
        if "https://cpnclub.co.il/supplier/" in data2:
            url.append(str(data2))
    return url


def geturl(base_url, url_link):
    response = requests.get(base_url)
    data = xmltodict.parse(response.content)
    numberentries = len(data['urlset']['url'])
    url = []
    for i in range(numberentries):
        data2 = data['urlset']['url'][i]['loc']
        if url_link in data2:
            url.append(str(data2))
    return url

some_num=0
def getinfo(url, content_info, name_info, subname_info):
    global some_num
    some_num=some_num+1
    if some_num%100==0:
        time.sleep(10)
        print("waiting...")
    time.sleep(0.05)
    element = ""
    des = ""
    results_names = ""
    results_description = ""
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    try:
        urllib.request.urlopen(req)
    except:
        return "","","",""
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    for link in soup.find_all("div", class_=content_info):
        element = link
        name = link.find(name_info)
        if str(name) not in results_names:
            results_names = cleanme(name)
        subname = link.find(subname_info)
        if str(subname) not in results_description:
            results_description = cleanme(subname)
        des = str(element)
    if element == "":
        return "", "", "", ""
    return element, des, results_names, results_description


def cleanme(html):
    html = str(html)
    soup = BeautifulSoup(html)  # create a new bs4 object from the html data loaded
    for script in soup(["script"]):
        script.extract()
    text = soup.get_text()
    return text


def getname(i):
    i = i.replace("\n", "")
    i = i.strip()
    return i


def getdescription(i):
    i = i.replace("\n", "")
    i = i.strip()
    return i


def info_description(i):
    if "1+1" in i:
        oneplusone = 1
        i = i.replace("1+1", "")
    else:
        oneplusone = 0
    if "₪" in i or "שח" in i or 'ש"ח' in i:
        r=6
        i=i.strip()
        a=i.find("₪")
        if a<6:
            r=a
        i = i[a - r:a].strip()
        i=i.replace("₪","")
        i=i.replace("ב-","       ")
        i = i.replace("ב -", "     ")
        i = i.replace("מ-", "     ")
        i = i.replace("מ -", "     ")
        i = i.replace("ב", "     ")
        i = i.replace("מ", "     ")
        #print(i[:39])
        price=i.strip()
        #price=i[a-6:a].strip()

    else:
        price = 0
    if "תמורת פינוק" in i:
        point = "1"
    else:
        point = ""
    if "הנחת יחיד" in i:
        discount = 1
    else:
        discount = 0
    return oneplusone, price, point, discount


def getcity(city, results_names, results_description, des):
    if "סניפי הרשת" in des:
        result_city = "all"
    else:
        exit = False
        while exit == False:
            for t in city:
                if t in str(results_names):
                    start_index = str(results_names).find(t)
                    last_index = start_index + len(t)
                    if (str(results_names)[last_index:(last_index + 1)]).isalpha() == False:
                        if len(t) == (last_index - start_index):
                            result_city = t
                            exit = True
                            break

                if t in str(results_description):
                    start_index = str(results_description).find(t)
                    last_index = start_index + len(t)
                    if (str(results_description)[last_index:(last_index + 1)]).isalpha() == False:
                        if len(t) == (last_index - start_index):
                            result_city = t
                            exit = True
                            break

                if t in des:
                    start_index = des.find(t)
                    last_index = start_index + len(t)
                    if (des[last_index:(last_index + 1)]).isalpha() == False:
                        if len(t) == (last_index - start_index):
                            result_city = t
                            exit = True
                            break

            if exit == False:
                result_city = ""
            exit = True
    return result_city


def append(name, des, oneplusone, price, discount, point, city, link):
    lis_names.append(name)
    # lis_description.append(des)
    lis_price.append(price)
    lis_discount.append(discount)
    lis_oneplusone.append(oneplusone)
    lis_point.append(point)
    lis_link.append(link)
    lis_city.append(city)


def append_leumi(name, price, point, city, link):
    lis_names.append(name)
    lis_price.append(price)
    lis_discount.append("")
    lis_oneplusone.append("")
    lis_point.append(point)
    lis_link.append(link)
    lis_city.append(city)
    # price(lis_names)


def getname_cal(name):
    name = str(name)
    start_index = name.find("<strong>")
    end_index = name.find("/strong>")
    name = (name[start_index + 8:end_index - 1])
    name = name.strip()
    return name


def getname_max(name):
    name = str(name)
    name = cleanme(name)
    name = name.strip()
    return name


def getdescription_leumi(des):
    # print("1")
    des = str(des)
    if "₪" in des:
        # print("2")
        start_index = des.find("₪")
        price_points = price_points = des[start_index - 7:start_index + 7]
        if "+" in price_points:
            # print("3")
            points, price = (price_points.split("+"))
            price = price.replace("₪", "")
            price = price.strip()
            points = points.strip()
            return price, points
        else:
            # print("4")
            price = des[start_index - 7:start_index + 7]
            price = price.replace("₪", "")
            price = int(re.search(r'\d+', price).group())
            if "float: right;font-size:" in des:
                # print("6")
                start_index2 = des.find("float: right;font-size:")
                points = des[start_index2 + 65: start_index2 + 80]
                points = points.strip()
                if points.isnumeric() == True:
                    return price, points
            return price, ""
    else:
        # print("5")
        if "float: right;font-size:" in des:
            # print("6")
            start_index2 = des.find("float: right;font-size:")
            points = des[start_index2 + 65: start_index2 + 80]
            points = points.strip()
            return "", points
        return "", ""


def getelement(url, content_info):
    element = ""
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content)
    for element in soup.findAll(attrs=content_info):
        element = element
    return element


def getelements(url, a, b, c, d):
    des = ""
    element = ""
    results_names = ""
    element2 = ""
    element3 = ""
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content)
    for element in soup.findAll(attrs=a):
        name = element.find(b)
        if str(name) not in results_names:
            results_names = cleanme(name)
        element1 = element
        des = str(element1)
    if element == "":
        return "", "", "", ""
    content = driver.page_source
    soup = BeautifulSoup(content)
    for element in soup.findAll(attrs=c):
        element2 = element
    content = driver.page_source
    soup = BeautifulSoup(content)
    for element in soup.findAll(attrs=d):
        element3 = element
    return element1, des, results_names, element2, element3


def getelements2(url, content_info, name_info, content_info2, content_info3):
    element1 = ""
    des = ""
    results_names = ""
    element2 = ""
    element3 = ""
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    element1 = soup
    for link in soup.find_all("div", class_=content_info):
        name = link.find(name_info)
        if str(name) not in results_names:
            results_names = cleanme(name)
        des = str(element1)
    if element1 == "":
        return "", "", "", ""
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    for link in soup.find_all("div", class_=content_info2):
        element2 = link
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    for link in soup.find_all("div", class_=content_info3):
        element3 = link
    return element1, des, results_names, element2, element3



def getnames_isracard(link):
    strlink=str(link)
    start=strlink.find('<span class="active">')
    strlink=strlink[start+21:]
    end=strlink.find("</span>")
    name=strlink[:end]
    name=name.strip()
    if "קופון" in name:
        if "קופון ל" in name:
            name=name.replace("קופון ל","")
        else:
            name=name.replace("קופון","")
    if "קבוצת ישראכרט" in name:
        if "- קבוצת ישראכרט" in name:
            name=name.replace("- קבוצת ישראכרט","")
        elif "-קבוצת ישראכרט" in name:
                name=name.replace("-קבוצת ישראכרט","")
        else:
            name=name.replace("קבוצת ישראכרט","")
    if "ל''" in name:
        name=name.replace("ל''","")
    name=name.strip()
    if "''" in name:
        name=name.replace("''","")
    #print(name)
    return name

def getelements3(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    element = soup
    for link in soup.find_all(class_="breadcrumbs-nav hidden-xs"):
        element1=link
    for link in soup.find_all(class_="col-md-7 benefit-info"):
        element2=link.find("h1")
    return element,element1,element2

def get_ae_links():

	url = 'https://rewards.americanexpress.co.il/parentcategories/culture/'
	req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
	html_page = urllib.request.urlopen(req)
	soup = BeautifulSoup(html_page, "html.parser" )

	links = []
	names = []

	for r in soup.findAll('script'):
		stripped = r.text.strip()
		if stripped.startswith('window.epi'):
			jsondata = stripped[13:-1]
			json_object = json.loads(jsondata)
			numitems = len(json_object["CurrentPage"]["Benefits"])
			for n in range(numitems):
				thisitem = json_object["CurrentPage"]["Benefits"][n]
				link = thisitem["LinkUrl"]
				name = thisitem["MobileBenefitName"]
				links.append('https://rewards.americanexpress.co.il' + link)
				names.append(name)
	return links



def get_ic_links():

	url = 'https://benefits.isracard.co.il/parentcategories/attractions/'
	req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
	html_page = urllib.request.urlopen(req)
	soup = BeautifulSoup(html_page, "html.parser" )

	links = []
	names = []

	for r in soup.findAll('script'):
		stripped = r.text.strip()
		if stripped.startswith('window.epi'):
			jsondata = stripped[13:-1]
			json_object = json.loads(jsondata)
			numitems = len(json_object["CurrentPage"]["Benefits"])
			for n in range(numitems):
				thisitem = json_object["CurrentPage"]["Benefits"][n]
				link = thisitem["LinkUrl"]
				name = thisitem["MobileBenefitName"]
				links.append('https://benefits.isracard.co.il/' + link)
				names.append(name)

	return links



def getelements4(url):
    element=""
    element1=""
    element2=""
    element3=""
    element4=""
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    element = soup
    for link in soup.find_all(class_="breadcrumbs-nav hidden-xs"):
        element1=link
    for link in soup.find_all(class_="col-md-7 benefit-info"):
        element2=link.find("h1")
    for link in soup.find_all("div",class_="col-10 short-border"):
        element3= link
        break
    for link in soup.find_all("div",class_="col-md-7 benefit-info"):
        element4=link.find("h1")
    return element,element1,element2, element3, element4



        #name = link.find("h1")
        #name= cleanme(name)
        #for m in re.finditer('ל', name):
            #start=m.start()








def getelements_cal(url):
    element1 = ""
    element2 = ""
    element3 = ""
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    res= soup.title
    res=res.get_text()
    res=res.replace("חנות החוויות של Cal -","")
    element1=res.strip()
    mydivs = soup.find_all("div", {"class": "col-9 col-lg-4"})
    element3 = soup.get_text()
    if mydivs:
        if "₪" in str(mydivs[0]):
            element2=mydivs[0].get_text()
            element2=getprice_cal(element2)
        else:
            element3=element3.replace("על כל 1500 ₪"," ")
            ran=element3.find("₪")
            element2=element3[ran-5:ran]
            element2=element2.strip()
    return element1, element2, element3


def getelements_cuponofesh(url):
    element1 = ""
    des = ""
    results_names = ""
    element2 = ""
    element3 = ""

    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    #print(soup)
    element1 = soup
    for link in soup.find_all("div", class_="top"):
        #print("hello")
        name = link.find("h2")
        address = link.find("address")
    if element1 == "":
        return "", "", "", ""
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    for link in soup.find_all(class_="price-label"):
        price = link.find("price")

    return name, address, price


# def getelements_cal(url, a, b, c):
# element = ""
# price = ""
# driver.get(url)
# content = driver.page_source
# soup = BeautifulSoup(content)
# for element in soup.findAll(attrs=a):
# element1 = element
# des = str(element1)
# if element == "":
# return "", "", "", ""

# content = driver.page_source
# soup = BeautifulSoup(content)
# for element in soup.findAll(attrs=b):
# element2 = element

# content = driver.page_source
# soup = BeautifulSoup(content)
# for element in soup.findAll(attrs=c):
# element3 = element
# return element1, des, element2, element3


def getprice_cal(element):
    element = str(element)
    element = element.replace("ב-", "      ")
    element = element.replace("ב", "      ")
    element = element.replace("ב -", "      ")
    element=element.replace("מ-","      ")
    element = element.replace("מ -", "      ")
    start_index = element.find("₪")
    price = element[start_index - 7:start_index]
    price = price.strip()
    return price


def getcity_leumi(element, element2, name):
    num = 0
    # if "רשימת הסניפים" in str(element):
    # print("a")
    # return "all"
    des = str(element)
    # rint("This is des:",des)
    start_index = des.find('"address":')
    des2 = des[start_index:]
    end_index = des2.find("businessUniqueNumber")
    city = (des2[11:end_index - 3].strip())
    end_index2 = des2.find("}];")
    des3 = des2[11:end_index2]
    for x in city_list:
        if x in des3:
            num = num + 1
            if num == 2:
                return "all"
    for c in city_list:
        if c in city:
            return c
    return ""


def getcity_cal(element):
    des = str(element)
    end_index = des.find("</div>")
    city = des[end_index - 50:end_index]
    city = city.strip()
    for c in city_list:
        if c in city:
            return c
    return ""


def csvmaker(name, oneplusone, price, discount, point, city, link):
    print(name, oneplusone, price, discount, point, city, link)
    df = pd.DataFrame({'Name': name, "price": price, "discount": discount, "plus_one": oneplusone,
                       "points": point, "city": city, "link": link})
    df.to_csv('names.csv', index=False, encoding='utf-8')


def getinfo_max(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    try:
        urllib.request.urlopen(req)
    except:
        return "","",""
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    res = soup.title
    res = res.get_text()
    a= res.find("הטבה")
    name=res[:a].strip()
    mydivs2=soup.find_all("h2")
    if mydivs2:
        desc= mydivs2[0].text
    else:
        desc=""
    des=str(soup.prettify())

    return des, name, desc


def checksimilar(name1, name2):
    if similar(name1, name2) > 0.7:
        return 1
    if similar(nospecial(name1.lower()), nospecial(name2.lower())) > 0.6 and nospecial(name2.lower()) != "":
        return 1
    if similar(name1.split('-')[0], name2.split('-')[0]) > 0.7:
        return 1
    return 0


def max():
    #print("Hello")
    global id
    url = geturl("https://max.co.il/sitemap.xml",
                 "https://www.max.co.il/he-il/Benefits/BenefitsPlus/Atractions/Pages")  # creates a list of urls
    #url = url[15:]
    #url= url.append("https://www.max.co.il/he-il/Benefits/BenefitsPlus/Atractions/Pages/kfar.aspx")

    for x in url:  # for every link
        #print("hello")
        #print(x)
        #print("bye")
        print(x)
        #element, des, results_names, results_description = getinfo(x, 'benefitInfo_content', 'h1',
                                                                   #'h2')
        des, name, description = getinfo_max(x)
        # get the data from the page
        if name == "":  # skips it if it doesn't have a name (Empty)
            print("stopped because name")
            continue
        if "מגוון אטרקציות" in name:
            print("stopped because name2")
            continue
        if description== "":
            print("stopped because description")
            continue
        oneplusone, price, point, discount = info_description(
            description)  # get the info from the nane description and more
        city = getcity(city_list, name, description, des)  # finds the city
        link = x  # saves the link
        database.add_attraction(connection, id, "max", name, price, discount, oneplusone, point, city, link)
        id = id + 1
    return id
    # append(name, description, oneplusone, price, discount, point, city, link)  # appends to lits
    # csvmaker(lis_names, lis_oneplusone, lis_price, lis_discount, lis_point, lis_city,
    # lis_link)  # create a csv file


def leumi():
    global id
    url = geturl2("https://www.leumi.co.il/sitemap_xml/LeumiHebrew/sitemap-benefit.xml",
                  "https://www.leumi.co.il/LeumiBenefit/45575")  # creates a list of urls
    #url= url[:20]
    # url = ["https://www.leumi.co.il/LeumiBenefit/45575/756"]
    # url.append("https://www.leumi.co.il/LeumiBenefit/45575/25556")
    # url.append("https://www.leumi.co.il/LeumiBenefit/45575/70063")
    for x in url:  # for every link
        # element, element2, element3, results_names = getinfo_max(x)
        # element, des, results_names, element2, element3 = getelements(x, 'BenefitItemParentContainer', 'h1',
        # 'BenefitItemDetails',"phone-and-location-details location-individual")

        element, des, results_names, element2, element3 = getelements2(x, 'BenefitItemParentContainer', 'h1',
                                                                       'BenefitItemDetails',
                                                                       "phone-and-location-details location-individual")
        if "כניסה ילד/מבוגר" and "מגוון הטבות החל מ" not in des:
            continue
        # if results_names == "":
        # continue
        price, points = getdescription_leumi(element2)
        if price == "" and points == "":
            continue
        link = x
        name = getname_max(results_names)
        city = (getcity_leumi(des, element3, name))
        records = connection.execute("SELECT * FROM attractions").fetchall()
        stop = 0
        for row in records:
            name2 = row[2]
            id_2 = row[0]
            if checksimilar(name, name2) == 1:
                stop = 1
                database.add_attraction(connection, id_2, "leumi", name, price, 0, 0, points, city, link)
                break
        if stop == 0:
            database.add_attraction(connection, id, "leumi", name, price, 0, 0, points, city, link)
            id = id + 1
    return id


def cal():
    global id
    #url_cal=["https://www.cal-store.co.il/product.php?pid=76CFC2D0-2D5C-40BC-B167-B0C19374D57E"]
    url_cal=getcallinks()
    #url_cal = url_cal[:20]
    for x in url_cal:  # for every link
        #print("a")
        print(x)
        element, element2, element3 = getelements_cal(x)
        #print("element2",element2)
        # element = getelement(x, "productTitle")
        #print(element)
        #print("b")
        #print(element)
        if element == "":
            #print("no")
            continue
        name = cleanme(element)
        #print(name)
        # element2 = getelement(x, "table table-stock")
        price = element2
        if price =="":
            continue

        # element3 = getelement(x, "branches-box")
        #print("hi")
        #print("ABC:",element3)
        city = getcity_cal(element3)
        link = x
        records = connection.execute("SELECT * FROM attractions").fetchall()
        stop = 0
        for row in records:
            name2 = row[2]
            id_2 = row[0]
            if checksimilar(name, name2) == 1:
                stop = 1
                database.add_attraction(connection, id_2, "cal", name, price, 0, 0, "", city, link)
                break
        if stop == 0:
            database.add_attraction(connection, id, "cal", name, price, 0, 0, "", city, link)
            id = id + 1
    return id


def cuponofesh():
    global id
    url = geturl3()
    # url = url[:5]
    for x in url:
        print(x)
        link=x
        url2 = x[:21] + "/siteapi" + x[21:]
        #print(url2)
        subprocess.call(['curl', url2, '-o', 'json.json'])
        subprocess.call(['curl', "https://cpnclub.co.il/siteapi/options", '-o', 'json_city.json'])
        # f = open("json.json", "r")
        # content = f.read()
        with open("json.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        name = jsonObject['supplierName']
        price = jsonObject['items']
        if len(price)==0:
            #print("Name:",name,"|","Price:","None","|","City: None")
            continue
        price=price[0]
        price = price["price"]
        city_num = jsonObject['cities_id']
        with open("json_city.json",encoding='utf-8') as jsonFile:
            jsonObject2 = json.load(jsonFile)
            jsonFile.close()
        citylist=jsonObject2["cities"]
        dic={}
        for c in citylist:
            id_city=c["id"]
            city2=c["name"]
            v= {id_city:city2}
            dic.update(v)
        city=dic[city_num]
        records = connection.execute("SELECT * FROM attractions").fetchall()
        stop = 0
        for row in records:
            name2 = row[2]
            id_2 = row[0]
            if checksimilar(name, name2) == 1:
                stop = 1
                database.add_attraction(connection, id_2, "cuponofesh", name, price, 0, 0, "", city, link)
                break
        if stop == 0:
            database.add_attraction(connection, id, "cuponofesh", name, price, 0, 0, "", city, link)
            id = id + 1
    return id


def isracard():
    global id
    url=get_ic_links()
    # url= url[:5]
    #url= ["https://benefits.isracard.co.il/benefitsforall/attractions/hay-kef-357/","https://benefits.isracard.co.il/benefitsforall/attractions/yamit-2000-355/","https://benefits.isracard.co.il/benefitsforall/family/ice-peaks-1409/"]
    for x in url:
        city=""
        link=x
        lenprice=0
        element, element1, element2=getelements3(x)
        if not element:
            continue
        name=getnames_isracard(element1)
        des=cleanme(element2)
        des=des.replace("בית ישראכרט, בני ברק, רחוב בר כוכבא 12","")
        #str_element=str(element)
        str_element=str(element).replace("בית ישראכרט, בני ברק, רחוב בר כוכבא 12","")
        str_element=str_element.replace('"כתובת: בית ישראכרט, בר כוכבא 12 בני ברק"',"")
        #print(str_element)
        if "1+1" in des:
            oneplusone="1"
        else:
            oneplusone="0"
        for c in city_list:
            if c in des:
                #print("a")
                city=c
                break
        if city=="":
            for c in city_list:
                if c in str_element:
                    #print("b")
                    city=c
                    break
        if "₪" in element:
            #print(element)
            numstop=0
            for m in re.finditer('₪', element):
                start=m.start()
                numstop=numstop+1
                if numstop==3:
                    break
            strprice=element[start-25:start]
            #strprice=nospecial2(strprice)
            #strprice.strip()
            #print(strprice)
            for i in strprice:
                lenprice=lenprice+1
                if len(nospecial2(i))!=0:
                    price=strprice[len(strprice)-lenprice:]
                    break
        else:
            price=""
        records = connection.execute("SELECT * FROM attractions").fetchall()
        stop = 0
        for row in records:
            pass
            name2 = row[2]
            id_2 = row[0]
            if checksimilar(name, name2) == 1:
                stop = 1
                database.add_attraction(connection, id_2, "isracard", name, "", 0, oneplusone, "", city, link)
                break
        if stop == 0:
            pass
            database.add_attraction(connection, id, "isracard", name, "", 0, oneplusone, "", city, link)
            id = id + 1
    return id

def americanexpress():
    url=get_ae_links()
    # url=url[:5]
    global id
    name_before=""
    number=0
    for x in url:
        #print("working on link number:",number)
        number=number+1
        link=x
        city=""
        element, element1, element2,element3, element4=getelements4(x)
        if not element:
            continue
        if "תרבות ופנאי" not in str(element1):
            continue
        if element2:
            if "הופעות והצגות" in element2:
                continue
        if element3:
            if "תמורת הטבת בונוס" in element3:
                points=1
            else:
                points1=cleanme(element3)
                points=int(re.search(r'\d+', points1).group())
        else:
            points=""
        name=cleanme(element4)
        if "פסטיבל" in name:
            continue
        if "סטנדאפ" in name:
            continue
        des=cleanme(element4)
        element=str(element)
        if "1+1" in des:
            name=name.replace("1+1","")
            oneplusone="1"
        elif "1 + 1" in des:
            name=name.replace("1 + 1","")
            oneplusone="1"
        else:
            oneplusone="0"
        if "₪" in des:
            price=int(re.search(r'\d+', des).group())
        else:
            price=""
        des=des.replace("בית ישראכרט, בני ברק, רחוב בר כוכבא 12","")
        #str_element=str(element)
        str_element=str(element).replace("בית ישראכרט, בני ברק, רחוב בר כוכבא 12","")
        str_element=str_element.replace('"כתובת: בית ישראכרט, בר כוכבא 12 בני ברק"',"")
        for c in city_list:
            if c in des:
                city=c
                break
        if city=="":
            for c in city_list:
                if c in str_element:
                    city=c
                    break
        if " - " in name:
            end=name.find(" - ")
            name=name[:end].strip()
        if not price and oneplusone==0:
            continue
        if name==name_before:
            continue
        name_before=name
        records = connection.execute("SELECT * FROM attractions").fetchall()
        stop = 0
        for row in records:
            pass
            name2 = row[2]
            id_2 = row[0]
            if checksimilar(name, name2) == 1:
                stop = 1
                database.add_attraction(connection, id_2, "americanexpress", name, price, 0, oneplusone, points, city, link)
                break
        if stop == 0:
            pass
            database.add_attraction(connection, id, "americanexpress", name, price, 0, oneplusone, points ,city, link)
            id = id + 1
    return id
# print(connection.execute("SELECT * FROM attractions").fetchall())


print("Good luck! starting max")
start1=time.time()
id = max()
end1=time.time()
print(f"ended max in: {end1 - start1} seconds | starting leumi")
# start2=time.time()
# id = leumi()
# end2=time.time()
# print(f"ended leumi in: {end2 - start2} seconds | starting cal")
# start3=time.time()
# id=cal()
# end3=time.time()
# print(f"ended cal in: {end3 - start3} seconds | starting cuponofesh")
# start4=time.time()
# id= cuponofesh()
# end4=time.time()
# print(f"ended cuponofesh in: {end4 - start4} seconds | starting isracard")
# start5=time.time()
# id= isracard()
# end5=time.time()
# print(f"ended isracard in: {end5 - start5} seconds | starting americanexpress")
# start6=time.time()
# id= americanexpress()
# end6=time.time()
# print(f"ended americanexpress in: {end6 - start6} seconds | took {(end6-start1)/60} minutes")

# Made by Aviv Friedman
