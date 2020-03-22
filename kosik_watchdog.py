import time
import logging
from random import randrange
import smtplib, ssl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# configuration
PATH_TO_CHROMEWEBDRIVER = r'C:\Users\jiri\Downloads\chromedriver_win32\chromedriver.exe'
TIME_SLEEP_MIN_SECONDS = 5
TIME_SLEEP_MAX_SECONDS = 15

ADDRESSES = {
    'receiver.address@test.com': 'Address of delivery.',
}

WATCHDOG_EMAIL = 'sender.address@test.com'
WATCHDOG_PASSWORD = '<sender password>'

def get_available_slots_count(address: str) -> int:
    driver = webdriver.Chrome(PATH_TO_CHROMEWEBDRIVER)
    driver.implicitly_wait(5)
    
    driver.get("https://www.kosik.cz/")

    driver.find_element(By.XPATH, "//b[contains(.,\'OVĚŘTE DOSTUPNÉ TERMÍNY ZDE\')]").click()
    driver.find_element(By.XPATH, "//div[@class=\'address-selector\']//input").send_keys(address)
    driver.find_element(By.XPATH, f"//td[contains(.,\'{address}\')]").click()
    driver.find_element(By.XPATH, "//button[contains(.,\'potvrzuji\')]").click()
    WebDriverWait(driver, 30000).until(expected_conditions.visibility_of_element_located((By.XPATH, "//p[contains(.,\'Přehled časů a cen doručení\')]")))
    elements = driver.find_elements(By.XPATH, "//p[contains(.,\'volno\')]")

    driver.quit()
    
    return len(elements)


def send_email(available_slots: int, receiver_email: str, address: str):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        message = f'Subject: {available_slots} available slots\n\nThe watchdog found {available_slots} available slots for address {address}.'.encode('utf-8')
        
        server.login(WATCHDOG_EMAIL, WATCHDOG_PASSWORD)
        server.sendmail(WATCHDOG_EMAIL, receiver_email, message)
        
        logging.info('Email sent to: %s', email)


logging.basicConfig(filename='kosik_watchdog.log', level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

for email, address in ADDRESSES.items():
    time.sleep(randrange(TIME_SLEEP_MIN_SECONDS, TIME_SLEEP_MAX_SECONDS))

    available_slots = get_available_slots_count(address)
    logging.info('Available slots found: %d, %s, %s', available_slots, email, address)

    if available_slots > 0:
        send_email(available_slots, email, address)
