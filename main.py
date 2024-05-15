import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By # Use to locate elements on the page , 
                                            # It replicates the getElementByID function of javascript 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from transformers import pipeline


        ########################################################################################
        ######## if you want to understand the codebase deeply or experiment with it ###########
        ######## a seperate notebook with explanations and extra comments is provided ##########
        ########################################################################################

driver = webdriver.Chrome()

def is_user_logged_in():
    try:
        # Check for user profile information or sign-out button
        driver.find_element(By.XPATH, "//span[@class='nav-line-3']")
        return True
    except NoSuchElementException:
        return False
    
def amazon_login( username , password ):
    
    print(" Logging you in ... ")
    print(" ... ")
    
    # Driver go to the website 
    driver.get("https://www.amazon.com/-/es/ap/signin?openid.pape.max_auth_age=3600&openid.return_to=https://www.amazon.com/myh/households?language=es&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&language=en_US&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.ns=http://specs.openid.net/auth/2.0")
    # driver.get("https://www.amazon.com/ap/signin")
    
    # wait for the page to load 
    time.sleep(2)
    
    # if user is already logged in
    if is_user_logged_in():
        print("You are already logged in.")
        return
    
    
    # Check if CAPTCHA input is required
    captcha_required = False
    try:
        captcha_input = driver.find_element(By.ID, "captchacharacters")
        captcha_required = True
    except NoSuchElementException:
        pass

    if captcha_required:
        # Pause execution and prompt the user to solve the CAPTCHA manually
        input("Please solve the CAPTCHA manually, then press Enter to continue...")
        # Once the CAPTCHA is solved, press Enter to proceed
        captcha_input.send_keys(Keys.ENTER)
        time.sleep(5)  # Add a delay to allow the page to load after submitting CAPTCHA
    
    #############################################################################
    ########  Please read the README.md if you are stuck at this point  #########
    #############################################################################
        
    # Takes in username and perform the actions required 
    username_input = driver.find_element(By.ID, "ap_email")
    username_input.send_keys(username)
    driver.find_element(By.ID, "continue").click()
    # wait for the page to load 
    time.sleep(2)
    
    # Takes in password and perform the actions required 
    password_input = driver.find_element(By.ID, "ap_password")
    password_input.send_keys(password)
    driver.find_element(By.ID, "signInSubmit").click()
    
    # wait for the page to load 
    time.sleep(5)
    
    
    # Check if OTP input is required
    otp_input_required = False
    try:
        otp_input = driver.find_element(By.ID, "auth-mfa-otpcode")
        otp_input_required = True
    except NoSuchElementException:
        pass

    if otp_input_required:
        otp = input("Enter the OTP received on your email/phone: ")
        otp_input.send_keys(otp)
        
        driver.find_element(By.ID, "auth-signin-button").click()
        
        time.sleep(5)
        
        
    print(" Logging complete ... ")
    print(" ... ")

def handle_unexpected_elements(page_source):
    
    prompt_text = f"You are navigating an order details page and encountered the following HTML: {page_source}. What actions should you take to continue extracting order details?"
    
    # Loading the free-to-use GPT-Neo model
    generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
    response = generator(prompt_text, max_length=150, num_return_sequences=1)
    
    # Extract and return the generated response
    actions = response[0]['generated_text'].strip()
    return actions


def get_source_page(driver, order_link):
    
    driver.get(order_link)
    
    # wait for the page to load 
    time.sleep(3)
    
    page_source = driver.page_source
    
    # Use GPT-Neo to handle any unexpected elements
    actions = handle_unexpected_elements(page_source)
    
    if "click the 'Close' button" in actions:
        
        close_button = driver.find_element(By.XPATH, "//button[text()='Close']")
        close_button.click()
        
        time.sleep(2)
    
    # Save the page HTML
    order_html = driver.page_source
    return order_html


def navigate_and_fetch_all_orders():
    
    print(" Getting your order history ... ")
    print(" ... ")
    
    driver.get("https://www.amazon.com/gp/your-account/order-history")
    time.sleep(5)

    all_order_html = ""  # Initialize an empty string to store all order HTML
    
    
    orders = driver.find_elements(By.CLASS_NAME, "order")
    for order in orders:
        order_link = order.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")
        order_html = fetch_order_details_with_llm(driver, order_link)
        all_order_html += order_html  # Append current order HTML to the string

        time.sleep(3)

        ########################################################################################
        # Decomment this if there are several pages , by default it only select the shown page # 
        ########################################################################################

#     while True:
#         orders = driver.find_elements(By.CLASS_NAME, "order")
#         for order in orders:
#             order_link = order.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")
#             order_html = fetch_order_details_with_llm(driver, order_link)
#             all_order_html += order_html  # Append current order HTML to the string

#             time.sleep(3)

#         # Check if there's a next page
#         next_button = driver.find_element(By.CSS_SELECTOR, ".a-pagination li.a-last a")
#         if "disabled" in next_button.get_attribute("class"):
#             break  # Exit loop if there's no next page

#         # Click on the next page button
#         next_button.click()
#         time.sleep(5)  # Add a delay to ensure the page is loaded

    # Write all order HTML to a single file
    with open("all_orders.html", "w", encoding="utf-8") as file:
        file.write(all_order_html)
        
    print(" Saved the RAW files ... ")
    print(" ... ")



def extract_order_details( html_content ):
    prompt_text = f"Extract order details such as order number, product names, quantities, prices, and delivery status from the following HTML: {html_content}"
    
    print(" Using LLM fetching your data ... ")
    print(" ... ")
    
    # Use the LLM
    generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
    response = generator(prompt_text, max_length=300, num_return_sequences=1)
    
    # Extract and return the generated order details
    order_details = response[0]['generated_text'].strip()
    return order_details


def save_order_details():
    
    with open("all_orders.html", "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    order_data = extract_order_details(html_content)

    with open("orders_data.json", "w", encoding="utf-8") as json_file:
        json.dump(order_data, json_file, indent=4)
        
    print(" Succesfully saved ... ")
    print(" ... ")


USERNAME = input("Enter your Amazon username: ")
PASSWORD = input("Enter your Amazon password: ")

# Decomment this for sensitive information

# # Load sensitive information from environment variables
# AMAZON_USERNAME = os.getenv("AMAZON_USERNAME")
# AMAZON_PASSWORD = os.getenv("AMAZON_PASSWORD")

amazon_login(USERNAME, PASSWORD)
navigate_and_fetch_all_orders()
save_order_details()

# Close the Driver

driver.quit()