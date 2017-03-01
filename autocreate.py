import requests
import io
import string
import random
import time
import os

# Speech Recognition Imports
from pydub import AudioSegment
import speech_recognition as sr

# Selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

# Firefox / Gecko Driver Related
FIREFOX_BIN_PATH = r"Path/To/FireFox/Executeable/Here"
GECKODRIVER_BIN = r"/Path/To/GechoDriver/Here"

# Randomization Related
MIN_RAND = 0.50
MAX_RAND = 1.00
LONG_MIN_RAND = 3.00
LONG_MAX_RAND = 8.00

# Page Related
PASSWORD_FIELD_VALUE = 'PasswordOneTwoThree'
EMAIL_FIELD_VALUE = 'test@test.com'
DAY_FIELD_VALUE = '28'
MONTH_FIELD_VALUE = '7'
YEAR_FIELD_VALUE = '1995'
USER_FIELD_ID = 'username'
PASSWORD_FIELD_ID = 'password'
EMAIL_FIELD_ID = 'email'
DAY_FIELD_ID = 'birthday.day'
MONTH_FIELD_ID = 'birthday.month'
YEAR_FIELD_ID = 'birthday.year'
SIGNUP_BUTTON_CLASS_NAME = 'js-signup-button'

NUMBER_OF_ITERATIONS = 100
RECAPTCHA_PAGE_URL = "https://www.twitch.tv/signup"

