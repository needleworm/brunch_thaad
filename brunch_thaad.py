from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class THAAD():
    def __init__(self, kill_list, log_output):
        self.log_output = log_output
        self.options = Options()
        self.options.add_argument("window-size=1080x1920")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        self.login_url = "https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3De0201caea90cafbb237e250f63a519b5%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fbrunch.co.kr%252Fcallback%252Fauth%252Fkakao%26scope%3D%26state%3DaHR0cHM6Ly9icnVuY2guY28ua3IvL3NpZ25pbi9maW5pc2g_dXJsPSUyRg%26grant_type%3Dauthorization_code"
        self.driver.get(self.login_url)
        print("please login")
        self.targets = []
        self.count = 0
        blacklist = open(kill_list)
        for line in blacklist:
            if "https" in line:
                print(line)
                self.targets.append(line.strip() + "#comments")
        blacklist.close()
    def run_thaad(self):
        log = open(self.log_output, 'w')
        for el in self.targets:
            self.driver.get(el)
            time.sleep(5)
            self.driver.get(el)
            replies = self.driver.find_elements_by_class_name("desc_comment")
            if len(replies) == 0:
                continue
            del_buttons = self.driver.find_elements_by_class_name("btn_delete")
            ids = self.driver.find_elements_by_class_name("link_userid")
            # screen by contents
            for i, el in enumerate(replies):
                if "http" in el.text or "clien" in el.text:
                    self.count += 1
                    line = time.ctime() + "\nUser Id is : " + ids[i].text + "\nContent is :\n" + el.text + "\n"
                    el.click()
                    del_buttons[i].click()
                    self.driver.switch_to.alert.accept()
                    print(line)
                    log.write(line)

        log.close()
