from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import codecs
from csv import writer
import driver_module


# "https://web.whatsapp.com/send/?phone={5493413860686}&amp;text&amp;type=phone_number&amp;app_absent=0"


class Bot:
    data = []

    def __init__(self) -> None:
        self.browser = driver_module.get_driver()

    def login(self):
        while True:
            try:
                WebDriverWait(self.browser, 2).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'wa-popovers-bucket')]")))
                break
            except Exception:
                pass

        self.try_numbers()

    def try_numbers(self):
        for number in self.data:
            self.browser.get(
                f"https://web.whatsapp.com/send/?phone={number}&amp;text&amp;type=phone_number&amp;app_absent=0")
            try:
                WebDriverWait(self.browser, 15).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-animate-modal-backdrop='true']")))
                text = self.browser.find_element(
                    By.XPATH, "//div[@data-animate-modal-backdrop='true']").text
                time.sleep(10)
                if "inválido" in text:
                    self.save_number_status(number, False)
                else:
                    self.save_number_status(number, True)

            except Exception:
                self.save_number_status(number, False)

    def read_data(self):
        output = open("output.txt", "r")
        output_text = output.read()
        file_obj = codecs.open('input.txt', 'r')
        for code in [code.replace("\n", "") for code in file_obj.readlines()]:
            if code not in output_text:
                self.data.append(code)

    def save_number_status(self, code, ok):
        if ok:
            code += " Existe\n"
        else:
            code += " NoExiste\n"

        file_obj = codecs.open("output.txt", 'a+', "utf-8")
        file_obj.write(code)
        file_obj.close()

    def start_sending(self):
        print("Empezando a probar números")
        # input()
        for code in self.data:
            # print(code)
            command = "/chk " + code
            print(command)
            try:
                WebDriverWait(self.browser, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'editable-message-text')]")))
                self.browser.find_element(
                    By.XPATH, "//div[contains(@id,'editable-message-text')]").send_keys(command)
                time.sleep(1)
                WebDriverWait(self.browser, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(@class,'send') and @aria-label='Send Message']")))
                self.browser.find_element(
                    By.XPATH, "//button[contains(@class,'send') and @aria-label='Send Message']").click()
            except Exception as e:
                print(e)
            # input()

            answered = False

            while not answered:
                time.sleep(60)
                elements = self.browser.find_elements(
                    By.XPATH, "//div[contains(@class,'can-select-text') and contains(@class,'message-content-wrapper')]//div[contains(@class,'text-content')]")
                for element in elements:
                    text = element.text
                    # print(text)
                    if "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱" in text and code in text:
                        answered = True
                        self.save_code_status(code, False)
                        print("Declined")
                        break
                    elif "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱" in text and code in text:
                        answered = True
                        self.save_code_status(code, True)
                        print("Approved")
                        break
                if not answered:
                    answered = True
                    print(
                        "No es posible hacer el checkeo en este momento. Demasiados intentos")
                    break
                # input()
        print("Terminado")
        # input()

    def start(self):
        self.read_data()
        self.browser.get("https://web.whatsapp.com/")

        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//canvas[contains(@aria-label,'Scan me!')]")))
            self.login()
        except Exception:
            pass


bot = Bot()
bot.start()
