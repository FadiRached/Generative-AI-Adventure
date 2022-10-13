import io
import os
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from requests import post
from replicate import models
from PIL import Image


DEEP_AI_API_KEY = ''
REPLICATE_API_KEY = ''
QUICK_START_BUTTON_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]'
TURN_OFF_EVENTS_BUTTON_XPATH = '/html/body/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[2]'
SUBMIT_BUTTON_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div[2]'
TEXT_AREA_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/textarea'
STORY_TEXT_DIV_XPATH = '//*[@id="root"]/div/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div'
AI_DUNGEON_URL = 'https://play.aidungeon.io/main/worldStart?worldPublicId=1542906f-3100-4849-b28b-e6b11a8dd0b8'
DEEP_AI_URL = 'https://api.deepai.org/api/text2img?grid_size=1'


def PlayAIDungeon():
    first_time = True
    temp = ''
    while (True):
        story_text = story_text_div.text
        if (not first_time):
            story_text = story_text.replace(temp, '')

        #Text
        window['-STORY-'].update(story_text_div.text)

        #Image
        url = GenerateImageUsingDeepAi(story_text)
        img = DownloadImage(url)
        window["-IMAGE-"].update(img)

        window['-SUBMIT-'].update(disabled=False)

        while True:
            event, values = window.read()
            if (event == '-SUBMIT-'):
                input_text = values['-INPUT-']
                text_area.send_keys(input_text)
                submit_button.click()
                window['-INPUT-'].update('')

                window['-SUBMIT-'].update(disabled=True)
                sleep(40)
                first_time = False
                temp += story_text
                break
            if (event == None):
                return


def SetupGUI():
    import PySimpleGUI as sg

    sg.theme("LightGrey")
    sg.set_options(font=("Courier New", 16))

    story_column = [
        [
            sg.Text("Story Text", key='-STORY-', size=(60, None))
        ],
        [
            sg.In(size=(25, None), enable_events=True, key="-INPUT-"),
            sg.Button("Submit", key='-SUBMIT-')
        ],

    ]

    image_viewer_column = [
        [sg.Image(key="-IMAGE-")]
    ]

    layout = [
        [
            sg.Column(story_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]

    global window
    window = sg.Window("Wade Dungeon", layout, finalize=True,
                       location=(0, 0), size=(1536, 864), resizable=True)


def SetupDriver():
    service = Service(executable_path="chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    global driver
    driver = webdriver.Chrome(service=service, options=options)


def GetApiKeys():
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
    url = json['output_url']
    return url


def GenerateImageUsingStableDiffusion(text):
    try:
        os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_KEY
        model = models.get("stability-ai/stable-diffusion")
        output = model.predict(prompt=text)
        return output[0]
    except Exception as e:
        print(e)


def LoginToAIDungeon():
    driver.get(AI_DUNGEON_URL)
    sleep(20)

    # Click the 'quick start' button
    driver.find_element(By.XPATH, QUICK_START_BUTTON_XPATH).click()
    sleep(20)
    # Click the 'turn off events' button
    driver.find_element(By.XPATH, TURN_OFF_EVENTS_BUTTON_XPATH).click()
    sleep(20)


def GetAIDungeonElements():
    global submit_button
    global text_area
    global story_text_div

    submit_button = driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH)
    text_area = driver.find_element(By.XPATH, TEXT_AREA_XPATH)
    story_text_div = driver.find_element(By.XPATH, STORY_TEXT_DIV_XPATH)


def DownloadImage(url):
    import cloudscraper

    jpg_data = (
        cloudscraper.create_scraper(
            browser={"browser": "firefox",
                     "platform": "windows", "mobile": False}
        )
        .get(url)
        .content
    )

    pil_image = Image.open(io.BytesIO(jpg_data))
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()
    return png_data


def main():
    SetupGUI()
    GetApiKeys()
    SetupDriver()
    LoginToAIDungeon()
    GetAIDungeonElements()
    PlayAIDungeon()


if __name__ == "__main__":
    main()
