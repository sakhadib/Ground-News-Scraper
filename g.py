import time
import csv
import sys
import os
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_article_data(url):
    # Setup WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Make sure the browser window is maximized
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(1)  # Wait for the page to load completely

        # Print completion message
        print("Page loaded successfully.")
        
        # Extract data using XPath
        article_data = {}

        # Extract Title
        article_data['title'] = driver.find_element(By.ID, "titleArticle").text
        print("Title extracted.")

        # Extract Total Source
        article_data['total_source'] = driver.find_element(By.XPATH, "/html/body/main/div/article/div/div/div[4]/div[1]/div/div/span[2]").text
        print("Total Source extracted.")

        # Extract Leaning Left
        article_data['leaning_left'] = driver.find_element(By.XPATH, "/html/body/main/div/article/div/div/div[4]/div[1]/div/span[2]").text
        print("Leaning Left extracted.")

        # Extract Leaning Right
        article_data['leaning_right'] = driver.find_element(By.XPATH, "/html/body/main/div/article/div/div/div[4]/div[1]/div/span[4]").text
        print("Leaning Right extracted.")

        # Extract Center
        article_data['center'] = driver.find_element(By.XPATH, "//*[@id='main']/div/article/div/div/div[4]/div[1]/div/span[6]").text
        print("Center extracted.")
        
        # Click and extract Left Points (with explicit wait to ensure the element is clickable)
        left_summary_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "left-summary-button")))

        ActionChains(driver).move_to_element(left_summary_button).click().perform()
        time.sleep(2)  # Wait for the points to load
        article_data['left_points'] = [point.text for point in driver.find_elements(By.XPATH, "/html/body/main/div/article/div/div/div[1]/div[2]/div[3]/div/div/div[2]/div[1]/ul/li")]
        print("Left Points extracted.")

        # Click and extract Center Points
        center_summary_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "center-summary-button")))
        ActionChains(driver).move_to_element(center_summary_button).click().perform()
        time.sleep(2)  # Wait for the points to load
        article_data['center_points'] = [point.text for point in driver.find_elements(By.XPATH, "/html/body/main/div/article/div/div/div[1]/div[2]/div[3]/div/div/div[2]/div[1]/ul/li")]
        print("Center Points extracted.")

        # Click and extract Right Points
        right_summary_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "right-summary-button")))
        ActionChains(driver).move_to_element(right_summary_button).click().perform()
        time.sleep(2)  # Wait for the points to load
        article_data['right_points'] = [point.text for point in driver.find_elements(By.XPATH, "/html/body/main/div/article/div/div/div[1]/div[2]/div[3]/div/div/div[2]/div[1]/ul/li")]
        print("Right Points extracted.")

        # Click on the 'more-stories' button until it disappears or becomes non-clickable
        while True:
            try:
                # Check if the "more stories" button exists and is clickable
                more_stories_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "more-stories")))
                ActionChains(driver).move_to_element(more_stories_button).click().perform()
                time.sleep(2)
                print("Loading more stories...")
            except:
                print("No more stories to load.")
                break

        # Extract Sources using the correct XPath structure
        article_data['sources'] = []
        source_elements = driver.find_elements(By.XPATH, "//div[@id='article-summary']")

        for source_element in source_elements:
            try:
                source = {}
                
                # Extract news title from the h4 element
                news_title_element = source_element.find_element(By.XPATH, ".//h4")
                source['news_title'] = news_title_element.text
                # print(f"  - News title: {source['news_title']}")
                
                # Extract news link from the h4's parent anchor tag
                news_link_element = source_element.find_element(By.XPATH, ".//a[h4]")
                source['news_link'] = news_link_element.get_attribute('href')
                # print(f"  - News link: {source['news_link']}")
                
                # Extract bias from the bias button
                bias_element = source_element.find_element(By.XPATH, ".//a[contains(@id, 'article-source-bias')]/div")
                source['bias'] = bias_element.text
                # print(f"  - Bias: {source['bias']}")
                
                # Extract source name for reference
                source_name_element = source_element.find_element(By.XPATH, ".//a[contains(@id, 'article-source-info')]//span")
                source['source_name'] = source_name_element.text
                # print(f"  - Source: {source['source_name']}")
                
                article_data['sources'].append(source)
                
            except Exception as e:
                print(f"  - Error extracting source data: {e}")
                continue

        print(f"Sources extracted. Total: {len(article_data['sources'])} sources")

        # Generate unique Story ID
        story_id = f"GN_{datetime.now().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8]}"
        print(f"Generated Story ID: {story_id}")

        # Save to CSV with improved error handling
        csv_filename = 'dataset.csv'
        
        try:
            # Check if file exists and if we can write to it
            file_exists = os.path.exists(csv_filename)
            
            # Flatten the sources data for CSV with Story ID as first column
            flattened_data = {
                'story_id': story_id,
                'title': article_data.get('title', ''),
                'total_source': article_data.get('total_source', ''),
                'leaning_left': article_data.get('leaning_left', ''),
                'leaning_right': article_data.get('leaning_right', ''),
                'center': article_data.get('center', ''),
                'left_points': ' | '.join(article_data.get('left_points', [])),
                'center_points': ' | '.join(article_data.get('center_points', [])),
                'right_points': ' | '.join(article_data.get('right_points', [])),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add sources data
            for i, source in enumerate(article_data.get('sources', []), 1):
                flattened_data[f'source_{i}_name'] = source.get('source_name', '')
                flattened_data[f'source_{i}_title'] = source.get('news_title', '')
                flattened_data[f'source_{i}_link'] = source.get('news_link', '')
                flattened_data[f'source_{i}_bias'] = source.get('bias', '')
            
            # Open file and write data
            mode = 'a' if file_exists else 'w'
            with open(csv_filename, mode, newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=flattened_data.keys())
                
                # Write header only if file is new
                if not file_exists:
                    writer.writeheader()
                    print("CSV header written.")
                
                writer.writerow(flattened_data)
                print("Data successfully saved to CSV.")
                
        except PermissionError:
            print(f"Permission denied: Cannot write to '{csv_filename}'. Please close the file if it's open in Excel or another application.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        fetch_article_data(url)
    else:
        print("Please provide a URL as a command-line argument.")
