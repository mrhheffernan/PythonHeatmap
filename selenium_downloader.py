import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

download_dir = "<replace>"

options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium-browser"

options.add_experimental_option(
    "prefs",
    {
        "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
        "download": {"prompt_for_download": False, "default_directory": download_dir},
    },
)
driver = webdriver.Chrome(options=options)

with open("login_info.secret") as f:
    usern, passw, id = f.read().strip().split(",")

driver.get("http://strava.com/login")

usern_box = driver.find_element(By.XPATH, "//input[@name='email' and @type='email']")
usern_box.send_keys(usern)

passw_box = driver.find_element(
    By.XPATH, "//input[@name='password' and @type='password']"
)
passw_box.send_keys(passw)

submit_button = driver.find_element(By.XPATH, '//button[@id="login-button"]')
submit_button.click()

time.sleep(2)

driver.get("https://www.strava.com/athletes/" + str(id))

monthly_button = driver.find_element(
    By.XPATH, '//a[contains(@class,"button btn-xs") and contains(@href,"month")]'
)
monthly_button.click()

time.sleep(2)

bar_list = driver.find_elements(
    By.XPATH, '//a[@class="bar" and contains(@href,"interval")]'
)

activity_list = []

for bar in bar_list:
    bar.click()
    time.sleep(3)

    for a in driver.find_elements(
        By.XPATH,
        './/a[contains(@href, "activities") and not(contains(@href, "twitter")) and not(contains(@href, "#")) and not(contains(@href, "photos")) and not(contains(@href, "segments"))]',
    ):
        activity_list.append(a.get_attribute("href"))

activity_list = set(activity_list)

print("Number of activities found: ", len(activity_list))

for address in activity_list:
    driver.get(address + "/export_gpx")
    time.sleep(1)

print("Data downloaded to " + download_dir + ", quitting.")

driver.quit()
