from typing import Dict, Any
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from .base_scraper import BaseScraper
import logging

class OpenSubtitlesWebScraper(BaseScraper):
    """Web scraper for OpenSubtitles.org as API fallback."""
    
    BASE_URL = "https://www.opensubtitles.org"
    
    def __init__(self):
        """Initialize the web scraper."""
        super().__init__()
        self._setup_driver()
        self.logger = logging.getLogger(__name__)
        
    def _setup_driver(self):
        """Configure Selenium WebDriver."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--proxy-server="direct://"')
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--start-maximized')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Add additional preferences to avoid detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = webdriver.ChromeService()
        self.driver = webdriver.Chrome(
            service=service,
            options=options
        )
        
        # Execute CDP commands to prevent detection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Remove webdriver flag
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        
        # Add error handling for timeouts
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        
    def _handle_cookie_consent(self):
        """Handle cookie consent popup if present."""
        try:
            cookie_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.cookie-consent-accept"))
            )
            cookie_button.click()
        except TimeoutException:
            self.logger.debug("No cookie consent button found")
        
    def _random_delay(self):
        """Add random delay between requests to avoid rate limiting."""
        time.sleep(random.uniform(2, 5))
        
    def _get_download_link(self, element) -> str:
        """Extract actual download link from subtitle element."""
        try:
            # Wait for download button and click it
            download_btn = element.find_element(By.CSS_SELECTOR, "a.download-subtitle")
            ActionChains(self.driver).move_to_element(download_btn).perform()
            time.sleep(1)  # Wait for any JS to execute
            
            # Get the actual download URL
            download_url = download_btn.get_attribute('href')
            if not download_url:
                raise ValueError("Download URL not found")
                
            return download_url
            
        except Exception as e:
            self.logger.error(f"Failed to get download link: {str(e)}")
            raise
            
    def _process_subtitle_element(self, elem) -> dict:
        """Process a single subtitle element."""
        try:
            title_elem = elem.find_element(By.CSS_SELECTOR, "td.name")
            title = title_elem.text.strip()
            
            # Get download URL before creating result dict
            download_url = self._get_download_link(elem)
            
            return {
                'attributes': {
                    'files': [{
                        'file_id': elem.get_attribute('id').split('-')[1],
                        'download_url': download_url
                    }],
                    'feature_details': {
                        'title': title
                    }
                }
            }
        except Exception as e:
            self.logger.warning(f"Error processing subtitle element: {e}")
            return None
            
    def search(self, url: str, language: str = 'en') -> Dict[str, Any]:
        """Search for subtitles."""
        search_url = f"{url}/sublanguageid-{language}"
        self.driver.get(search_url)
        self._handle_cookie_consent()
        self._random_delay()
        
        try:
            # Wait for subtitle elements
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr.change"))
            )
            
            # Get all subtitle elements
            subtitle_elements = self.driver.find_elements(By.CSS_SELECTOR, "tr.change")
            
            results = []
            for elem in subtitle_elements:
                result = self._process_subtitle_element(elem)
                if result:
                    results.append(result)
                    
            return {'data': results}
            
        except (TimeoutException, Exception) as e:
            self.logger.error(f"Search failed: {str(e)}")
            return {'data': []}
        
    def download(self, file_id: str) -> Dict[str, str]:
        """Get download link using web scraping."""
        download_url = f"{self.BASE_URL}/en/subtitleserve/sub/{file_id}"
        
        # Visit the download page
        self.driver.get(download_url)
        self._random_delay()
        
        # Wait for and click the download button
        download_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.download"))
        )
        actual_download_url = download_button.get_attribute('href')
        
        self.download_count += 1
        return {'link': actual_download_url}
        
    def __del__(self):
        """Clean up the web driver."""
        if hasattr(self, 'driver'):
            self.driver.quit() 