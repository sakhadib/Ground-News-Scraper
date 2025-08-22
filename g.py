import time
import json
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

from newspaper import Article

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
        
        # Initialize summary points arrays
        article_data['left_points'] = []
        article_data['center_points'] = []
        article_data['right_points'] = []
        
        # Check and extract Left Points
        try:
            left_summary_button = driver.find_element(By.ID, "left-summary-button")
            if left_summary_button.is_enabled() and left_summary_button.is_displayed():
                ActionChains(driver).move_to_element(left_summary_button).click().perform()
                time.sleep(2)  # Wait for the points to load
                article_data['left_points'] = [point.text for point in driver.find_elements(By.XPATH, "/html/body/main/div/article/div/div/div[1]/div[2]/div[3]/div/div/div[2]/div[1]/ul/li")]
                print("Left Points extracted.")
            else:
                print("Left summary button not clickable. Keeping left_points as empty array.")
        except Exception as e:
            print("Left summary button not found. Keeping left_points as empty array.")

        # Check and extract Center Points
        try:
            center_summary_button = driver.find_element(By.ID, "center-summary-button")
            if center_summary_button.is_enabled() and center_summary_button.is_displayed():
                ActionChains(driver).move_to_element(center_summary_button).click().perform()
                time.sleep(2)  # Wait for the points to load
                article_data['center_points'] = [point.text for point in driver.find_elements(By.XPATH, "/html/body/main/div/article/div/div/div[1]/div[2]/div[3]/div/div/div[2]/div[1]/ul/li")]
                print("Center Points extracted.")
            else:
                print("Center summary button not clickable. Keeping center_points as empty array.")
        except Exception as e:
            print("Center summary button not found. Keeping center_points as empty array.")

        # Check and extract Right Points
        try:
            right_summary_button = driver.find_element(By.ID, "right-summary-button")
            if right_summary_button.is_enabled() and right_summary_button.is_displayed():
                ActionChains(driver).move_to_element(right_summary_button).click().perform()
                time.sleep(2)  # Wait for the points to load
                article_data['right_points'] = [point.text for point in driver.find_elements(By.XPATH, "/html/body/main/div/article/div/div/div[1]/div[2]/div[3]/div/div/div[2]/div[1]/ul/li")]
                print("Right Points extracted.")
            else:
                print("Right summary button not clickable. Keeping right_points as empty array.")
        except Exception as e:
            print("Right summary button not found. Keeping right_points as empty array.")

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
        # Extract Sources using the correct XPath structure
        article_data['sources'] = []

        # Find all source elements
        source_elements = driver.find_elements(By.ID, "article-summary")

        for source_element in source_elements:
            try:
                source = {}
                
                # Extract news title from the h4 element, relative to the article-summary
                news_title_element = source_element.find_element(By.XPATH, ".//a/h4")
                source['news_title'] = news_title_element.text
                
                # Extract news link from the anchor tag, relative to the article-summary
                news_link_element = source_element.find_element(By.XPATH, ".//a")
                source['news_link'] = news_link_element.get_attribute('href')
                
                # Extract bias from the bias element, relative to the article-summary
                try:
                    bias_element = source_element.find_element(By.XPATH, ".//a[contains(@id, 'article-source-bias')]/div")
                    source['bias'] = bias_element.text
                except Exception as e:
                    source['bias'] = "unknown"
                    print(f"  - Error extracting bias: {e}")
                    
                link = str(source['news_link'])
                article = Article(link)
                article.download()
                article.parse()
                source['actual_title'] = article.title
                source['authors'] = article.authors
                source['published_at'] = article.publish_date
                source['fulltext'] = article.text

                article_data['sources'].append(source)
                
            except Exception as e:
                print(f"  - Error extracting source data: {e}")
                continue

        print(f"Sources extracted. Total: {len(article_data['sources'])} sources")


        # Generate unique Story ID
        story_id = f"GN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        sid = str(story_id)
        print(f"Generated Story ID: {sid}")

        # Prepare structured data for JSON
        structured_data = {
            'story_id': sid,
            'metadata': {
                'title': article_data.get('title', ''),
                'timestamp': datetime.now().isoformat(),
                'url': url
            },
            'bias_distribution': {
                'total_sources': article_data.get('total_source', ''),
                'leaning_left': article_data.get('leaning_left', ''),
                'center': article_data.get('center', ''),
                'leaning_right': article_data.get('leaning_right', '')
            },
            'perspective_summaries': {
                'left': article_data.get('left_points', []),
                'center': article_data.get('center_points', []),
                'right': article_data.get('right_points', [])
            },
            'sources': article_data.get('sources', [])
        }

        # Save to JSON file in json/ directory
        json_filename = os.path.join('json', f"{sid}.json")
        
        try:
            # Ensure json directory exists
            os.makedirs('json', exist_ok=True)
            
            # Write JSON data with proper formatting
            with open(json_filename, 'w', encoding='utf-8') as file:
                json.dump(structured_data, file, indent=2, ensure_ascii=False)
                print(f"Data successfully saved to {json_filename}")
                
        except PermissionError:
            print(f"Permission denied: Cannot write to '{json_filename}'. Please check file permissions.")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

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