class rebreakcaptcha(object):
    def __init__(self):
        os.environ["PATH"] += os.pathsep + GECKODRIVER_BIN
        self.driver = webdriver.Firefox(firefox_binary=FirefoxBinary(FIREFOX_BIN_PATH))
        
    def is_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def get_rand_username(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(random.randint(10, 20)))
        
    def visit_page(self):
        # Navigate to page
        self.driver.get(RECAPTCHA_PAGE_URL)
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))

    def fill_page_data(self):
        # Assign form fields
        username_field = self.driver.find_element_by_name(USER_FIELD_ID)
        password_field = self.driver.find_element_by_name(PASSWORD_FIELD_ID)
        email_field = self.driver.find_element_by_name(EMAIL_FIELD_ID)
        day_field = self.driver.find_element_by_name(DAY_FIELD_ID)
        month_field = self.driver.find_element_by_name(MONTH_FIELD_ID)
        year_field = self.driver.find_element_by_name(YEAR_FIELD_ID)

        # Fill form fields
        rand_username = self.get_rand_username()
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        username_field.send_keys(rand_username)
        print("[{0}] Entering username: {1}".format(self.current_iteration, rand_username))

        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        password_field.send_keys(PASSWORD_FIELD_VALUE)
        print("[{0}] Entering password: {1}".format(self.current_iteration, PASSWORD_FIELD_VALUE))

        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        email_field.send_keys(EMAIL_FIELD_VALUE)
        print("[{0}] Entering email: {1}".format(self.current_iteration, EMAIL_FIELD_VALUE))

        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        Select(day_field).select_by_value(DAY_FIELD_VALUE)
        print("[{0}] Entering day: {1}".format(self.current_iteration, DAY_FIELD_VALUE))

        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        Select(month_field).select_by_value(MONTH_FIELD_VALUE)
        print("[{0}] Entering month: {1}".format(self.current_iteration, MONTH_FIELD_VALUE))

        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        Select(year_field).select_by_value(YEAR_FIELD_VALUE)
        print("[{0}] Entering year: {1}".format(self.current_iteration, YEAR_FIELD_VALUE))

    def signup(self):
        try:
            signup_button = self.driver.find_element_by_class_name(SIGNUP_BUTTON_CLASS_NAME)
            time.sleep(random.uniform(MIN_RAND, MAX_RAND))
            signup_button.click()
            return True
        except Exception as e:
            print("[{0}] Signup button could not be clicked".format(self.current_iteration))
            return False
        else:
            return False

    def get_recaptcha_challenge(self):
        while 1:
            # Get all the iframes on the page
            iframes = self.driver.find_elements_by_tag_name("iframe")
            
            # Switch focus to ReCaptcha iframe
            if (len(iframes) > 0):
                self.driver.switch_to_frame(iframes[0])
                time.sleep(random.uniform(MIN_RAND, MAX_RAND))
            else:
                return
            
            # Verify ReCaptcha checkbox is present
            if not self.is_exists_by_xpath('//div[@class="recaptcha-checkbox-checkmark" and @role="presentation"]'):
                print("[{0}] No element in the frame!!".format(self.current_iteration))
                continue
            
            # Click on ReCaptcha checkbox
            self.driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-checkmark" and @role="presentation"]').click()
            time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))
        
            # Check if the ReCaptcha has no challenge
            if self.is_exists_by_xpath('//span[@aria-checked="true"]'):
                print("[{0}] ReCaptcha has no challenge. Trying again!".format(self.current_iteration))
            else:
                return
            
    def get_audio_challenge(self, iframes):
        # Switch to the last iframe (the new one)
        self.driver.switch_to_frame(iframes[-1])
        
        # Check if the audio challenge button is present
        if not self.is_exists_by_xpath('//button[@title="Get an audio challenge"]'):
            print("[{0}] No element of audio challenge!!".format(self.current_iteration))
            return False
        
        print("[{0}] Clicking on audio challenge".format(self.current_iteration))
        # Click on the audio challenge button
        self.driver.find_element_by_xpath('//button[@title="Get an audio challenge"]').click()
        time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))
    
    def get_challenge_audio(self, url):
        # Download the challenge audio and store in memory
        request = requests.get(url)
        audio_file = io.BytesIO(request.content)
        
        # Convert the audio to a compatible format in memory
        converted_audio = io.BytesIO()
        sound = AudioSegment.from_mp3(audio_file)
        sound.export(converted_audio, format="wav")
        converted_audio.seek(0)
        print("[{0}] Downloaded audio challenge".format(self.current_iteration))
        
        return converted_audio
    
    def speech_to_text(self, audio_source):
        # Initialize a new recognizer with the audio in memory as source
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_source) as source:
            audio = recognizer.record(source) # read the entire audio file

        audio_output = ""
        # recognize speech using Google Speech Recognition
        try:
            audio_output = recognizer.recognize_google(audio)
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("[{0}] Google Speech Recognition: ".format(self.current_iteration) + audio_output)
        except sr.UnknownValueError:
            print("[{0}] Google Speech Recognition could not understand audio".format(self.current_iteration))
        except sr.RequestError as e:
            print("[{0}] Could not request results from Google Speech Recognition service; {1}".format(self.current_iteration).format(e))
            
        return audio_output
    
    def solve_audio_challenge(self):
        # Verify audio challenge download button is present
        if not self.is_exists_by_xpath('//a[@class="rc-audiochallenge-download-link"]') and \
                not self.is_exists_by_xpath('//div[@class="rc-text-challenge"]'):
            print("[{0}] No element in audio challenge download link!!".format(self.current_iteration))
            return False
        
        # If text challenge - reload the challenge
        while self.is_exists_by_xpath('//div[@class="rc-text-challenge"]'):
            print("[{0}] Got a text challenge! Reloading!".format(self.current_iteration))
            self.driver.find_element_by_id('recaptcha-reload-button').click()
            time.sleep(random.uniform(MIN_RAND, MAX_RAND))

        # Get the audio challenge URI from the download link
        download_object = self.driver.find_element_by_xpath('//a[@class="rc-audiochallenge-download-link"]')
        download_link = download_object.get_attribute('href')
        
        # Get the challenge audio to send to Google
        converted_audio = self.get_challenge_audio(download_link)
        
        # Send the audio to Google Speech Recognition API and get the output
        audio_output = self.speech_to_text(converted_audio)

        # Enter the audio challenge solution
        self.driver.find_element_by_id('audio-response').send_keys(audio_output)
        time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))

        # Click on verify
        self.driver.find_element_by_id('recaptcha-verify-button').click()
        time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))
        
        return True
            
    def solve(self, current_iteration):
        self.current_iteration = current_iteration + 1
        
        # Visit page
        self.visit_page()

        # Fill page data
        self.fill_page_data()

        # Get a ReCaptcha Challenge
        self.get_recaptcha_challenge()
        
        # Switch to page's main frame
        self.driver.switch_to.default_content()
                
        # Get all the iframes on the page again- there is a new one with a challenge
        iframes = self.driver.find_elements_by_tag_name("iframe")
        
        # Get audio challenge
        self.get_audio_challenge(iframes)
        
        # Solve the audio challenge
        if not self.solve_audio_challenge():
            return False
        
        # Check if there is another audio challenge and solve it too
        while self.is_exists_by_xpath('//div[@class="rc-audiochallenge-error-message"]') and \
                self.is_exists_by_xpath('//div[contains(text(), "Multiple correct solutions required")]'):
            print("[{0}] Need to solve more. Let's do this!".format(self.current_iteration))
            self.solve_audio_challenge()
            
        # Switch to the ReCaptcha iframe to verify it is solved
        self.driver.switch_to.default_content()
        self.driver.switch_to_frame(iframes[0])
        capcha_solved = self.is_exists_by_xpath('//span[@aria-checked="true"]')

        # Switch back to page
        self.driver.switch_to_default_content()
        signup_solved = self.signup()

        return capcha_solved and signup_solved
                
def main():
    rebreakcaptcha_obj = rebreakcaptcha()
    
    counter = 0
    for i in xrange(NUMBER_OF_ITERATIONS):
        if rebreakcaptcha_obj.solve(i):
            counter += 1

            
        time.sleep(random.uniform(LONG_MIN_RAND, LONG_MAX_RAND))
        print("Successful breaks: {0}".format(counter))
        
    print("Total successful breaks: {0}\{1}".format(counter, NUMBER_OF_ITERATIONS))

if __name__ == '__main__':
    main()
