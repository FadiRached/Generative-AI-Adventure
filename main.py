import os
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from requests import post
from replicate import models

DEEP_AI_API_KEY = ''
REPLICATE_API_KEY = ''
QUICK_START_BUTTON_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]'
TURN_OFF_EVENTS_BUTTON_XPATH = '/html/body/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[2]'
SUBMIT_BUTTON_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div[2]'
TEXT_AREA_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/textarea'
STORY_TEXT_DIV_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div'
AI_DUNGEON_URL = 'https://play.aidungeon.io/main/worldStart?worldPublicId=1542906f-3100-4849-b28b-e6b11a8dd0b8'
DEEP_AI_URL = 'https://api.deepai.org/api/text2img?grid_size=1'


def SetupDriver():
    service = Service(executable_path="chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def GetApiKey():
    with open('deep-ai.txt') as file:
        text = file.read()
        global DEEP_AI_API_KEY
        DEEP_AI_API_KEY = text

    with open('replicate.txt') as file:
        text = file.read()
        global REPLICATE_API_KEY
        REPLICATE_API_KEY = text


def GenerateImageUsingDeepAi(text):
    r = post(
        DEEP_AI_URL,
        data={'text': text, },
        headers={'api-key': DEEP_AI_API_KEY}
    )

    json = r.json()
    print('Deep AI Image URL: ' + json['output_url'])


def GenerateImageUsingStableDiffusion(text):
    try:
        os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_KEY
        model = models.get("stability-ai/stable-diffusion")
        output = model.predict(prompt=text)
        print('Stable Diffusion Image URL: ' + output[0] + '\n')
    except Exception as e:
        print(e)


def LoginToAIDungeon(driver: webdriver.Chrome):
    driver.get(AI_DUNGEON_URL)
    sleep(10)
    quickstart_button = driver.find_element(By.XPATH, QUICK_START_BUTTON_XPATH)
    quickstart_button.click()
    sleep(20)
    turn_off_events_button = driver.find_element(
        By.XPATH, TURN_OFF_EVENTS_BUTTON_XPATH)
    turn_off_events_button.click()
    sleep(10)


def PlayAIDungeon(driver: webdriver.Chrome):
    LoginToAIDungeon(driver)
    submit_button = driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH)
    text_area = driver.find_element(By.XPATH, TEXT_AREA_XPATH)
    story_text_div = driver.find_element(By.XPATH, STORY_TEXT_DIV_XPATH)

    first_time = True
    temp = ''
    while (True):
        story_text = story_text_div.text
        if (not first_time):
            story_text = story_text.replace(temp, '')
        GenerateImageUsingDeepAi(story_text)
        GenerateImageUsingStableDiffusion(story_text)
        print(story_text)
        temp += story_text
        input_text = input()
        text_area.send_keys(input_text)
        submit_button.click()
        sleep(25)
        first_time = False


GetApiKey()
driver = SetupDriver()
PlayAIDungeon(driver)
