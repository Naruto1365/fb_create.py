import time
import random
import os
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from PIL import Image
from io import BytesIO

# Step 1: Login Check
def authenticate_user():
    print("What is your name?")
    username = input("Name: ")
    
    password = input("Enter password: ")
    if password != "12345":
        print("Wrong password. Access denied.")
        exit()

    print(f"Welcome, {username}!")
    start = input("Type 'start' to begin the Facebook bot: ").strip().lower()
    if start != "start":
        print("You didn't type 'start'. Exiting...")
        exit()

# Step 2: Generate Fake User
def generate_fake_user():
    fake = Faker()
    gender = random.choice(['male', 'female'])
    first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
    last_name = fake.last_name()
    email = fake.email()
    password = fake.password(length=12, special_chars=True)
    birth_day = str(random.randint(1, 28))
    birth_month = str(random.randint(1, 12))
    birth_year = str(random.randint(1975, 2000))
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'day': birth_day,
        'month': birth_month,
        'year': birth_year,
        'gender': gender
    }

# Step 3: Download Profile Pic
def download_random_profile_picture(filename="profile_pic.jpg"):
    try:
        url = "https://thispersondoesnotexist.com/image"
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            os.makedirs("profile_pics", exist_ok=True)
            img.save(os.path.join("profile_pics", filename))
            print("[+] Random profile picture saved.")
        else:
            print("[-] Could not fetch profile picture.")
    except Exception as e:
        print("[-] Error downloading image:", e)

# Step 4: Facebook Automation
def automate_facebook_signup():
    user = generate_fake_user()
    download_random_profile_picture(user['first_name'] + ".jpg")

    print("[*] Launching browser...")
    driver = webdriver.Chrome()  # Make sure ChromeDriver is installed
    driver.get("https://www.facebook.com/reg")
    time.sleep(3)

    print("[*] Filling in Facebook signup form...")
    driver.find_element(By.NAME, "firstname").send_keys(user['first_name'])
    driver.find_element(By.NAME, "lastname").send_keys(user['last_name'])
    driver.find_element(By.NAME, "reg_email__").send_keys(user['email'])
    time.sleep(1)
    driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(user['email'])
    driver.find_element(By.NAME, "reg_passwd__").send_keys(user['password'])

    driver.find_element(By.ID, "day").send_keys(user['day'])
    driver.find_element(By.ID, "month").send_keys(user['month'])
    driver.find_element(By.ID, "year").send_keys(user['year'])

    gender_value = '2' if user['gender'] == 'male' else '1'
    driver.find_element(By.XPATH, f"//input[@value='{gender_value}']").click()

    print("[*] Submitting...")
    driver.find_element(By.NAME, "websubmit").click()

    print("[*] Waiting 15 seconds to see result...")
    time.sleep(15)
    driver.quit()

    print(f"[+] Fake signup simulated with: {user['email']} | {user['password']}")

# --- RUN EVERYTHING ---
authenticate_user()
automate_facebook_signup()
