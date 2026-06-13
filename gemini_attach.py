from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

time.sleep(3)

elements = driver.find_elements(
    By.CSS_SELECTOR,
    '[contenteditable="true"]'
)

prompt_box = elements[0]

prompt_box.click()

prompt_box.send_keys(
    "Create an image of a cute white rabbit wearing blue overalls and a red scarf."
)

print("Prompt entered!")

input("Press Enter to exit...")