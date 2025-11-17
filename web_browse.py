import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def browse_web(url):
    """
    Browse a web page using Selenium for dynamic content and return the text content.
    Falls back to requests if Selenium fails.
    """
    try:
        # Try Selenium for dynamic content
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        # Extract main text content
        text = soup.get_text(separator='\n', strip=True)
        return text[:2000]  # Limit to 2000 chars for brevity
    except Exception as e:
        # Fallback to requests
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            return text[:2000]
        except Exception as e2:
            return f"Error browsing {url}: Selenium - {e}, Requests - {e2}"
