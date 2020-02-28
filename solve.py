import time
import datetime
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Threshold yyyy/mm/dd
threshold_date = datetime.datetime(2019, 12, 31)

# Agents
agents = ["Ehizogie I", "Tyler G.", "Gabriel H.", "Andrew Wong", "Antonio"]

# Get User from env
user = os.environ['ZENDESK_USER']
password = os.environ['ZENDESK_PASSWORD']

# Get Date of Last Message
def get_date(driver):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".live.full")))
    date = driver.find_element_by_css_selector(".live.full")
    text = date.text.replace(',', '').encode('ascii', 'ignore').decode('utf-8')
    return datetime.datetime.strptime(text, '%b %d %Y %I:%M %p')

# Get Agent Name
def get_name(driver):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "name")))
    return driver.find_element_by_class_name("name")
    
# Check the content of the message for dispute form URL
def check_content(driver):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zd-comment")))
    comment = driver.find_element_by_class_name("zd-comment")
    if "https://docs.google.com/forms/d/1EQyrrY1AUP9cH5UTskqIx5yK9mtSvIQCgZi_VkduRf0/viewform?edit_requested=true" in comment.text:
        return True
    return False

# Login logic
def login(driver):
    wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
    driver.find_element_by_name("identifier").send_keys(user + Keys.RETURN)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located((By.NAME, "password")))
    driver.find_element_by_name("password").send_keys(password + Keys.RETURN)

with webdriver.Chrome('/Users/tylergearing/Downloads/chromedriver') as driver:
    # Setup wait for later
    wait = WebDriverWait(driver, 50)

    # Open Zendesk URL
    driver.get('https://synapsepay.zendesk.com/agent/filters')

    # Login to Zendesk
    login(driver)

    # Wait for the window to load then get the window handle
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".LRab.LRaf.LRag.LRah.LRai.LRaj.LRak.LRal.LRam.LRan.LRao.LRap.LRaq.LRar.LRas.LRat.LRau.LRbd")))
    current_window = driver.current_window_handle
    assert len(driver.window_handles) == 1

    # Open Dispute Form tab
    driver.execute_script("window.open('');")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)
    driver.get("https://docs.google.com/spreadsheets/d/13h-zXiHgbtzkIzEEiAB_lvoYDzPjb0pEa8XijuDn4sA/edit?pli=1#gid=1961126054")
    wait.until(EC.title_is("Dispute Form - Google Sheets"))

    # Switch back to Zendesk
    driver.switch_to.window(current_window)

    # Sort by Updated
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".LRab.LRaf.LRag.LRah.LRai.LRaj.LRak.LRal.LRam.LRan.LRao.LRap.LRaq.LRar.LRas.LRat.LRau.LRbd")))
    elems = driver.find_elements_by_css_selector(".LRab.LRaf.LRag.LRah.LRai.LRaj.LRak.LRal.LRam.LRan.LRao.LRap.LRaq.LRar.LRas.LRat.LRau.LRbd")
    elems[3].click()
    time.sleep(1)
    elems[3].click()
    time.sleep(1)

    # Hit Play Button
    driver.find_element_by_css_selector(".btn._tooltip").click()

    # Get Last Person to Respond and Recent Date
    name = get_name(driver)
    dt_object = get_date(driver)
    
    processing_tickets = True
    while processing_tickets:
        if dt_object < threshold_date and name.text in agents and check_content(driver):
            driver.find_elements_by_class_name("zd-selectmenu-base")[4].click()
            time.sleep(1)
            driver.find_element_by_link_text("No User Response").click()
            time.sleep(1)
            driver.find_element_by_css_selector(".Button__StyledButton-sc-12lsl5w-0.index__c-btn___3y2Qe.index__c-btn--primary___1YOfW.lcPfmb").click()
            time.sleep(2)
            name = get_name(driver)
            dt_object = get_date(driver)
        else:
            driver.find_element_by_css_selector(".btn.next").click()
            time.sleep(2)
            name = get_name(driver)
            dt_object = get_date(driver)