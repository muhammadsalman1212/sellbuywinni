import csv
import os
import pandas as pd
import os
import requests
from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs, urlencode, urljoin



description_contact_info = 'Ainsley Yoong\nSellBuyWinnipeg.com\nReal Broker'
enter_the_hours = int(input("[HOW MUCH AFTER YOU ANT TO CHECK IT?]: "))





# Function to convert date to website format
def format_date(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %I:%M %p")



def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



def delete_images(folder_path):
    # Check if folder exists
    if os.path.exists(folder_path):
        # Iterate through all files in folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")



# Function to download image
def download_image(url, folder_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_path, url.split("/")[-1]), "wb") as f:
            f.write(response.content)
            print(f"Downloaded: {url}")

folder_path = r"C:\Users\ainsl\PycharmProjects\sellbuywinni_fbautomation\website_images"
create_folder(folder_path)



def extract_specific_url_part(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Remove specific query parameters you don't need
    query_params.pop('listingSort', None)
    query_params.pop('layoutType', None)
    query_params.pop('mapType', None)
    query_params.pop('page', None)
    query_params.pop('pageSize', None)
    query_params.pop('isSearching', None)
    query_params.pop('siteId', None)
    query_params.pop('listingSource', None)
    query_params.pop('condition', None)
    query_params.pop('uiConfig', None)
    query_params.pop('zoom', None)
    query_params.pop('mapSearch', None)
    query_params.pop('mapRadius[]', None)
    query_params.pop('timeline', None)
    query_params.pop('listingSortOptions', None)
    query_params.pop('timezone', None)
    query_params.pop('source', None)

    # Convert the modified query params back to URL encoded string
    encoded_query_params = urlencode(query_params, doseq=True)

    # Reconstruct the URL
    new_url = parsed_url._replace(query=encoded_query_params).geturl()

    return new_url


# User input for date
input_date = input("Enter date (MM/DD/YYYY): ")
input_time = input("Enter time (HH:MM AM/PM): ")

# Modify the ChromeOptions to include the desired profile directory
profile_directory = r"C:\Users\ainsl\AppData\Local\Google\Chrome\User Data\Profile 3"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(fr'user-data-dir={profile_directory}')

checking_number = 1

already_scraped_links_list = []

csv_scrape_list_checker = []


csv_file = 'scrape_links.csv'

# Read CSV file into DataFrame
df = pd.read_csv(csv_file)

# Extract 'Scraped_link' column into a list using a for loop
for link in df['Scraped_link']:
    csv_scrape_list_checker.append(link)
driver = webdriver.Chrome(options=chrome_options)
# Display the list of scraped links
print(csv_scrape_list_checker)

driver.get("https://sellbuywinnipeg.com/listing")
time.sleep(20)
driver.execute_script("window.open('https://www.facebook.com/marketplace/create/rental','_blank')")
driver.switch_to.window(driver.window_handles[0])

# Switch to the newly opened tab (Facebook Marketplace)


# Launch Chrome WebDriver with the specified profile

while True:
    print(f"Checking: {checking_number} Time")

    driver.get("https://sellbuywinnipeg.com/listing")
    time.sleep(20)



    try:
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
    except:
        pass
    try:
        time.sleep(12)
        driver.find_element(By.XPATH, "//label[text()='Default']").click()
    except:
        time.sleep(23)
        driver.find_element(By.XPATH, "//label[text()='Default']").click()
    try:
        time.sleep(10)
        driver.find_element(By.XPATH, "//span[text()='Newest Listings']").click()
    except:
        time.sleep(20)
        driver.find_element(By.XPATH, "//span[text()='Newest Listings']").click()
    time.sleep(20)

    all_properties = []
    all_prices_list = []

    # Fetching all posts and prices
    all_new_posts = driver.find_elements(By.XPATH, '//h3[@class="house-address"]//a')
    prices = driver.find_elements(By.XPATH, '//p[@class="house-price"]')

    for post, price in zip(all_new_posts, prices):
        all_post_href = post.get_attribute('href')
        print(all_post_href)
        all_properties.append(all_post_href)
        price_text = price.text
        print(price_text)
        all_prices_list.append(price_text)

    # Iterate through each property URL and fetch details
    for property_url, price in zip(all_properties, all_prices_list):
        time.sleep(5)
        driver.get(property_url)
        time.sleep(5)
        # title
        try:
            time.sleep(2)
            title = driver.find_element(By.XPATH, '//h1[@class="address-container black top-address"]').text
            if title == "":
                title = "N/A"
        except:
            time.sleep(5)
            title = driver.find_element(By.XPATH, '//h1[@class="address-container black top-address"]').text
            if title == "":
                title = "N/A"
                pass

        # Get property type

        try:
            time.sleep(2)
            property_type = driver.find_element(By.XPATH,
                                                "//h5[@class='info-content']/span[@class='info-title' and text()='Property Type']/following-sibling::span[@class='info-data']").text
            if property_type == "":
                property_type = "N/A"
        except:
            time.sleep(6)
            property_type = driver.find_element(By.XPATH,
                                                "//h5[@class='info-content']/span[@class='info-title' and text()='Property Type']/following-sibling::span[@class='info-data']").text
            if property_type == "":
                property_type = "N/A"
                pass


        # listing_status
        # listing_status = driver.find_element(By.XPATH,
        #                                      "//h5[@class='info-content']/span[@class='info-title' and text()='Listing Status']/following-sibling::span[@class='info-data']").text
        # Square Footage
        try:
            time.sleep(2)
            square_footage = driver.find_element(By.XPATH,
                                                 "//h5[@class='info-content']/span[@class='info-title' and text()='Square Footage']/following-sibling::span[@class='info-data']").text
            if square_footage == "":
                square_footage = "N/A"
        except:
            time.sleep(5)
            square_footage = driver.find_element(By.XPATH,
                                                 "//h5[@class='info-content']/span[@class='info-title' and text()='Square Footage']/following-sibling::span[@class='info-data']").text
            if square_footage == "":
                square_footage = "N/A"
                pass

        # Subdivision
        # subdivision = driver.find_element(By.XPATH,
        #                                   "//h5[@class='info-content']/span[@class='info-title' and text()='Subdivision']/following-sibling::span[@class='info-data']").text
        # style
        try:
            style = driver.find_element(By.XPATH,
                                        "//h5[@class='info-content']/span[@class='info-title' and text()='Style']/following-sibling::span[@class='info-data']").text
        except:
            style = "N/A"
            pass
        # Originating Board

        # originating_board = driver.find_element(By.XPATH,
        #                                         "//h5[@class='info-content']/span[@class='info-title' and text()='Originating Board']/following-sibling::span[@class='info-data']").text
        # Sub Type
        # sub_type = driver.find_element(By.XPATH,
        #                                "//h5[@class='info-content']/span[@class='info-title' and text()='Sub Type']/following-sibling::span[@class='info-data']").text
        # Purchase Type
        # purchase_type = driver.find_element(By.XPATH,
        #                                     "//h5[@class='info-content']/span[@class='info-title' and text()='Purchase Type']/following-sibling::span[@class='info-data']").text
        # price_per_sqft
        price_per_sqft = driver.find_element(By.XPATH,
                                             "//h5[@class='info-content']/span[@class='info-title' and text()='Price per Sqft']/following-sibling::span[@class='info-data']").text
        # MLS® Listing ID
        try:
            time.sleep(2)
            mls_listing_id = driver.find_element(By.XPATH,
                                                 "//h5[@class='info-content']/span[@class='info-title' and text()='MLS® Listing ID']/following-sibling::span[@class='info-data']").text
            if mls_listing_id == "":
                mls_listing_id = "N/A"
        except:
            time.sleep(5)
            mls_listing_id = driver.find_element(By.XPATH,
                                                 "//h5[@class='info-content']/span[@class='info-title' and text()='MLS® Listing ID']/following-sibling::span[@class='info-data']").text
        # Bedrooms
        try:
            time.sleep(2)
            bedrooms = driver.find_element(By.XPATH,
                                           "//h5[@class='info-content']/span[@class='info-title' and text()='Bedrooms']/following-sibling::span[@class='info-data']").text
            if bedrooms == "":
                bedrooms = "N/A"
        except:
            time.sleep(10)
            bedrooms = driver.find_element(By.XPATH,
                                           "//h5[@class='info-content']/span[@class='info-title' and text()='Bedrooms']/following-sibling::span[@class='info-data']").text
            beds = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/p[2]').text
        if bedrooms == "":
            bedrooms = "N/A"
        # Year Built
        try:
            time.sleep(2)
            year_built = driver.find_element(By.XPATH,
                                             "//h5[@class='info-content']/span[@class='info-title' and text()='Year Built']/following-sibling::span[@class='info-data']").text
            if year_built == "":
                year_built = "N/A"
        except:
            time.sleep(5)
            year_built = driver.find_element(By.XPATH,
                                             "//h5[@class='info-content']/span[@class='info-title' and text()='Year Built']/following-sibling::span[@class='info-data']").text
            if year_built == "":
                year_built = "N/A"
                pass
        # description
        # try:
        #     description = driver.find_element(By.XPATH,
        #                                       '//p[@class="info-content read-more-content"]//span[@class="info-data max-height"]').text
        #     if description == "":
        #         description = "N/A"
        # except:
        #     time.sleep(9)
        #     description = driver.find_element(By.XPATH,
        #                                       '//p[@class="info-content read-more-content"]//span[@class="info-data max-height"]').text
        #     if description == "":
        #         description = "N/A"
        #         pass
        # else:
        #     description = "N/A"
        #     pass
             # Get date of post
        post_date_str = driver.find_element(By.XPATH,
                                            "//p[@class='detail-content']/span[text()='UPDATED:']/following-sibling::span[@class='day-site']").text
        print(post_date_str)
        # beds
        try:
            beds = driver.find_element(By.XPATH, '//div[@class="bed-count"]//p[@class="desc"]').text
        except:
            time.sleep(10)
            beds = driver.find_element(By.XPATH, '//div[@class="bed-count"]//p[@class="desc"]').text
        # baths
        try:
            baths = driver.find_element(By.XPATH, '//div[@class="bath-count"]//p[@class="desc"]').text
        except:
            time.sleep(4)
            baths = driver.find_element(By.XPATH, '//div[@class="bath-count"]//p[@class="desc"]').text
        # sqft
        try:
            sqft = driver.find_element(By.XPATH, '//div[@class="sqft-count"]//p[@class="desc"]').text
        except:
            time.sleep(5)
            sqft = driver.find_element(By.XPATH, '//div[@class="sqft-count"]//p[@class="desc"]').text

        try:
            post_date_str = driver.find_element(By.XPATH, "//p[@class='detail-content']/span[text()='UPDATED:']/following-sibling::span[@class='day-site']").text
        except:
            time.sleep(2)
            post_date_str = driver.find_element(By.XPATH, "//p[@class='detail-content']/span[text()='UPDATED:']/following-sibling::span[@class='day-site']").text

        if property_url in already_scraped_links_list or property_url in csv_scrape_list_checker:
            print(f"ALREADY SCRAPED THIS LINK: {property_url}")
            continue
        elif post_date_str:
            # Extracting date and time from the post
            post_datetime = datetime.strptime(post_date_str, "%m/%d/%Y %I:%M %p")

            # Converting user input to datetime object
            input_datetime = format_date(input_date, input_time)

            # Checking if the post date is after user input date and time
            if post_datetime.date() > input_datetime.date() or (
                    post_datetime.date() == input_datetime.date() and post_datetime.time() > input_datetime.time()
            ):
                already_scraped_links_list.append(property_url)

                header = ["Scraped_link"]

                with open('scrape_links.csv', 'a+', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)

                    # Write header
                    if file.tell() == 0:  # Check if file is empty
                        writer.writerow(header)

                    writer.writerow([property_url])


                # Printing all details if condition is met
                try:
                    print(
                        f"Title: {title}\nPrice: {price}\nBeds:{beds}\nBaths: {baths}\nSqft: {sqft}\nDate: {post_datetime}\nProperty Type: {property_type}\nProperty Link: {property_url}\nSquare Footage: {square_footage}\nStyle: {style}\nPrice per Sqft: {price_per_sqft}\nMLS® Listing ID: {mls_listing_id}\nBedrooms: {bedrooms}\nYear Built: {year_built}\nDescription: {description_contact_info}\n"
                    )
                except:
                    pass
                image_elements = driver.find_elements(By.XPATH,
                                                      "//div[@class='img-box swiper-img']//div[@class='img-content']//img")
                time.sleep(3)
                try:
                    for i in range(3):
                        more_images_btn = driver.find_element(By.XPATH,
                                                              '//div[@class="swiper-button-next iconfont icon-chevron_right"]')
                        more_images_btn.click()
                        time.sleep(5)
                except:
                    pass
                # Download each image
                try:
                    for image_element in image_elements:
                        image_url = image_element.get_attribute("src")
                        if image_url:
                            image_url = urljoin(property_url, image_url)
                            download_image(image_url, folder_path)
                except:
                    time.sleep(5)
                    for image_element in image_elements:
                        image_url = image_element.get_attribute("src")
                        if image_url:
                            image_url = urljoin(property_url, image_url)
                            download_image(image_url, folder_path)

                # Close the browser

                # driver.execute_script("window.open('https://www.facebook.com/marketplace/create/rental','_blank')")
                #
                # # Switch to the newly opened tab (Facebook Marketplace)
                # driver.switch_to.window(driver.window_handles[1])

                driver.switch_to.window(driver.window_handles[1])

                time.sleep(11)



                # time.sleep(5)

                # Folder ka path
                folder_path = r"C:\Users\ainsl\PycharmProjects\sellbuywinni_fbautomation\website_images"

                all_paths_list = []

                # Folder mein files aur subfolders ke paths nikalne ke liye
                for root, dirs, files in os.walk(folder_path):
                    for name in files:
                        file_path = os.path.join(root, name)
                        print("File Path:", file_path)
                        all_paths_list.append(file_path)
                print(all_paths_list)


                time.sleep(6)
                upload_image = driver.find_element(By.XPATH, '//input[@accept="image/*,image/heif,image/heic"]')

                # i want to send just 5 images from list
                for all_images in all_paths_list[:9]:
                    upload_image.send_keys(all_images)
                    time.sleep(5)
                time.sleep(30)
                # //label[@aria-label='Home for Sale or Rent']//i[@class='x1b0d499 xep6ejk']
                try:
                    home_for_sale_or_rent = driver.find_element(By.XPATH, "//label[@aria-label='Home for Sale or Rent']//i[@class='x1b0d499 xep6ejk']")
                    home_for_sale_or_rent.click()
                except:
                    home_for_sale_or_rent = driver.find_element(By.XPATH,
                                                                "//label[@aria-label='Home for Sale or Rent']//i[@class='x1b0d499 xep6ejk']")
                    home_for_sale_or_rent.click()

                time.sleep(4)

                try:
                    for_sale = driver.find_element(By.XPATH, "//span[normalize-space()='For Sale']")
                    for_sale.click()
                except:
                    for_sale = driver.find_element(By.XPATH, "//span[normalize-space()='For Sale']")
                    for_sale.click()

                time.sleep(5)
                try:
                    property_type_button = driver.find_element(By.XPATH,
                                                             "//label[@aria-label='Property type']//i[@class='x1b0d499 xep6ejk']")
                    property_type_button.click()
                except:
                    property_type_button = driver.find_element(By.XPATH,
                                                             "//label[@aria-label='Rental type']//i[@class='x1b0d499 xep6ejk']")
                    property_type_button.click()
                time.sleep(3)
                if property_type == "Single Family Home":
                    single_family_home = driver.find_element(By.XPATH, "//span[normalize-space()='House']")
                    single_family_home.click()
                    time.sleep(6)
                elif property_type == "Townhouse":
                    townhouse = driver.find_element(By.XPATH, "//span[normalize-space()='Townhouse']")
                    townhouse.click()
                    time.sleep(2)
                elif property_type == "Condo":
                    condo = driver.find_element(By.XPATH, "//span[normalize-space()='Apartment']")
                    condo.click()
                    time.sleep(7)
                else:
                    single_family_home = driver.find_element(By.XPATH, "//span[normalize-space()='House']")
                    single_family_home.click()
                    time.sleep(3)


                time.sleep(3)

                try:
                    number_of_bedrooms = driver.find_element(By.XPATH,
                                                             '//label[@aria-label="Number of bedrooms"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    number_of_bedrooms.send_keys(beds)
                    time.sleep(6)
                except:
                    time.sleep(10)
                    number_of_bedrooms = driver.find_element(By.XPATH,
                                                             '//label[@aria-label="Number of bedrooms"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    number_of_bedrooms.send_keys(beds)
                    time.sleep(6)

                try:
                    number_of_bathrooms = driver.find_element(By.XPATH,
                                                              '//label[@aria-label="Number of bathrooms"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    number_of_bathrooms.send_keys(baths)
                except:
                    time.sleep(10)
                    number_of_bathrooms = driver.find_element(By.XPATH,
                                                              '//label[@aria-label="Number of bathrooms"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    number_of_bathrooms.send_keys(baths)

                try:
                    time.sleep(8)

                    price_ = driver.find_element(By.XPATH,
                                                 '//label[@aria-label="Price"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    time.sleep(2)
                    price_.send_keys(price)
                except:
                    time.sleep(10)

                    price_ = driver.find_element(By.XPATH,
                                                 '//label[@aria-label="Price"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    time.sleep(2)
                    price_.send_keys(price)

                try:
                    time.sleep(9)
                    address = driver.find_element(By.XPATH,
                                                  '//label[@aria-label="Property address"]//input[@aria-label and @class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    address.send_keys(title)
                    time.sleep(4)
                except:
                    time.sleep(10)
                    address = driver.find_element(By.XPATH,
                                                  '//label[@aria-label="Property address"]//input[@aria-label and @class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    address.send_keys(title)
                    time.sleep(4)

                try:
                    time.sleep(4)
                    click_on_first_address = driver.find_element(By.XPATH,
                                                                 '//li[@role="option"]//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h"]')
                    time.sleep(6)
                    click_on_first_address.click()
                except:
                    time.sleep(8)
                    click_on_first_address = driver.find_element(By.XPATH,
                                                                 '//li[@role="option"]//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h"]')
                    time.sleep(6)
                    click_on_first_address.click()

                time.sleep(4)
                rentral_description = driver.find_element(By.XPATH,
                                                          "//label[@aria-label='Property description']//textarea[@dir='ltr']")
                # ye url ko short mein convert kray ga
                specific_part_url = extract_specific_url_part(property_url)

                try:
                    time.sleep(4)
                    rentral_description.send_keys(
                        f'For More Information:\nVisit the website Below\n{specific_part_url}\n\n{description_contact_info}')
                except:
                    time.sleep(7)
                    rentral_description.send_keys(
                        f'For More Information:\nVisit the website Below\n{specific_part_url}\n\n{description_contact_info}')

                try:
                    property_sqft = driver.find_element(By.XPATH,
                                                        '//label[@aria-label="Property square feet"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    time.sleep(4)
                    property_sqft.send_keys(sqft)
                except:
                    time.sleep(7)
                    property_sqft = driver.find_element(By.XPATH,
                                                        '//label[@aria-label="Property square feet"]//input[@class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4"]')
                    time.sleep(4)
                    property_sqft.send_keys(sqft)

                try:
                    time.sleep(3)

                    laundry_type = driver.find_element(By.XPATH,
                                                       "//label[@aria-label='Laundry type']//i[@class='x1b0d499 xep6ejk']")
                    time.sleep(3)
                    laundry_type.click()
                except:
                    time.sleep(5)

                    laundry_type = driver.find_element(By.XPATH,
                                                       "//label[@aria-label='Laundry type']//i[@class='x1b0d499 xep6ejk']")
                    time.sleep(3)
                    laundry_type.click()

                time.sleep(6)

                try:
                    time.sleep(8)
                    laundry_none = driver.find_element(By.XPATH,
                                                       "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h'][normalize-space()='None']")
                    time.sleep(6)
                    laundry_none.click()
                    time.sleep(4)
                except:
                    pass

                try:
                    time.sleep(3)
                    parking_type = driver.find_element(By.XPATH,
                                                       "//label[@aria-label='Parking type']//i[@class='x1b0d499 xep6ejk']")
                    time.sleep(3)
                    parking_type.click()
                except:
                    time.sleep(10)
                    parking_type = driver.find_element(By.XPATH,
                                                       "//label[@aria-label='Parking type']//i[@class='x1b0d499 xep6ejk']")
                    time.sleep(3)
                    parking_type.click()

                time.sleep(5)
                try:
                    time.sleep(3)
                    parking_none = driver.find_element(By.XPATH,
                                                       "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h'][normalize-space()='None']")
                    time.sleep(3)
                    parking_none.click()
                except:
                    time.sleep(6)
                    parking_none = driver.find_element(By.XPATH,
                                                       "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h'][normalize-space()='None']")
                    time.sleep(3)
                    parking_none.click()

                try:
                    time.sleep(2)

                    air_conditioning_type = driver.find_element(By.XPATH,
                                                                "//label[@aria-label='Air conditioning type']//i[@class='x1b0d499 xep6ejk']")
                    time.sleep(6)
                    air_conditioning_type.click()
                except:
                    time.sleep(6)

                    air_conditioning_type = driver.find_element(By.XPATH,
                                                                "//label[@aria-label='Air conditioning type']//i[@class='x1b0d499 xep6ejk']")
                    time.sleep(6)
                    air_conditioning_type.click()

                time.sleep(4)
                try:
                    air_conditioning_type_none = driver.find_element(By.XPATH,
                                                                     "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h'][normalize-space()='None']")
                    time.sleep(3)
                    air_conditioning_type_none.click()
                except:
                    pass

                time.sleep(7)
                try:
                    heating_type = driver.find_element(By.XPATH,
                                                       "//label[@aria-label='Heating type']//i[@class='x1b0d499 xep6ejk']")
                    time.sleep(3)
                    heating_type.click()
                except:
                    pass

                time.sleep(6)
                try:
                    heating_none = driver.find_element(By.XPATH,
                                                       "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h'][normalize-space()='None']")
                    time.sleep(2)
                    time.sleep(5)
                    heating_none.click()
                except:
                    pass

                time.sleep(5)
                try:
                    next_button = driver.find_element(By.XPATH,
                                                      '//span[text()="Next" and @class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84"]')
                    time.sleep(5)
                    next_button.click()
                    time.sleep(8)
                except:
                    pass

                time.sleep(10)

                try:
                    publish_btn = driver.find_element(By.XPATH,
                                                      '//span[text()="Publish" and @class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84"]')

                    time.sleep(8)
                    publish_btn.click()

                    time.sleep(60)
                except:
                    pass

                time.sleep(35)
                # 03/16/2024 02:12 AM
                driver.get("https://facebook.com/marketplace/create/rental")

                time.sleep(4)

                # back to first tab
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(5)

                delete_images(folder_path)
                # print("Deleted all images")

                time.sleep(10)
                print("<<COMPLETED...>>")

            hours_splep = enter_the_hours * 3600
            time.sleep(hours_splep)
            print(f"[NOW IT WILL CHECK NEW POST AFTER {enter_the_hours} HOURS]")

            # 05:10 PM

            checking_number += 1

# time.sleep(5666)



# 03/15/2024 05:01 AM



# UPDATED:03/13/2024 05:17 PM ON MARKET: New on market today
#




# UPDATED:03/14/2024 03:12 AM



