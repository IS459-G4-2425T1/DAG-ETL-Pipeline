import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import boto3
import json
import os
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-tools')
    chrome_options.add_argument('--no-zygote')
    chrome_options.binary_location = os.environ.get('CHROME_BINARY_PATH', '/opt/chrome-linux/chrome')
    
    service = Service(os.environ.get('CHROMEDRIVER_PATH', '/opt/chromedriver'))
    
    return webdriver.Chrome(
        service=service,
        options=chrome_options
    )

# Check if the button exists
def check_button_exists(driver):
    try:
        button = driver.find_element(By.ID, 'submit')
        return button
    except NoSuchElementException:
        return None

# Wait for the page to load specific element
def wait_for_page_to_load(driver, by, value):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        print("The page has fully loaded.")
    except TimeoutException:
        print("Timed out waiting for the page to load.")

# Check if the current selection has no data
def is_not_active(driver):
    try:
        # Check for the <td> element by its text
        driver.find_element(By.XPATH, f"//td[contains(text(), 'No data available for the selected carrier, airport, or time period.')]")
        return True
    except NoSuchElementException:
        return False


# Main function to scrape the website
def scrape_website():
    driver = init_driver()
    dropdown_id = 'Carrier'
    try:
        url = 'https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp'
        driver.get(url)

        wait_for_page_to_load(driver, By.ID, 'submit')

        dropdown = Select(driver.find_element(By.ID, dropdown_id))
        options = dropdown.options
        length = len(options)
        active_carriers = []


        for i in range(1, length):
            dropdown.select_by_index(i)
            text = options[i].text
            # print(f"Selected: {options[i].text}")

            button = check_button_exists(driver)
            if button is None:
                # print('failed run')
                break

            button.click()
            # print('submit button clicked')

            wait_for_page_to_load(driver, By.ID, 'submit')

            # Re-fetch the dropdown after the button click
            dropdown = Select(driver.find_element(By.ID, dropdown_id))
            options = dropdown.options  # Re-fetch options

            if not is_not_active(driver): #bug here
                active_carriers.append(text)
            else:
                logger.info(f"No data for {options[i].text}")
            
            dropdown = Select(driver.find_element(By.ID, dropdown_id))
            options = dropdown.options

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
    finally:
        driver.quit()
    
    return active_carriers

# def process_data(data):
#     json_data = {}
    
#     for item in data:
#         start_index = item.rfind('(')
#         end_index = item.rfind(')')
        
#         if start_index != -1 and end_index != -1:
#             key = item[start_index + 1:end_index].strip()  # airline code
#             value = item[:start_index].strip()  # airline name
#             json_data[key] = value

#     filepath = "/tmp/active_carriers.json"
#     with open(filepath, 'w') as json_file:
#         json.dump(json_data, json_file, indent=4)
    
#     return filepath

def process_data(data):
    csv_data = []
    
    for item in data:
        start_index = item.rfind('(')
        end_index = item.rfind(')')
        
        if start_index != -1 and end_index != -1:
            key = item[start_index + 1:end_index].strip()  # airline code
            value = item[:start_index].strip()  # airline name
            csv_data.append([key, value])

    filepath = "/tmp/active_carriers.csv"
    with open(filepath, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Airline Code', 'Airline Name'])  # header
        writer.writerows(csv_data)  # write data rows
    
    return filepath

def upload_to_s3(filepath, bucket_name, filename):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(filepath, bucket_name, filename)
    except Exception as e:
        logger.error(f"Failed to upload {filename} to S3: {str(e)}")

def delete_local_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print(f"The file {filepath} does not exist")

# bucket_name = "active-carriers-data"
#carrier_filename = "active_carriers.json"

# AWS Lambda handler
def lambda_handler(event, context):
    active_carriers = scrape_website()
    filepath = process_data(active_carriers)
    # Fix the order and add the filename parameter
    upload_to_s3(filepath, "active-carriers-data", "active_carriers.csv")
    delete_local_file(filepath)

if __name__ == "__main__":
   active_carriers = scrape_website()
   filepath = process_data(active_carriers)
   upload_to_s3(filepath, "active-carriers-data", "active_carriers.csv")
   delete_local_file(filepath)

