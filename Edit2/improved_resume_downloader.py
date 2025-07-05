#!/usr/bin/env python3
"""
Improved Resume Downloader for LinkedIn Job Applications
Handles click interception errors and uses JavaScript execution
Now with pagination support to process all pages
"""

import os
import time
import re
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime
import logging
import csv
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('improved_downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImprovedResumeDownloader:
    def __init__(self, linkedin_email, linkedin_password):
        self.linkedin_email = linkedin_email
        self.linkedin_password = linkedin_password
        self.driver = None
        self.wait = None
        self.download_folder = "FSD_resume"
        self.job_id = "4254395344"
        self.processed_candidates = set()  # Track processed candidates
        
        # Create download folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            logger.info(f"Created download folder: {self.download_folder}")
    
    def setup_driver(self):
        """Set up Chrome driver with enhanced anti-detection measures"""
        chrome_options = Options()
        
        # Enhanced anti-detection options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-field-trial-config")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Set download preferences
        prefs = {
            "download.default_directory": os.path.abspath(self.download_folder),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Execute anti-detection scripts
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        self.wait = WebDriverWait(self.driver, 20)
        
        logger.info("Chrome driver setup completed with enhanced anti-detection")
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add random delay to simulate human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_like_typing(self, element, text):
        """Type text like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def login_to_linkedin(self):
        """Login to LinkedIn with human-like behavior"""
        try:
            logger.info("Navigating to LinkedIn login page...")
            self.driver.get("https://www.linkedin.com/login")
            self.random_delay(2, 4)
            
            # Wait for login form and enter credentials
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_field = self.driver.find_element(By.ID, "password")
            
            # Clear fields first
            email_field.clear()
            password_field.clear()
            self.random_delay(0.5, 1)
            
            # Type credentials like a human
            self.human_like_typing(email_field, self.linkedin_email)
            self.random_delay(0.5, 1)
            self.human_like_typing(password_field, self.linkedin_password)
            self.random_delay(1, 2)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            self.random_delay(3, 5)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                logger.error("Login failed - please check credentials")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return False
    
    def navigate_to_applicants_page(self):
        """Navigate to the job applicants page"""
        try:
            logger.info("Navigating to job applicants page...")
            applicants_url = f"https://www.linkedin.com/hiring/jobs/{self.job_id}/applicants/"
            self.driver.get(applicants_url)
            self.random_delay(5, 8)
            
            # Wait for applicants list to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.artdeco-list")))
            logger.info("Applicants list loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to applicants page: {str(e)}")
            return False
    
    def click_with_js(self, element):
        """Click element using JavaScript to bypass click interception"""
        try:
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            logger.warning(f"JavaScript click failed: {str(e)}")
            return False
    
    def scroll_and_wait(self, element):
        """Scroll to element and wait for it to be clickable"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.random_delay(1, 2)
            
            # Wait for element to be clickable
            self.wait.until(EC.element_to_be_clickable(element))
            return True
        except Exception as e:
            logger.warning(f"Scroll and wait failed: {str(e)}")
            return False
    
    def get_next_page_button(self):
        """Find the next page button"""
        try:
            # Look for next page button
            next_button_selectors = [
                "//button[contains(@aria-label, 'Next')]",
                "//button[contains(text(), 'Next')]",
                "//a[contains(@aria-label, 'Next')]",
                "//a[contains(text(), 'Next')]",
                "//button[@aria-label='Next page']",
                "//a[@aria-label='Next page']"
            ]
            
            for selector in next_button_selectors:
                try:
                    next_button = self.driver.find_element(By.XPATH, selector)
                    if next_button.is_displayed() and next_button.is_enabled():
                        return next_button
                except NoSuchElementException:
                    continue
            
            return None
        except Exception as e:
            logger.warning(f"Error finding next page button: {str(e)}")
            return None
    
    def click_next_page(self):
        """Click the next page button"""
        try:
            next_button = self.get_next_page_button()
            if next_button:
                logger.info("Clicking next page...")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                self.random_delay(1, 2)
                
                try:
                    next_button.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", next_button)
                
                self.random_delay(3, 5)
                
                # Wait for new content to load
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.artdeco-list")))
                logger.info("Next page loaded successfully")
                return True
            else:
                logger.info("No next page button found - reached end of results")
                return False
                
        except Exception as e:
            logger.error(f"Error clicking next page: {str(e)}")
            return False
    
    def get_candidate_name(self, candidate_element):
        """Extract candidate name from the candidate element"""
        try:
            # Try to get name from the candidate list item
            name_selectors = [
                ".//span[contains(@class, 'name')]",
                ".//div[contains(@class, 'name')]",
                ".//a[contains(@href, '/in/')]",
                ".//span[contains(@class, 'artdeco-entity-lockup__title')]"
            ]
            
            for selector in name_selectors:
                try:
                    name_elem = candidate_element.find_element(By.XPATH, selector)
                    name = name_elem.text.strip()
                    if name:
                        return name
                except NoSuchElementException:
                    continue
            
            return None
        except Exception as e:
            logger.warning(f"Error extracting candidate name: {str(e)}")
            return None
    
    def download_resume_for_candidate(self, candidate_element, candidate_name, candidate_index):
        """Download resume for a specific candidate with improved click handling"""
        try:
            # Check if we've already processed this candidate
            if candidate_name in self.processed_candidates:
                logger.info(f"Skipping already processed candidate: {candidate_name}")
                return False
            
            # Click on candidate to load their details
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", candidate_element)
            self.random_delay(1, 2)
            
            # Try multiple click methods
            try:
                candidate_element.click()
            except ElementClickInterceptedException:
                self.click_with_js(candidate_element)
            
            self.random_delay(2, 3)
            
            # Extract candidate name from page if not provided
            if not candidate_name:
                try:
                    name_elem = self.driver.find_element(By.XPATH, "//h2[contains(text(), \"'s application\")] | //h3[contains(text(), \"'s application\")]")
                    candidate_name = name_elem.text.replace("'s application", '').strip()
                except NoSuchElementException:
                    candidate_name = f"Candidate_{candidate_index}"
            
            logger.info(f"Processing resume for {candidate_name}")
            
            # Look for resume section with multiple strategies
            resume_section = None
            found = False
            
            # Strategy 1: Direct resume selectors
            resume_selectors = [
                "//section[contains(., 'Resume')]",
                "//section[contains(., 'CV')]",
                "//div[contains(., 'Resume')]",
                "//div[contains(., 'CV')]",
                "//div[contains(@class, 'resume')]",
                "//div[contains(@class, 'cv')]"
            ]
            
            for selector in resume_selectors:
                try:
                    resume_section = self.driver.find_element(By.XPATH, selector)
                    if resume_section.is_displayed():
                        found = True
                        break
                except NoSuchElementException:
                    continue
            
            # Strategy 2: Scroll and search
            if not found:
                self.driver.execute_script("window.scrollBy(0, 500);")
                self.random_delay(1, 2)
                
                for selector in resume_selectors:
                    try:
                        resume_section = self.driver.find_element(By.XPATH, selector)
                        if resume_section.is_displayed():
                            found = True
                            break
                    except NoSuchElementException:
                        continue
            
            # Strategy 3: Look for download links directly
            if not found:
                download_link_selectors = [
                    "//a[contains(@href, 'ambry')]",
                    "//a[contains(text(), 'Download')]",
                    "//a[contains(@aria-label, 'Download')]",
                    "//button[contains(text(), 'Download')]"
                ]
                
                for selector in download_link_selectors:
                    try:
                        download_btn = self.driver.find_element(By.XPATH, selector)
                        if download_btn.is_displayed():
                            resume_section = download_btn
                            found = True
                            break
                    except NoSuchElementException:
                        continue
            
            if found and resume_section:
                # Scroll to resume section
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", resume_section)
                self.random_delay(1, 2)
                
                # Look for download button with multiple strategies
                download_btn = None
                download_selectors = [
                    ".//a[contains(@href, 'ambry')]",
                    ".//a[contains(text(), 'Download')]",
                    ".//button[contains(text(), 'Download')]",
                    ".//a[contains(@aria-label, 'Download')]",
                    ".//button[contains(@aria-label, 'Download')]"
                ]
                
                # If resume_section is already a download button
                if resume_section.tag_name in ['a', 'button']:
                    download_btn = resume_section
                else:
                    # Search within resume section
                    for selector in download_selectors:
                        try:
                            download_btn = resume_section.find_element(By.XPATH, selector)
                            break
                        except NoSuchElementException:
                            continue
                
                if download_btn:
                    # Most robust: Clean and split the name, use first and last word (alphabetic only)
                    words = [re.sub(r'[^A-Za-z]', '', w) for w in candidate_name.split() if re.sub(r'[^A-Za-z]', '', w)]
                    if len(words) >= 2:
                        first, last = words[0], words[-1]
                    elif len(words) == 1:
                        first = last = words[0]
                    else:
                        first = last = f"Candidate_{candidate_index}"
                    filename = f"{first}_{last}.pdf"
                    
                    # Check if file already exists
                    filepath = os.path.join(self.download_folder, filename)
                    if os.path.exists(filepath):
                        logger.info(f"Resume already exists for {candidate_name}: {filename}")
                        self.processed_candidates.add(candidate_name)
                        return True
                    
                    # Try multiple click methods
                    logger.info(f"Downloading resume for {candidate_name}")
                    
                    # Method 1: Regular click
                    try:
                        download_btn.click()
                    except ElementClickInterceptedException:
                        # Method 2: JavaScript click
                        if not self.click_with_js(download_btn):
                            # Method 3: Action chains
                            try:
                                ActionChains(self.driver).move_to_element(download_btn).click().perform()
                            except Exception:
                                # Method 4: Direct URL access
                                download_url = download_btn.get_attribute("href")
                                if download_url:
                                    self.driver.get(download_url)
                    
                    self.random_delay(3, 5)
                    
                    # Check if file was downloaded
                    if os.path.exists(filepath):
                        logger.info(f"Successfully downloaded resume for {candidate_name}: {filename}")
                        self.processed_candidates.add(candidate_name)
                        return True
                    else:
                        logger.warning(f"Download may have failed for {candidate_name}")
                        return False
                else:
                    logger.warning(f"No download button found for {candidate_name}")
                    return False
            else:
                logger.warning(f"No resume section found for {candidate_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading resume for candidate {candidate_name}: {str(e)}")
            return False
    
    def download_all_resumes(self):
        """Download resumes for all candidates on the current page"""
        try:
            logger.info("Starting resume download process...")
            
            # Navigate to applicants page
            if not self.navigate_to_applicants_page():
                return False
            
            # Get all candidate items
            candidate_items = self.driver.find_elements(By.CSS_SELECTOR, "ul.artdeco-list > li")
            logger.info(f"Found {len(candidate_items)} candidates")
            
            successful_downloads = 0
            
            for i, candidate in enumerate(candidate_items, 1):
                try:
                    logger.info(f"Processing candidate {i}/{len(candidate_items)}")
                    
                    # Download resume for this candidate
                    if self.download_resume_for_candidate(candidate, None, i):
                        successful_downloads += 1
                    
                    self.random_delay(2, 4)
                    
                except Exception as e:
                    logger.error(f"Error processing candidate {i}: {str(e)}")
                    continue
            
            logger.info(f"Successfully downloaded {successful_downloads} resumes out of {len(candidate_items)} candidates")
            return True
            
        except Exception as e:
            logger.error(f"Error in download_all_resumes: {str(e)}")
            return False
    
    def check_and_process_all_pages(self):
        """Check if more pages are available by clicking the next page number and process them all"""
        try:
            logger.info("Starting multi-page resume download process (by page number)...")
            
            # Navigate to applicants page
            if not self.navigate_to_applicants_page():
                return False
            
            page_number = 1
            total_successful_downloads = 0
            total_candidates_processed = 0
            
            while True:
                logger.info(f"Processing page {page_number}")
                
                # Get all candidate items on current page
                candidate_items = self.driver.find_elements(By.CSS_SELECTOR, "ul.artdeco-list > li")
                logger.info(f"Found {len(candidate_items)} candidates on page {page_number}")
                
                if not candidate_items:
                    logger.info("No candidates found on current page")
                    break
                
                page_successful_downloads = 0
                
                for i, candidate in enumerate(candidate_items, 1):
                    try:
                        logger.info(f"Processing candidate {total_candidates_processed + i} on page {page_number}")
                        
                        # Download resume for this candidate
                        if self.download_resume_for_candidate(candidate, None, total_candidates_processed + i):
                            page_successful_downloads += 1
                            total_successful_downloads += 1
                        
                        total_candidates_processed += 1
                        self.random_delay(2, 4)
                        
                    except Exception as e:
                        logger.error(f"Error processing candidate {total_candidates_processed + i}: {str(e)}")
                        total_candidates_processed += 1
                        continue
                
                logger.info(f"Page {page_number}: Downloaded {page_successful_downloads} resumes out of {len(candidate_items)} candidates")
                
                # Try to go to the next page by clicking the next page number (robust XPaths and click strategies)
                next_page_number = page_number + 1
                next_page_elem = None
                next_page_xpaths = [
                    f"//button[text()='{next_page_number}']",
                    f"//li[.//button[text()='{next_page_number}']]//button[text()='{next_page_number}']",
                    f"//li[.//span[text()='{next_page_number}']]//span[text()='{next_page_number}']",
                    f"//a[text()='{next_page_number}']",
                    f"//span[text()='{next_page_number}']",
                    f"//div[text()='{next_page_number}']"
                ]
                clicked = False
                for xpath in next_page_xpaths:
                    try:
                        elem = self.driver.find_element(By.XPATH, xpath)
                        if elem.is_displayed() and elem.is_enabled():
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                            self.random_delay(1, 2)
                            try:
                                elem.click()
                                clicked = True
                                logger.info(f"Clicked next page number {next_page_number} using normal click.")
                                break
                            except Exception as e1:
                                logger.warning(f"Normal click failed: {e1}")
                                # Try parent click
                                try:
                                    parent = elem.find_element(By.XPATH, './..')
                                    parent.click()
                                    clicked = True
                                    logger.info(f"Clicked next page number {next_page_number} using parent click.")
                                    break
                                except Exception as e2:
                                    logger.warning(f"Parent click failed: {e2}")
                                    # Try JavaScript click
                                    try:
                                        self.driver.execute_script("arguments[0].click();", elem)
                                        clicked = True
                                        logger.info(f"Clicked next page number {next_page_number} using JavaScript click.")
                                        break
                                    except Exception as e3:
                                        logger.warning(f"JavaScript click failed: {e3}")
                                        continue
                    except Exception:
                        continue
                if clicked:
                    self.random_delay(3, 5)
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.artdeco-list")))
                    logger.info(f"Successfully moved to page {next_page_number}")
                    page_number += 1
                else:
                    # Log the pagination area's HTML for debugging
                    try:
                        pagination_html = self.driver.find_element(By.XPATH, "//*[contains(@class, 'pagination') or contains(@class, 'artdeco-pagination')]").get_attribute('outerHTML')
                        logger.info(f"Pagination area HTML:\n{pagination_html}")
                    except Exception:
                        logger.info("Could not find pagination area to log HTML.")
                    logger.info("No further page numbers found or could not interact - reached end of results")
                    break
            
            logger.info(f"Total: Successfully downloaded {total_successful_downloads} resumes out of {total_candidates_processed} candidates across {page_number} pages")
            return True
            
        except Exception as e:
            logger.error(f"Error in check_and_process_all_pages: {str(e)}")
            return False
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser driver closed")
            except:
                pass

def main():
    """Main function to run the improved resume downloader"""
    # Load credentials from environment variables
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    
    if not linkedin_email or not linkedin_password:
        logger.error("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables")
        return
    
    downloader = ImprovedResumeDownloader(linkedin_email, linkedin_password)
    
    try:
        # Setup driver
        downloader.setup_driver()
        
        # Login to LinkedIn
        if not downloader.login_to_linkedin():
            logger.error("Failed to login to LinkedIn")
            return
        
        # Download all resumes
        success = downloader.check_and_process_all_pages()
        
        if success:
            logger.info("Resume download process completed successfully")
        else:
            logger.error("Resume download process failed")
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        downloader.close_driver()

if __name__ == "__main__":
    main() 