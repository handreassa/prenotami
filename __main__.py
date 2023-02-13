import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from time import sleep
import logging
import yaml
load_dotenv()

logging.basicConfig(
    format = '%(levelname)s:%(message)s',
    level = logging.INFO,
    handlers = [
        logging.FileHandler('/tmp/out.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class Prenota:
    def __init__(self):
        self.user_config = load_config('parameters.yaml')
        self.email = os.getenv('username')
        self.password = os.getenv('password')
        self.driver = webdriver.Safari()


    def check_file_exists(file_name):
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        file_path = os.path.join(parent_dir, file_name)
        return os.path.isfile(file_path)

    def load_config(file_path):
        # Open the YAML file
        with open(file_path, 'r') as file:
            # Load the YAML content into a Python dictionary
            config = yaml.safe_load(file)
        return config

    def do_login(self):
        try:
            self.driver.get("https://prenotami.esteri.it/")
            # Wait for the page to fully load
            self.driver.implicitly_wait(5)
            email_box = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "login-email")))
            password_box = self.driver.find_element(By.ID, "login-password")
            email_box.send_keys(self.email)
            password_box.send_keys(self.password)
        except Exception as e:
            logging.info(f"Exception: {e}")

    def fill_form(self):
        file_location = os.path.join('files/endereco.pdf')
        choose_file = self.driver.find_elements(By.ID, "File_0")
        choose_file[0].send_keys(file_location)
        privacy_check = self.driver.find_elements(By.ID, "PrivacyCheck")
        privacy_check[0].click()

    if __name__ == "__main__":
        
        do_login(self)

        if request_type == 'citizenship':
            self.driver.get('https://prenotami.esteri.it/Services/Booking/751')
            appts_available = self.driver.find_element(By.XPATH, "//*[@id='WlNotAvailable']").get_attribute("value")
            
            if appts_available == 'Al momento non ci sono date disponibili per il servizio richiesto':
                logging.info("TIMESTAMP: " + str(datetime.now()))
                logging.info("No change to prenotami detected.")
                sys.exit(0)
            else:
                message = "Change detected on prenotami, please check system for available appointments."
                logging.info("TIMESTAMP: " + str(datetime.now()))
                logging.info("Change detected on prenotami.")
                fill_form(self)
        elif request_type == 'passport':
            ...
            
        # Close the driver once the page has loaded
        driver.quit()