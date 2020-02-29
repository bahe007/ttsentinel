import json 
import requests
import datetime, time 
import threading
import smtplib

NOTIFICATION_MAIL_TEXT = "Subject: [Important] A Website Went Offline\r\n\r\n\
    Website: {}\r\n\
    Time and Date: {}"

config = None 
with open("config.json", "r") as f:
    config = json.load(f)

def is_website_online(path, timeout):
    """
    Checks wether a given website is currently online. To do that, it reads the
    HTTP status code. However, you could also add addidtional checks, e. g. testing
    if a specific text is returned.

    Parameters
    ----------
    - path : str
        exact path which should be checked
    - timeout : float
        after `timeout` seconds without answer, a website is considered offline

    Returns
    -------
    `True` if the website could be reached with the given path and returned HTTP Code `200`.
    """
    try:
        response = requests.get(path, timeout=timeout)
        return response.status_code == 200
    except:
        return False 

def send_notification_email(website, email_receiver):
    """
    Sends a notification email that a website was offline during a check. 

    If a failure occurs while sending the email, it'll be automatically
    retried up to nine times with a backoff time of 1s between.

    Parameters
    ----------
    - website : str
        website that is offline
    - email_receiver : str
        email address to which the notification should be sent
    """
    global NOTIFICATION_MAIL_TEXT

    offline_time = datetime.datetime.now()
    text = NOTIFICATION_MAIL_TEXT.format(website, offline_time)
    print("{} went offline: {}".format(website, offline_time))

    for _ in range(10):
        try:
            server = smtplib.SMTP(config["email"]["server"], config["email"]["port"])
            server.ehlo()
            server.starttls()
            server.login(config["email"]["sender"], config["email"]["password"])
            server.sendmail(config["email"]["sender"], [email_receiver], text)
            break
        except Exception as e:
            print('Couldn\'t send email: {}'.format(e))
        time.sleep(1)

def check_website(path, email, timeout):
    """
    Coordinator function to determine if a website is offline and sending a 
    notification if necessary..

    Parameters
    ----------
    - path : str
        exact path which should be checked
    - email : str
        email address to which the notification should be sent
    - timeout : float
        after `timeout` seconds without answer, a website is considered offline
    """
    if is_website_online(path, timeout): # website is online
        if path in config["offline"]: 
            config["offline"].remove(path)
    elif path not in config["offline"]: # website is offline and not already known to be offline
        config["offline"].append(path)
        send_notification_email(path, email)


print("ttsentinel started: {}".format(datetime.datetime.now()))
while True: 
    for i in range(len(config["sites"])):
        website = config["sites"][i]
        threading.Thread(target=check_website, args=(i,))
        check_website(website["url"], website["email"], config["timeout"])

    time.sleep(config["intervall"])