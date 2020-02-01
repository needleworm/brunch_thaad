from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys


class THAAD():
    def __init__(self, kill_list, log_output, id, ps, kill_keywords):
        self.log_output = log_output
        self.kill_keywords = kill_keywords
        self.options = Options()
        self.options.add_argument("headless")
        self.options.add_argument("window-size=1080x3020")
        self.options.add_argument("disable-gpu")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        self.login_url = "https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3De0201caea90cafbb237e250f63a519b5%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fbrunch.co.kr%252Fcallback%252Fauth%252Fkakao%26scope%3D%26state%3DaHR0cHM6Ly9icnVuY2guY28ua3IvL3NpZ25pbi9maW5pc2g_dXJsPSUyRg%26grant_type%3Dauthorization_code"
        self.driver.get(self.login_url)
        time.sleep(5)
        self.driver.find_element_by_name("email").send_keys(id)
        self.driver.find_element_by_name("password").send_keys(ps)
        self.driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button').click()
        print("login success")
        self.targets = []
        self.count = 0
        blacklist = open(kill_list)
        for line in blacklist:
            if "https" in line:
                self.targets.append(line.strip() + "#comments")
        blacklist.close()

    def run_thaad(self):
        log = open(self.log_output, 'w')
        for el in self.targets:
            self.driver.get(el)
            time.sleep(3)
            self.driver.get(el)
            replies = self.driver.find_elements_by_class_name("cont_info")
            if len(replies) == 0:
                continue
            # screen by contents
            for i, elm in enumerate(replies):
                target_detected = False
                for keyword in self.kill_keywords:
                    if keyword in elm.text:
                        target_detected = True
                if target_detected:
                    self.count += 1
                    line = time.ctime() + "\n" + elm.text
                    print(line)
                    for i in range(30):
                        elm.click()
                        del_button = elm.find_elements_by_tag_name("button")[-1]
                        if "삭제" in del_button.text:
                            del_button.click()
                            self.driver.switch_to.alert.accept()
                            log.write(line)
                            print("Deleted Success")
                            break
                        self.driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
                    print(del_button.text)
        log.close()
