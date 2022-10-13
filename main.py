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
        # GenerateImageUsingDeepAi(story_text)
        # GenerateImageUsingStableDiffusion(story_text)
        print(story_text)
        window['STORY'].update(story_text)
        temp += story_text
        input_text = input()
        text_area.send_keys(input_text)
        submit_button.click()
        sleep(30)
        first_time = False

def Start():
    GetApiKey()
    driver = SetupDriver()
    PlayAIDungeon(driver) 



import PySimpleGUI as sg

sg.theme("LightGrey")
sg.set_options(font = ("Courier New", 8))

# frame_1 = [sg.Text('This is where you will write your story', key='STORY')], [sg.Text('', size = (20,10)), sg.InputText()], [sg.Submit()]
# frame_2 = [[sg.Text('This is where the image will be generated !')], ]

# layout = [
#     [sg.Frame('', frame_1, pad = (0,5)),
#      sg.Frame('', frame_2, pad = (0, (12,7)), key = 'Hide')],
# ]

# window = sg.Window('Image Generator', layout, resizable=True)
# event, values = window.read()
# Start()
# window.maximize()
# window.close()

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Story Text", key='STORY')
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-")
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout, finalize=True)

# Run the Event Loop
while True:
    Start()
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

        except:
            pass

window.close()


            