from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv

# Selenium Wire configuration to use a proxy
proxy_username = 'username'
proxy_password = 'password'
seleniumwire_options = {
    'proxy': {
        'http': f'http://{proxy_username}:{proxy_password}@city.smartproxy.com:21250',
        'verify_ssl': False,
    },
}

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, seleniumwire_options=seleniumwire_options)

# URL of the web page
url = "https://www.google.com/maps/search/falafel+in+london/"

# Open the web page
driver.get(url)

try: 
    button = driver.find_element(By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc']") 
    button.click()
    print("Clicked consent to cookies.") 
except: 
    print("No consent required.")

# Set an implicit wait time to wait for JavaScript to render
driver.implicitly_wait(30)  # Wait for max 30 seconds

# Take a screenshot after the content you want is loaded
screenshot_path = '/path/to/your/destination/screenshot.png'
driver.save_screenshot(screenshot_path)
print(f"Screenshot saved to {screenshot_path}")

def scroll_panel_with_page_down(driver, panel_xpath, presses, pause_time):
    """
    Scrolls within a specific panel by simulating Page Down key presses.

    :param driver: The Selenium WebDriver instance.
    :param panel_xpath: The XPath to the panel element.
    :param presses: The number of times to press the Page Down key.
    :param pause_time: Time to pause between key presses, in seconds.
    """
    # Find the panel element
    panel_element = driver.find_element(By.XPATH, panel_xpath)
    
    # Ensure the panel is in focus by clicking on it
    # Note: Some elements may not need or allow clicking to focus. Adjust as needed.
    actions = ActionChains(driver)
    actions.move_to_element(panel_element).click().perform()

    # Send the Page Down key to the panel element
    for _ in range(presses):
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(pause_time)

panel_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div"
scroll_panel_with_page_down(driver, panel_xpath, presses=5, pause_time=1)

# Get the page HTML source
page_source = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all elements using its class
titles = soup.find_all(class_="hfpxzc")
ratings = soup.find_all(class_='MW4etd')
reviews = soup.find_all(class_='UY7F9')
services = soup.find_all(class_='Ahnjwc')

# Print the number of places found
elements_count = len(titles)
print(f"Number of places found: {elements_count}")

# Specify the CSV file path
csv_file_path = '/path/to/your/destination/places.csv'

# Open a CSV file in write mode
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write the header row (optional, adjust according to your data)
    csv_writer.writerow(['Place', 'Rating', 'Reviews', 'Service options'])
    
    # Write the extracted data
    for i, title in enumerate(titles):
        title = title.get('aria-label')
        rating = (ratings[i].text + "/5") if i < len(ratings) else 'N/A' # Ensure we have a rating and reviews for each title, defaulting to 'N/A' if not found
        review_count = reviews[i].text if i < len(reviews) else 'N/A'
        service = services[i].text if i < len(services) else 'N/A'

        # Write a row to the CSV file
        if title:
            csv_writer.writerow([title, rating, review_count, service])

print(f"Data has been saved to '{csv_file_path}'")

# Close the WebDriver
driver.quit()
