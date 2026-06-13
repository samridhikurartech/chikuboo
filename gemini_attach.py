from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

options = Options()

options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

print("Connected to Chrome")

driver.get("https://gemini.google.com/images")

prompt_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            '[contenteditable="true"]'
        )
    )
)

prompt = """
Generate ONE image only.

A cute white rabbit wearing blue overalls and a red scarf.

Pixar-style 3D animation.
Children's storybook illustration.
Bright colors.

Do not provide text.
Return only the generated image.
"""

prompt_box.click()
prompt_box.send_keys(prompt)

time.sleep(1)

prompt_box.send_keys(Keys.ENTER)

print("Prompt submitted")

# Wait for image generation
time.sleep(35)

images = driver.find_elements(By.TAG_NAME, "img")

print("Images found:", len(images))

for i, img in enumerate(images):
    try:
        print(
            i,
            "width=", img.size["width"],
            "height=", img.size["height"]
        )
    except:
        pass

# Hover over latest image
generated_image = None

for img in images:
    if img.size["width"] > 500:
        generated_image = img
        break

print("Generated image found:", generated_image.size)

ActionChains(driver).move_to_element(
    generated_image
).perform()

print("Hovered over image")

time.sleep(2)


# Now find download button
download_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
            'button[aria-label="Download full size image"]'
        )
    )
)

print("Download button found!")

download_button.click()

print("Download clicked!")


input("Press Enter to exit...")