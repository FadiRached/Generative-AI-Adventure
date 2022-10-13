import os
from time import sleep
import requests
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


def PlayAIDungeon():
    first_time = True
    temp = ''
    while (True):
        story_text = story_text_div.text
        if (not first_time):
            story_text = '\n' + story_text.replace(temp, '') + '\n'

        #Text
        print(story_text)
        window['-STORY-'].update(story_text)

        #Image
        # url = GenerateImageUsingDeepAi(story_text)
        # response = requests.get(url, stream=True)
        # response.raw.decode_content = True
        # window["-IMAGE-"].update(data=response.raw.read())

        temp += story_text
        input_text = input()
        text_area.send_keys(input_text)
        submit_button.click()
        sleep(30)
        first_time = False


def SetupGUI():
    import PySimpleGUI as sg

    sg.theme("LightGrey")
    sg.set_options(font=("Courier New", 16))

    # First the window layout in 2 columns
    file_list_column = [
        [
            sg.Text("Story Text", key='-STORY-')
        ],
        [
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-")
        ],
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [sg.Text("Generated Image")],
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

    global window
    window = sg.Window("Wade Dungeon", layout, finalize=True)

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
    print('Deep AI Image URL: ' + url)
    return url


def GenerateImageUsingStableDiffusion(text):
    try:
        os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_KEY
        model = models.get("stability-ai/stable-diffusion")
        output = model.predict(prompt=text)
        print('Stable Diffusion Image URL: ' + output[0] + '\n')
        return output[0]
    except Exception as e:
        print(e)


def LoginToAIDungeon():
    driver.get(AI_DUNGEON_URL)
    sleep(15)
    driver.find_element(By.XPATH, QUICK_START_BUTTON_XPATH).click() # Click the 'quick start' button
    sleep(20)
    driver.find_element(By.XPATH, TURN_OFF_EVENTS_BUTTON_XPATH).click() # Click the 'turn off events' button
    sleep(10)


def GetAIDungeonElements():
    global submit_button
    global text_area
    global story_text_div
    
    submit_button = driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH)
    text_area = driver.find_element(By.XPATH, TEXT_AREA_XPATH)
    story_text_div = driver.find_element(By.XPATH, STORY_TEXT_DIV_XPATH)


def main():
    SetupGUI()
    GetApiKeys()
    SetupDriver()
    LoginToAIDungeon()
    GetAIDungeonElements()
    PlayAIDungeon()

if __name__ == "__main__":
    main()

# # Run the Event Loop
# while True:
#     Start()
#     event, values = window.read()
#     if event == "Exit" or event == sg.WIN_CLOSED:
#         break
#     # Folder name was filled in, make a list of files in the folder
#     if event == "-FOLDER-":
#         folder = values["-FOLDER-"]
#         try:
#             # Get list of files in folder
#             file_list = os.listdir(folder)
#         except:
#             file_list = []

#         fnames = [
#             f
#             for f in file_list
#             if os.path.isfile(os.path.join(folder, f))
#             and f.lower().endswith((".png", ".gif"))
#         ]
#         window["-FILE LIST-"].update(fnames)
#     elif event == "-FILE LIST-":  # A file was chosen from the listbox
#         try:
#             filename = os.path.join(
#                 values["-FOLDER-"], values["-FILE LIST-"][0]
#             )
#             window["-TOUT-"].update(filename)
#             window["-IMAGE-"].update(filename=filename)

#         except:
#             pass

# window.close()
