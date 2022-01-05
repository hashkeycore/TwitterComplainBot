import random
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.common.keys import Keys

PROMISED_DOWN = "100"
PROMISED_UP = "80" #21
CHROME_DRIVER_PATH = "/Users/hashkey/PycharmProjects/chrome_driver/chromedriver"
TWITTER_EMAIL = os.environ['user']
TWITTER_PASSWORD = os.environ['pass']
TWITTER_LOGIN_URL = "https://twitter.com/i/flow/login"
SPEED_URL = "https://www.speedtest.net/"


class HasText(object):
    def __init__(self, by, loc):
        self._locator = loc
        self.by = by
        self._text = " "

    def __call__(self, driver: WebElement):
        if driver.find_element(self.by, self._locator).text != self._text:
            return driver.find_element(self.by, self._locator).text


class SpeedData:

    def __init__(self, down: float, up: float):
        self.promise_up = float(PROMISED_UP)
        self.promise_down = float(PROMISED_DOWN)
        self.up = up
        self.down = down

    def is_low(self) -> bool:
        if self.down < self.promise_down and self.up < self.promise_up:
            return True


class TwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 90)

    def quit(self):
        self.driver.quit()

    def get_twitter_login_page(self, url=TWITTER_LOGIN_URL):
        self.driver.get(url=TWITTER_LOGIN_URL)

    def insert_username(self, username=TWITTER_EMAIL):
        user_name_field = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="username"]')))

        self._slow_send_keys(user_name_field, username)
        user_name_field.send_keys(Keys.ENTER)

    def insert_phone_number(self, phone="3469736639"):
        phone_field = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="text"]')))
        self._click(phone_field,1)
        self._slow_send_keys(phone_field,phone,0,1)
        phone_field.send_keys(Keys.ENTER)

    def insert_password(self, password=TWITTER_PASSWORD):
        password_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]')))

        self._slow_send_keys(password_field, password)
        password_field.send_keys(Keys.ENTER)

    def tweet(self, speed: SpeedData):
        time.sleep(2)
        # Write Message
        text_area = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')))
        self._click(text_area, 2)
        self._slow_send_keys(text_area, f"@WindTreOfficial, al momento ho {speed.down} in Download e {speed.up} "
                                        f"in Upload, la vostra offerta e' di {speed.promise_down} in download e "
                                        f"{speed.promise_up} in upload",
                             0, 1
                             )

        tweet_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]')))
        self._click(tweet_btn, 10)

    @staticmethod
    def _slow_send_keys(field: WebElement, text: str, min_wait=1, max_wait=2):
        for char in text:
            field.send_keys(char)
            time.sleep(random.randint(min_wait, max_wait))

    @staticmethod
    def _click(field: WebElement, wait_time):
        time.sleep(wait_time)
        field.click()

    def quit(self):
        self.driver.quit()


class SpeedBot:
    down: float
    up: float

    def __init__(self):
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        self.driver.maximize_window()
        # self.promise_down = PROMISED_DOWN
        # self.promise_up = PROMISED_UP
        self.wait = WebDriverWait(self.driver, 90)

    def get_speed_page(self, url=SPEED_URL):
        self.driver.get(url)

    def start_speed_test(self):
        consent = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#_evidon-banner-acceptbutton")))

        consent.click()

        go = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.start-text")))
        go.click()

    def get_speed_values(self) -> SpeedData:
        down = self.wait.until(HasText(By.CSS_SELECTOR, "span.download-speed"))
        self.down = float(down.strip())

        up = self.wait.until(HasText(By.CSS_SELECTOR, "span.upload-speed"))
        self.up = float(up.strip())
        return SpeedData(self.down, self.up)
