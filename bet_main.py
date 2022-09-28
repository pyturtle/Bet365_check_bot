
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import pybettor
import ctypes

#pip install request 
#pip install undetected-chromedriver
#pip install selenium==4.0.0
#pip install pybettor



if __name__ == '__main__':
    USERNAME = ""
    PASSWORD = ""

    
    chrome_options = Options()
    driver = uc.Chrome(options=chrome_options)
    driver.get("https://www.on.bet365.ca/?_h=mPclEvn4-5qJmR4BCbbPRA%3D%3D#/IP/B1") #replace this with you default soccer link on live games 
    sleep(2)

    #un comment part below if the is the live match stats popup 
    driver.switch_to.window(driver.current_window_handle)
    popup = driver.find_element(By.CLASS_NAME,"iip-IntroductoryPopup_Cross")
    popup.click()
    ############################################################################
    
    sleep(2)
    

    # try:
    #     popup = driver.find_element(By.CLASS_NAME,"iip-IntroductoryPopup_Cross")
    #     popup.click()u
    #     sleep(2)
    #     login = driver.find_element(By.CLASS_NAME,"hm-MainHeaderRHSLoggedOutWide_LoginContainer ")
    #     login.click()
    #     sleep(2)
    #     username_field = driver.find_element(By.CLASS_NAME,"lms-StandardLogin_Username ")
    #     password_field = driver.find_element(By.CLASS_NAME,"lms-StandardLogin_Password ")
    #     username_field.send_keys(USERNAME)
    #     sleep(1)
    #     password_field.send_keys(PASSWORD)
    #     sleep(1)
    #     login_button = driver.find_element(By.CLASS_NAME,"lms-LoginButton ")
    #     login_button.click()
    #     sleep(4)
    #     driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))
    #     popup = driver.find_element(By.CLASS_NAME, "accept-button")
    #     popup.click()
    #     driver.switch_to.default_content()
    #     sleep(3)
    #     driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))
    #     popup = driver.find_element(By.ID,"remindLater")
    #     popup.click()
    #     driver.switch_to.default_content()
    #     driver.execute_script("window.scrollTo(0, 123)") 
    #     sleep(3)
    #     popup = driver.find_element(By.CLASS_NAME,"llm-LastLoginModule_Button ")
    #     popup.click()
    # except Exception as e:
    #     print(e)
    
    


    found = []
    while True:
        driver.switch_to.window(driver.current_window_handle)
        game_list = driver.find_elements(By.CLASS_NAME,"ovm-Fixture_Container")
        game_aditional_element = driver.find_elements(By.CLASS_NAME,"ovm-MediaIconContainer ")

        # print(game_list.get_attribute('innerHTML'))
        for i,game in enumerate(game_list):

            try:
                time = game.find_element(By.CLASS_NAME,"ovm-FixtureDetailsTwoWay_PeriodWrapper").text
                # print(f"Time:{time}")
            except Exception as e:
                print(e)
            
            if time != "45:00":
                continue

            print("1 pass")


            try:
                score_one = game.find_element(By.CLASS_NAME,"ovm-StandardScoresSoccer_TeamOne ").text
                score_two = game.find_element(By.CLASS_NAME,"ovm-StandardScoresSoccer_TeamTwo ").text
                # print (f"Score:{score_one}x{score_two}")
            except Exception as e:
                print(e)

            if int(score_one)+int(score_two) != 1:
                continue

            print("2 pass")

            try:
                odds = game.find_elements(By.CLASS_NAME,"ovm-ParticipantOddsOnly_Odds")
                odd1 = pybettor.convert_odds(int(odds[0].text),cat_out="dec")[0]
                odd2 = pybettor.convert_odds(int(odds[1].text),cat_out="dec")[0]
            except Exception as e:
                print(e)
            
            
            if odd1 < 1.40 and odd2 < 1.40:
                continue
            
            print("3 pass")

            driver.execute_script("arguments[0].scrollIntoView();", game_aditional_element[i])
            game_aditional_element[i].click()
            
            try:
                sleep(0.2)
                attacks_one = driver.find_elements(By.CLASS_NAME,"ml-WheelChart_Team1Text ")
                attacks_two = driver.find_elements(By.CLASS_NAME,"ml-WheelChart_Team2Text ")
                # print(f"Dangerous Attacks:{attacks_one[1]}-{attacks_two[1]")
            except Exception as e:
                print(e)

            if int(attacks_one[1].text) + int(attacks_two[1].text) <= 44:
                continue
            
            
            if i in found:
                print("in")
                continue
            print("Game found!")
            ctypes.windll.user32.MessageBoxW(0, "Game found!", "Alert", 0x1000)

            found.append(i)
            stall = input()
        for i in found:
            print(i)
            game_time = game_list[i].find_element(By.CLASS_NAME,"ovm-FixtureDetailsTwoWay_PeriodWrapper").text
            print(game_time)
            if game_time != "45:00":
                found.remove(i)

        sleep(5)
        
