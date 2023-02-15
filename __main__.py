import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
    
    def eval_availability(appts_available) -> bool:
        """"Receives the value displayed in the screen for both scheduling types and return if it should proceed with form filling or try to book again"""
        if (appts_available == "Al momento non ci sono date disponibili per il servizio richiesto"):
            logging.info(f"Timestamp: {str(datetime.now())} - Scheduling is not available right now.")
            return False
        else:
            logging.info(f"Timestamp: {str(datetime.now())} - Proceeding with form filling...")
            return True
        

    if __name__ == "__main__":

        if check_file_exists("files/residencia.pdf"):
            logging.info(f"Timestamp: {str(datetime.now())} - Required files available.")
            email = os.getenv("username")
            password = os.getenv("password")
            user_config = load_config("parameters.yaml")
            print(user_config.get("full_address"))            
            chrome_options = ChromeOptions()
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--start-maximized")
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

            try:
                driver.get("https://prenotami.esteri.it/")
                # Wait for the page to fully load
                email_box = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "login-email"))
                )
                password_box = driver.find_element(By.ID, "login-password")
                email_box.send_keys(email)
                password_box.send_keys(password)
                sleep(2)
                button = driver.find_elements(By.XPATH, "//button[contains(@class,'button primary g-recaptcha')]")
                button[0].click()
                logging.info(f"Timestamp: {str(datetime.now())} - Successfuly logged in.")

            except Exception as e:
                logging.info(f"Exception: {e}")
                
            for i in range(4):
                random_number = random.randint(1, 5)
                
                if user_config["request_type"] == "citizenship":
                    try:
                        driver.get("https://prenotami.esteri.it/Services/Booking/751")
                        appts_available = driver.find_element(By.XPATH, "//*[@id='WlNotAvailable']").get_attribute("value")

                        if eval_availability(appts_available):
                            
                            file_location = os.path.join("files/residencia.pdf")
                            choose_file = driver.find_elements(By.ID, "File_0")
                            choose_file[0].send_keys(file_location)
                            privacy_check = driver.find_elements(By.ID, "PrivacyCheck")
                            privacy_check[0].click()
                            submit = driver.find_elements(By.ID, "btnAvanti")
                            submit[0].click()
                            time.sleep(60)
                            test = driver.find_elements(By.ID, "ServizioDescrizione")
                            with open('files/citizenship_form.html', 'w') as f:
                                f.write(driver.page_source)
                            sleep(400)
                            break
                    except Exception as e:
                        logging.info(f"Exception {e}")
                        break

                elif user_config["request_type"] == "passport":
                    try:
                        driver.get("https://prenotami.esteri.it/Services/Booking/671")
                        
                        appts_available = driver.find_element(By.XPATH, "//*[@id='WlNotAvailable']").get_attribute("value")

                        if eval_availability(appts_available):
                            with open('files/passport_form.html', 'w') as f:
                                    f.write(driver.page_source)
                            
                            q0 = Select(driver.find_element_by_id("ddls_0"))
                            q0.select_by_visible_text(
                                user_config.get("possess_expired_passport")
                            )  # Possess expired italian passport? Yes or no

                            # Dropdown Menu Question 2
                            q1 = Select(driver.find_element_by_id("ddls_1"))
                            q1.select_by_visible_text(user_config.get("possess_expired_passport"))  # Has under age child? Yes or No

                            # Text Question 1
                            q2 = driver.find_element_by_id("DatiAddizionaliPrenotante_2___testo")
                            q2.send_keys(user_config.get("total_children"))  # Number of children - send total

                            # Text Question 2 (Address)
                            q3 = driver.find_element_by_id("DatiAddizionaliPrenotante_3___testo")
                            q3.send_keys(
                                user_config.get("full_address")
                            )  # Residential address - full address

                            # Dropdown Menu Question 3
                            q4 = Select(driver.find_element_by_id("ddls_4"))
                            q4.select_by_visible_text(
                                user_config.get("marital_status")
                            )  # Marital status - fill it with the available options

                            time.sleep(1)

                            # File Upload 1
                            file0 = driver.find_element_by_xpath('//*[@id="File_0"]')
                            file0.send_keys(os.getcwd() + "/files/residencia.pdf")  # FILL THIS

                            time.sleep(1)

                            # File Upload 2
                            file1 = driver.find_element_by_xpath('//*[@id="File_1"]')
                            file1.send_keys(
                                os.getcwd() + "/files/residencia_2.pdf"
                            )  # FILL THIS

                            # CheckBox
                            checkBox = driver.find_element_by_xpath('//*[@id="PrivacyCheck"]')
                            checkBox.click()

                            # Submit Button
                            form_submit = driver.find_element_by_xpath('//*[@id="submit"]')
                            form_submit.click()
                            sleep(400)
                            break
                    except Exception as e:
                        logging.info(f"Exception {e}")
                        break

                time.sleep(random_number)


        else:
            logging.info("Required files not available. Check the required files in readme.md file. Ending execution.")
            sys.exit(0)

        # Close the driver once the page has loaded - since we will have to deal manually with schedule, will keep driver open
        driver.quit()
