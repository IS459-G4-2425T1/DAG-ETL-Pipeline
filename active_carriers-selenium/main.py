
#This script has yet to be tested with AWS Lambda

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkdtemp

def lambda_handler(event, context):
    # Set up Chrome options for headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920x1080')
    options.add_argument(f'--user-data-dir={mkdtemp()}')
    options.add_argument(f'--data-path={mkdtemp()}')
    options.add_argument(f'--disk-cache-dir={mkdtemp()}')
    
    # Specify the path for Chrome and ChromeDriver
    options.binary_location = "/opt/chrome/chrome"  # Path to Chrome binary
    service = ChromeService(executable_path="/opt/chrome-driver/chromedriver")  # Path to ChromeDriver

    # Initialize WebDriver with the specified options
    driver = webdriver.Chrome(service=service, options=options)

    dropdown_id = 'Carrier'
    active_carriers = []

    def check_button_exists():
        try:
            button = driver.find_element(By.ID, 'submit')
            print("The submit button exists on the page.")
            return button
        except NoSuchElementException:
            print("The submit button does not exist on the page.")
            return None

    def wait_for_page_to_load():
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'submit')))
            print("The page has fully loaded.")
        except TimeoutException:
            print("Timed out waiting for the page to load.")

    def is_not_active():
        try:
            # Check for the <td> element by its text
            driver.find_element(By.XPATH, f"//td[contains(text(), 'No data available for the selected carrier, airport, or time period.')]")
            return True
        except NoSuchElementException:
            return False

    try:
        url = 'https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp'  # Replace with the actual URL
        driver.get(url)
        wait_for_page_to_load()

        # Fetch the dropdown options
        dropdown = Select(driver.find_element(By.ID, dropdown_id))
        options = dropdown.options  # Get all options from the dropdown
        length = len(options)

        for i in range(1, length):  # Skip the first option (usually a placeholder)
            # Select the i-th option using the Select class
            dropdown.select_by_index(i)
            text = options[i].text
            print(f"Selected: {options[i].text}")

            # Check if the button exists and click it
            button = check_button_exists()
            if button is None:
                print("Failed run")
                break

            button.click()
            print("Submit button clicked")

            # Wait for the new page to load completely
            wait_for_page_to_load()

            # Check whether there is data 
            if not is_not_active():
                active_carriers.append(text)

            # Re-fetch the dropdown options to avoid stale reference
            dropdown = Select(driver.find_element(By.ID, dropdown_id))
            options = dropdown.options  # Re-fetch options

    finally:
        driver.quit()

    # Print output
    print(active_carriers)
    return {
        'statusCode': 200,
        'body': active_carriers
    }
