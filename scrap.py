# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
import re
import os
import time
from requests_html import HTMLSession

send_mail = 'ENV' in os.environ and os.environ['ENV'] == "PROD"

searching_for = {
    "name":"KS-2",
    "ref":"1801sk13"
}

# credentials

with open('gg_mdp_access.txt') as f:
    gmail_password = f.read()

gmail_user = 'fley58@gmail.com'

# get a webdriver
# driver = webdriver.PhantomJS(executable_path="/usr/local/Cellar/geckodriver/0.23.0/bin/geckodriver")

while True:
    # specify the url
    quote_page = 'https://www.kimsufi.com/fr/serveurs.xml'
    session = HTMLSession()
    r = session.get(quote_page)
    r.html.render(sleep=5)
    # with open('test.html','w+') as f:
    #     f.write(r.html.find('body', first=True).html)
    body = r.html.find('body', first=True).html

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(body, "html.parser")

    ####
    # SEARCHING FOR THE INFO WE NEED
    ####

    # Take out the <div> of name and get its value
    try:
        td_div = soup.find('tr', attrs={
            'class':'zone-dedicated-availability',
            'data-ref': searching_for["ref"]
        }).find('td', attrs={
            'class':'show-on-ref-unavailable'
        })
        html_availability_state = td_div["style"] == "display: none;"
    except Exception as e:
        print(body)
        print(e)
        html_availability_state = None

    state = "UNVAILABLE"
    body = ""

    if html_availability_state:
        state = "AVAILABLE"
        body = "Hey, seems that the server {} is available.".format(searching_for["name"])

    if html_availability_state == None:
        state = "LOST"
        body = "An error seems to occured." 

    if send_mail and state is not "UNVAILABLE":
        # send the mail

        sent_from = gmail_user
        to = ['fley58@gmail.com']  
        subject = 'Kimsufi monitoring'

        email_text = """Subject: {}\n\n{}""".format(subject, body)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

    sleep_time = 10
    if state == "AVAILABLE":
        sleep_time = 7200
    if state == "LOST":
        while True:
            time.sleep(1)
    print("{} Kimsufi state : {}".format(searching_for["name"],state))
    time.sleep(sleep_time)
