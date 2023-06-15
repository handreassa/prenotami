import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service #Fix deprecated executable_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import logging
import yaml
import sys
import time
import random

load_dotenv()

logging.basicConfig(
    format="%(levelname)s:%(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("/tmp/out.log"), logging.StreamHandler(sys.stdout)],
)


class Prenota:
    def check_file_exists(file_name):
        # parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        file_path = os.path.join(os.getcwd(), file_name)
        return os.path.isfile(file_path)

    def load_config(file_path):
        # Open the YAML file
        with open(file_path, "r") as file:
            # Load the YAML content into a Python dictionary
            config = yaml.safe_load(file)
        return config

    if __name__ == "__main__":
        if check_file_exists("files/residencia.pdf"):
            logging.info(
                f"Timestamp: {str(datetime.now())} - Required files available."
            )
            email = os.getenv("username")
            password = os.getenv("password")
            user_config = load_config("parameters.yaml")
            print(user_config.get("full_address"))
            chrome_options = ChromeOptions() #Some changes for optimize the load
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(
                options=chrome_options, service=Service(ChromeDriverManager().install(), #Some Changes for fix deprecated executable_path
            ))

            try:
                driver.get("https://prenotami.esteri.it/")
                # Wait for the page to fully load
                email_box = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "login-email"))
                )
                password_box = driver.find_element(By.ID, "login-password")
                email_box.send_keys(email)
                password_box.send_keys(password)
                time.sleep(4) #2 default
                button = driver.find_elements(
                    By.XPATH, "//button[contains(@class,'button primary g-recaptcha')]"
                )
                button[0].click()
                logging.info(
                    f"Timestamp: {str(datetime.now())} - Successfuly logged in."
                )
                time.sleep(10)#Waiting some time to fully load after login and skip errors

            except Exception as e:
                logging.info(f"Exception: {e}")

            for i in range(200):
                random_number = random.randint(1, 5)

                if user_config["request_type"] == "citizenship":
                    try:
                        driver.get("https://prenotami.esteri.it/Services/Booking/751")
                        time.sleep(10) #Waiting some time to fully load and skip errors
                        
                        try:
                            appts_available = driver.find_element(
                                By.XPATH, "//*[@id='WlNotAvailable']"
                            ).get_attribute("value")
                            logging.info(
                                f"Timestamp: {str(datetime.now())} - Scheduling is not available right now."
                            )
                        except NoSuchElementException:
                            logging.info(
                                f"Timestamp: {str(datetime.now())} - Element WlNotAvailable not found. Start filling the forms."
                            )
                            file_location = os.path.join("files/residencia.pdf")
                            choose_file = driver.find_elements(By.ID, "File_0")
                            choose_file[0].send_keys(file_location)
                            privacy_check = driver.find_elements(By.ID, "PrivacyCheck")
                            privacy_check[0].click()
                            submit = driver.find_elements(By.ID, "btnAvanti")
                            submit[0].click()
                            with open("files/citizenship_form.html", "w") as f:
                                f.write(driver.page_source)
                            break
                    except Exception as e:
                        logging.info(f"Exception {e}")
                        break		
                elif user_config["request_type"] == "passport":
                    try:
                        time.sleep(10) #Waiting some time to fully load and skip errors                        
                        driver.get("https://prenotami.esteri.it/Services/Booking/671")#/Booking/671
                        time.sleep(5) #Waiting some time to fully load and skip errors
                        #driver.get("https://prenotami.esteri.it/Services/Booking/671")
                        #time.sleep(10) #Waiting some time to fully load and skip errors                       

                        try:
                            appts_available = driver.find_element(
                                By.XPATH, "//*[@id='WlNotAvailable']"
                            ).get_attribute("value")
                            logging.info(
                                f"Timestamp: {str(datetime.now())} - Scheduling is not available right now."
                            )
                        except NoSuchElementException:
                            logging.info(
                                f"Timestamp: {str(datetime.now())} - Element WlNotAvailable not found. Start filling the forms."
                            )

                            with open("files/passport_form.html", "w") as f:
                                f.write(driver.page_source)

                            q0 = Select(driver.find_element(By.ID,"ddls_0"))
                            q0.select_by_visible_text(
                                user_config.get("possess_expired_passport")
                            )

                            q1 = Select(driver.find_element(By.ID,"ddls_1"))
                            q1.select_by_visible_text(
                                user_config.get("possess_expired_passport")
                            )

                            q2 = driver.find_element(By.ID,
                                "DatiAddizionaliPrenotante_2___testo"
                            )
                            q2.send_keys(user_config.get("total_children"))

                            q3 = driver.find_element(By.ID,
                                "DatiAddizionaliPrenotante_3___testo"
                            )
                            q3.send_keys(user_config.get("full_address"))

                            q4 = Select(driver.find_element(By.ID,"ddls_4"))
                            q4.select_by_visible_text(user_config.get("marital_status"))

                            time.sleep(1)

                            file0 = driver.find_element(By.XPATH,'//*[@id="File_0"]')
                            file0.send_keys(os.getcwd() + "/files/identidade.pdf")

                            time.sleep(1)

                            file1 = driver.find_element(By.XPATH,'//*[@id="File_1"]')
                            file1.send_keys(os.getcwd() + "/files/residencia.pdf")

                            checkBox = driver.find_element(By.ID,"PrivacyCheck")
                            checkBox.click()

                            form_submit = driver.find_element(By.ID,"btnAvanti")
                            form_submit.click()

                            break
                    except Exception as e:
                        logging.info(f"Exception {e}")
                        break

                time.sleep(random_number)

        else:
            logging.info(
                "Required files not available. Check the required files in readme.md file. Ending execution."
            )
            sys.exit(0)
        user_input = input(
            f"Timestamp: {str(datetime.now())} - Go ahead and fill manually the rest of the process. When finished, type quit to exit the program and close the browser. "
        )
        while True:
            if user_input == "quit":
                driver.quit()
                break