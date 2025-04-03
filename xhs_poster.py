from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import os


class XiaohongshuPoster:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.token_file = os.path.join(current_dir, "xiaohongshu_token.json")
        self.cookies_file = os.path.join(current_dir, "xiaohongshu_cookies.json")
        self.token = self._load_token()
        self._load_cookies()
        
    def _load_token(self):
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    if token_data.get('expire_time', 0) > time.time():
                        return token_data.get('token')
            except:
                pass
        return None
        
    def _save_token(self, token):
        token_data = {
            'token': token,
            'expire_time': time.time() + 30 * 24 * 3600
        }
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)
    
    def _load_cookies(self):
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    self.driver.get("https://creator.xiaohongshu.com")
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
            except:
                pass
    
    def _save_cookies(self):
        cookies = self.driver.get_cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)
            
    def login(self, phone='123', country_code="+86"):
        if self.token:
            return
        
        self.driver.get("https://creator.xiaohongshu.com/login")
        self._load_cookies()
        self.driver.refresh()
        time.sleep(3)
        if self.driver.current_url != "https://creator.xiaohongshu.com/login":
            print("使用cookies登录成功")
            self.token = self._load_token()
            self._save_cookies()
            time.sleep(2)
            return
        else:
            self.driver.delete_all_cookies()
            print("无效的cookies，已清理")
            
        self.driver.get("https://creator.xiaohongshu.com/login")

        time.sleep(5)
        qr_code_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[class='css-wemwzq']")))
        qr_code_button.click()
        time.sleep(20)
        if self.driver.current_url == "https://creator.xiaohongshu.com/new/home":
            print('Login successful')
        else:
            print('Login failed')
        print('Closing in 10 seconds')
        time.sleep(10)
        
        self._save_cookies()
        
    def post_article(self, title, content, images=None):
        time.sleep(3)
        publish_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.el-tooltip__trigger.el-tooltip__trigger")))
        publish_btn.click()

        time.sleep(3)
        tabs = self.driver.find_elements(By.CSS_SELECTOR, ".creator-tab")
        if len(tabs) > 1:
            tabs[1].click()
        time.sleep(3)

        if images:
            upload_input = self.driver.find_element(By.CSS_SELECTOR, ".upload-input")
            upload_input.send_keys('\n'.join(images))
            time.sleep(1)
        time.sleep(3)
        title_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".d-text")))
        self.driver.execute_script("arguments[0].value += arguments[1]; arguments[0].dispatchEvent(new Event('input'));", title_input, title)
        
        # Start of Selection
        content_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ql-editor")))
        self.driver.execute_script("arguments[0].innerHTML += arguments[1]; arguments[0].dispatchEvent(new Event('input'));", content_input, content)
        time.sleep(120)
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, ".d-button.publishBtn")
        submit_btn.click()
        time.sleep(60)
        
    def close(self):
        self.driver.quit()

# if __name__ == "__main__":
#     poster = XiaohongshuPoster()
#     poster.login()
#     poster.post_article("First note posted!", "This is my first note :Do", ['<path>'])
#     poster.close()