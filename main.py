from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path="C:\WebDriver\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=service, chrome_options=options)
driver.get('https://play.aidungeon.io/main/worldStart?worldPublicId=1542906f-3100-4849-b28b-e6b11a8dd0b8')
sleep(5)
quickstart_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]')
quickstart_button.click()
sleep(20)
turn_off_events_button =  driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[2]')
turn_off_events_button.click()
sleep(1)
story_text_div = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div')
story_text = story_text_div.text

with open('C:\Keys\deep-ai.txt') as file:
    text = file.read()
API_KEY = text

import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': story_text,
    },
    headers={'api-key': API_KEY}
)

json = r.json()
print('\nGenerated Image URL: ' + json['output_url']+ '\n')


sleep(100000)
