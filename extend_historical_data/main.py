from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize WebDriver with proper options
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-tools')
    chrome_options.add_argument('--no-zygote')

    # Define the download directory path
    download_dir = os.path.abspath('downloads')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Set download preferences
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(os.environ.get('CHROMEDRIVER_PATH', '/opt/chromedriver'))
    
    return webdriver.Chrome(
        service=service,
        options=chrome_options
    ), download_dir

# Wait for the page to load specific element
def wait_for_page_to_load(driver, by, value):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        print("The page has fully loaded.")
    except TimeoutException:
        print("Timed out waiting for the page to load.")

# Function to select dropdown options
def select_dropdown(driver, dropdown_id, value):
    dropdown = Select(driver.find_element(By.ID, dropdown_id))
    dropdown.select_by_value(value)


# Function to select checkboxes
def select_checkbox(driver, checkbox_id):
    checkbox = driver.find_element(By.ID, checkbox_id)
    if not checkbox.is_selected():
        checkbox.click()


def lambda_handler(event, context):
    logging.info("STARTING MAIN FUNCTION...")
    driver, download_dir = init_driver()
    try:
        url = 'https://www.transtats.bts.gov/ONTIME/Departures.aspx'
        driver.get(url)
        # wait for the cboAirport dropdown list to load
        wait_for_page_to_load(driver, By.ID, 'cboAirport')

        # List of all parameters to loop through
        origin_airports = ['ORD', 'SFO']  # Add more as needed
        airlines = ['AA']  # Add more airline codes as needed
        years = range(2012, 2013)

        # Loop through all combinations to download CSV files
        for origin in origin_airports:
            for airline in airlines:
                for year in years:
                    logging.info("I am here now...")
                    # Select the options for origin airport and airline
                    select_dropdown(driver, 'cboAirport', origin)
                    select_dropdown(driver, 'cboAirline', airline)

                    # Select checkboxes for year, month, and day
                    select_checkbox(driver, f'chkYears_{year}')  # Replace with actual ID pattern
                    select_checkbox(driver, 'chkAllMonths')  # Replace with actual ID pattern
                    select_checkbox(driver, 'chkAllDays')  # Replace with actual ID pattern

                    # Submit or trigger search (click the search button)
                    driver.find_element(By.ID, 'btnSubmit').click()

                    # Wait for the page to load results
                    time.sleep(5)

                    # Check for the presence of data or the "No data found" message
                    if "No data found" in driver.page_source:
                        print(f"No data for {origin}, {airline}, {year}")
                    else:
                        # Wait until the download button is available and click it
                        download_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'DL_CSV')))
                        download_button.click()

                        # Wait for the download to complete (adjust time as needed)
                        time.sleep(15)

                        # Rename the downloaded file to the desired format
                        original_filename = os.path.join(download_dir, 'On_Time_Reporting.csv')
                        new_filename = os.path.join(download_dir, f'{origin}_{airline}_{year}.csv')
                        if os.path.exists(original_filename):
                            os.rename(original_filename, new_filename)
                            print(f"Downloaded: {new_filename}")
                logging.info("End of {} year...".format(year))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
    pass


if __name__ == '__main__':
    logging.info('reach name -- main')
    pass
