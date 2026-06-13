from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import os
import shutil
import time
import pygetwindow as gw

class ImageAgent:


    def __init__(self):

        options = Options()

        options.add_experimental_option(
            "debuggerAddress",
            "127.0.0.1:9222"
        )

        self.driver = webdriver.Chrome(
            options=options
        )
        
        print("CONNECTED")

        try:
            print("Handles:", self.driver.window_handles)
        except Exception as e:
            print("Handles ERROR:", e)

        try:
            print("Current URL:", self.driver.current_url)
        except Exception as e:
            print("URL ERROR:", e)

        ##print("Connected to Gemini Chrome")
        
        self.downloads_folder = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        print(
            "Downloads folder:",
            self.downloads_folder
        )

    def generate_image(
        self,
        prompt,
        scene_number
    ):

        print(
            f"Generating image for scene "
            f"{scene_number}"
        )

        self.driver.get(
            "https://gemini.google.com/images"
        )
        
        print(
            "Current URL after navigation:",
            self.driver.current_url
        )
                
        print("Navigation complete")
        
        
        time.sleep(2)

        for window in gw.getWindowsWithTitle("Google Gemini"):

            try:

                window.restore()
                window.activate()

                print(
                    "Activated:",
                    window.title
                )

                break

            except Exception as e:

                print(
                    "Activation error:",
                    e
                )
        
        # self.driver.maximize_window()
        
        time.sleep(2)
       

        # self.driver.switch_to.window(
        #     self.driver.current_window_handle
        # )

        prompt_box = WebDriverWait(
            self.driver,
            30
        ).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '[contenteditable="true"]'
                )
            )
        )
        
        self.driver.execute_script(
            "arguments[0].focus();",
            prompt_box
        )

        prompt_box.click()

        time.sleep(2)

        prompt_box.send_keys(prompt)

        time.sleep(2)

        print(
            "Textbox content:",
            repr(prompt_box.text)
        )

        time.sleep(1)

        prompt_box.send_keys(Keys.ENTER)

        print("Prompt submitted")
        
        # Wait for Gemini to generate image
        time.sleep(35)

        images = self.driver.find_elements(
            By.TAG_NAME,
            "img"
        )

        print("Images found:", len(images))

        generated_image = None

        for img in images:

            if img.size["width"] > 500:

                generated_image = img
                break

        if generated_image is None:
            raise Exception("Generated image not found")

        print(
            "Generated image found:",
            generated_image.size
        )

        ActionChains(self.driver).move_to_element(
            generated_image
        ).perform()

        print("Hovered over image")

        time.sleep(2)

        download_button = WebDriverWait(
            self.driver,
            30
        ).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'button[aria-label="Download full size image"]'
                )
            )
        )

        print("Download button found!")
        
        before_files = set(
            os.listdir(self.downloads_folder)
        )

        before_files = {
        f
        for f in os.listdir(
        self.downloads_folder
        )
        if f.startswith(
        "Gemini_Generated_Image"
        )
        }

        print(
        "Gemini files before download:",
        len(before_files)
        )

        download_button.click()

        print("Download clicked!")

        downloaded_file = None

        for _ in range(30):

            
            time.sleep(1)

            after_files = {
                f
                for f in os.listdir(
                    self.downloads_folder
                )
                if f.startswith(
                    "Gemini_Generated_Image"
                )
            }

            new_files = (
                after_files
                - before_files
            )
            
            print(
                "Checking downloads...",
                len(after_files)
            )

            if new_files:

                downloaded_file = list(
                    new_files
                )[0]

                break
        

        if downloaded_file is None:

        
            raise Exception(
                "Downloaded Gemini image not found"
            )
        

        print(
        "New Gemini file:",
        downloaded_file
        )

        source_path = os.path.join(
        self.downloads_folder,
        downloaded_file
        )

        destination_path = os.path.join(
        "assets",
        "generated_images",
        f"scene{scene_number}.png"
        )

        print(
        "Absolute destination:",
        os.path.abspath(
        destination_path
        )
        )

        if os.path.exists(
        destination_path
        ):
            os.remove(
            destination_path
            )

        shutil.move(
        source_path,
        destination_path
        )

        print(
        "Moved image to:",
        destination_path
        )


    def generate_images(self, story):
        
        print("About to navigate")

        for file in os.listdir(
            "assets/generated_images"
        ):

            if file.endswith(".png"):

                os.remove(
                    os.path.join(
                        "assets/generated_images",
                        file
                    )
                )

        for scene in story["scenes"]:

            print(
                f"Starting Scene {scene['scene_number']}"
            )

            self.generate_image(
                scene["image_prompt"],
                scene["scene_number"]
            )

