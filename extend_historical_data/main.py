from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Optional: Automatically manage ChromeDriver
import os
import time
import logging
import glob
from datetime import datetime
import process_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize WebDriver with proper options
def init_driver(download_dir):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  #Headless
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument('--window-size=1920x1080')  
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-tools')
    chrome_options.add_argument('--no-zygote')
    chrome_options.add_argument('--disable-gpu')

    chrome_options.binary_location = os.environ.get('CHROME_BINARY_PATH', '/opt/chrome-linux/chrome')

    # Set download preferences
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(os.environ.get('CHROMEDRIVER_PATH', '/opt/chromedriver'))
    # service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(
        service=service,
        options=chrome_options
    )

# Wait for the page to load specific element
def wait_for_page_to_load(driver, by, value):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        print("The page has fully loaded.")
    except TimeoutException:
        print("Timed out waiting for the page to load.")

# Function to select dropdown options
def select_dropdown(driver, dropdown_id, display_text):
    dropdown = Select(driver.find_element(By.ID, dropdown_id))
    dropdown.select_by_visible_text(display_text)  # Select by the display text


# Function to select checkboxes
def select_checkbox(driver, checkbox_id):
    checkbox = driver.find_element(By.ID, checkbox_id)
    if not checkbox.is_selected():
        checkbox.click()

# Function to select checkboxes by value
def select_checkbox_by_value(driver, value):
    checkbox = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{value}']")
    if not checkbox.is_selected():
        checkbox.click()


def get_latest_file(directory, extension="csv"):
    # Get all files with the specified extension in the directory
    files = glob.glob(os.path.join(directory, f"*.{extension}"))
    if not files:
        return None
    # Sort files by modification time in descending order
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def wait_for_download_to_complete(directory, timeout=60):
    """
    Wait for a file to be fully downloaded by checking for the absence of .crdownload files.
    """
    time.sleep(5)
    for _ in range(timeout):
        if not any(f.endswith('.crdownload') for f in os.listdir(directory)):
            print("File Downloaded")
            return True
        time.sleep(1)
    return False

def scrape_departure():
    print("STARTING TO SCRAPE DEPARTURE DATA...")
    
    # Initialize the download directory path
    # download_dir = os.path.expanduser('~/Desktop/SMU/Y4S1/IS459/Project/DAG-ETL-Pipeline/extend_historical_data/departure_data')
    download_dir = '/home/ubuntu/scraper/departure_data'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    driver = init_driver(download_dir)
    try:
        url = 'https://www.transtats.bts.gov/ONTIME/Departures.aspx'
        driver.get(url)
        # wait for the cboAirport dropdown list to load
        wait_for_page_to_load(driver, By.ID, 'cboAirport')

        # Get all display words for options in the airport dropdown
        airport_dropdown = driver.find_element(By.ID, 'cboAirport')
        select_airport = Select(airport_dropdown)
        airports = [option.text for option in select_airport.options]  # Get the display text
         # half the airport list
        airports = airports[::4]

        # # Get all display words for options in the airline dropdown
        # airline_dropdown = driver.find_element(By.ID, 'cboAirline')
        # select_airline = Select(airline_dropdown)
        # airlines = [option.text for option in select_airline.options]  # Get the display text
        airlines = [
            'Alaska Airlines Inc. (AS)',
            'Allegiant Air (G4)',
            'American Airlines Inc. (AA)',
            'American Eagle Airlines Inc. (MQ)',
            'Comair Inc. (OH)',
            'Delta Airlines Inc. (DL)',
            'Endeavor Air Inc. (9E)',
            'Envoy Air (MQ)',
            'Frontier Airlines Inc. (F9)',
            'Hawaiian Airlines Inc. (HA)',
            'Horizon Air (QX)',
            'JetBlue Airways (B6)',
            'Mesa Airlines Inc. (YV)',
            'PSA Airlines Inc. (OH)',
            'Pinnacle Airlines Inc. (9E)',
            'Republic Airline (YX)',
            'SkyWest Airlines Inc. (OO)',
            'Southwest Airlines Co. (WN)',
            'Spirit Airlines (NK)',
            'United Airlines Inc. (UA)'
        ]


        # Print to check the display words
        print()
        print("Count Airports:", len(airports))
        print("Count Airlines:", len(airlines))

        # Select checkboxes for year, month, and day and statistics
        # all these are all boxes that needs to be checked once
        select_checkbox(driver, 'chkAllStatistics') 
        select_checkbox_by_value(driver, '2024')

        select_checkbox(driver, 'chkAllMonths')
        select_checkbox(driver, 'chkAllDays') 


        # Loop through all combinations to download CSV files
        for origin in airports:
            for airline in airlines:
                # Select the options for origin airport and airline
                select_dropdown(driver, 'cboAirport', origin)
                select_dropdown(driver, 'cboAirline', airline)

                # Submit or trigger search (click the search button)
                driver.find_element(By.ID, 'btnSubmit').click()

                # Wait for the page to load results, give it 30 seconds since we doing many years of data
                time.sleep(5)

                # Check for the presence of data or the "No data found" message
                if "No data found" in driver.page_source:
                    print(f"No data for {origin}, {airline}")
                else:
                    # Wait until the download button is available and click it
                    download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'DL_CSV')))
                    download_button.click()

                    # give it max 5mins to download
                    if wait_for_download_to_complete(download_dir, timeout=60):
                        latest_file = get_latest_file(download_dir)
                        print("latest file name (old): ".format(latest_file))
                        if latest_file:

                            # new_filename = os.path.join(download_dir, f'{origin}_{airline}.csv')
                            # Set the new filename with the timestamp
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            new_filename = os.path.join(download_dir, f'{timestamp}.csv')

                            os.rename(latest_file, new_filename)
                            print(f"Renamed {latest_file} to: {new_filename}")
                        else:
                            print("No new file found for renaming.")
                    else:
                        print("Download did not complete within the expected time.")

                print("Done for Origin Airport: {} Airline: {}".format(origin,airline))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

def scrape_arrival():
    print("STARTING TO SCRAPE ARRIVAL DATA...")
    
    # Initialize the download directory path
    # download_dir = os.path.expanduser('~/Desktop/SMU/Y4S1/IS459/Project/DAG-ETL-Pipeline/extend_historical_data/arrival_data')
    download_dir = '/home/ubuntu/scraper/arrival_data'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    driver = init_driver(download_dir)
    try:
        url = 'https://www.transtats.bts.gov/ONTIME/Arrivals.aspx'
        driver.get(url)
        # wait for the cboAirport dropdown list to load
        wait_for_page_to_load(driver, By.ID, 'cboAirport')

        # Get all display words for options in the airport dropdown
        airport_dropdown = driver.find_element(By.ID, 'cboAirport')
        select_airport = Select(airport_dropdown)
        airports = [option.text for option in select_airport.options]  # Get the display text

        # half the airport list
        airports = airports[::4]

        # # Get all display words for options in the airline dropdown
        # airline_dropdown = driver.find_element(By.ID, 'cboAirline')
        # select_airline = Select(airline_dropdown)
        # airlines = [option.text for option in select_airline.options]  # Get the display text
        airlines = [
            'Alaska Airlines Inc. (AS)',
            'Allegiant Air (G4)',
            'American Airlines Inc. (AA)',
            'American Eagle Airlines Inc. (MQ)',
            'Comair Inc. (OH)',
            'Delta Airlines Inc. (DL)',
            'Endeavor Air Inc. (9E)',
            'Envoy Air (MQ)',
            'Frontier Airlines Inc. (F9)',
            'Hawaiian Airlines Inc. (HA)',
            'Horizon Air (QX)',
            'JetBlue Airways (B6)',
            'Mesa Airlines Inc. (YV)',
            'PSA Airlines Inc. (OH)',
            'Pinnacle Airlines Inc. (9E)',
            'Republic Airline (YX)',
            'SkyWest Airlines Inc. (OO)',
            'Southwest Airlines Co. (WN)',
            'Spirit Airlines (NK)',
            'United Airlines Inc. (UA)'
        ]

        # Print to check the display words
        print("Count Airports:", len(airports))
        print("Count Airlines:", len(airlines))

        # Select checkboxes for year, month, and day and statistics
        # all these are all boxes that needs to be checked once
        select_checkbox(driver, 'chkAllStatistics') 
        select_checkbox_by_value(driver, '2024')

        select_checkbox(driver, 'chkAllMonths')
        select_checkbox(driver, 'chkAllDays') 


        # Loop through all combinations to download CSV files
        for origin in airports:
            for airline in airlines:
                # Select the options for origin airport and airline
                select_dropdown(driver, 'cboAirport', origin)
                select_dropdown(driver, 'cboAirline', airline)

                # Submit or trigger search (click the search button)
                driver.find_element(By.ID, 'btnSubmit').click()

                # Wait for the page to load results, give it 30 seconds since we doing many years of data
                time.sleep(5)

                # Check for the presence of data or the "No data found" message
                if "No data found" in driver.page_source:
                    print(f"No data for {origin}, {airline}")
                else:
                    # Wait until the download button is available and click it
                    download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'DL_CSV')))
                    download_button.click()

                    # give it max 5mins to download
                    if wait_for_download_to_complete(download_dir, timeout=60):
                        latest_file = get_latest_file(download_dir)
                        print("latest file name (old): ".format(latest_file))
                        if latest_file:
                            # new_filename = os.path.join(download_dir, f'{origin}_{airline}.csv')
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            new_filename = os.path.join(download_dir, f'{timestamp}.csv')

                            os.rename(latest_file, new_filename)
                            print(f"Renamed {latest_file} to: {new_filename}")
                        else:
                            print("No new file found for renaming.")
                    else:
                        print("Download did not complete within the expected time.")

                print("Done for Origin Airport: {} Airline: {}".format(origin,airline))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == '__main__':
    
    scrape_departure()
    scrape_arrival()
    process_data.main()
