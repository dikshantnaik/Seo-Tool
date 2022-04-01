import time
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
import sheets



API_KEY = "50e99d1ef912ed612ec08d1612372c8e"
AHREFS_EMAIL = "rahulthepcl@gmail.com"
AHREFS_PASSWORD = "Adsense007##"


def getDriver():

    options = Options()
    options.binary_location = "/opt/google/chrome/google-chrome"    #chrome binary location specified here

    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument("--no-sandbox") #bypass OS security model
    options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome("/bin/chromedriver",options=options)
    return driver

def get_da_pa_ss(urls):
    driver = getDriver()
    print("Finding DA PA and SS")
    driver.get("https://www.dapachecker.org/spam-score-checker")
    time.sleep(2)

    search = driver.find_element("id", "urls")
    for url in urls:
        search.send_keys(url+"\n")
    time.sleep(2)

    analyse_btn = WebDriverWait(driver, 7).until(EC.element_to_be_clickable(("id", "checkBtnCap")))
    analyse_btn.click()

    time.sleep(2)
    values = []
    DA_list = []
    SS_list = []
    PA_list = []
    m = 0
    while not values:
        m += 1
        values = driver.find_elements("css selector", "table#example tbody tr td")
        values_str = []
        # if m > 15:
        #     cleanup(driver)
        #     main_program()
        for value in values:
            if values.index(value) in [25, 51, 77, 103]:
                print(f"{value.text} of index {values.index(value)} is not added")
                pass
            else:
                values_str.append(value.text)

        print(len(values_str))
        print(len(values))
        DA_list = values_str[3::5]
        SS_list = values_str[2::5]
        PA_list = values_str[4::5]
        time.sleep(2)
    print("Values of DS and SS obtained")
    print(DA_list)
    print(SS_list)
    print(PA_list)
    print("All required values are obtained")
    return DA_list, SS_list, PA_list


def get_alexa_rank( urls):
    driver = getDriver()
    print("Getting alexa rank")
    alexa_list = []
    domains = urls
    first_set, second_set, third_set, fourth_set = [],[],[],[]
    n = 0
    for domain in domains:
            if n <= 4:
                first_set.append(domain)
            elif n <= 9:
                second_set.append(domain)
            elif n <= 14:
                third_set.append(domain)
            elif n <= 19:
                fourth_set.append(domain)
            n += 1
    sets = [first_set, second_set, third_set, fourth_set]
    print("PRINTING ALL SET :",sets)
    for my_set in sets:
        if my_set:
            driver.get("https://www.rankwatch.com/free-tools/alexa-rank-checker#:~:text=You%20should%20begin%20by%20opening,And%20that's%20it.")
            text_area = WebDriverWait(driver, 7).until(EC.presence_of_element_located(("id", "search-by-url")))
            for domain in my_set:
                text_area.send_keys(domain+"\n")
            time.sleep(2)
            find_rank = driver.find_element("id", "find-alexa")
            find_rank.click()
            time.sleep(7)
            result_list = driver.find_elements("css selector", "table#res-table td")
            # new_list = []
            # for item in result_list:
            #     if "ConnectException" not in item.text or "finding" not in item.text or "updating" not in item.text:
            #         new_list.append(item.text)
            #     else:
            #         new_list.append("No data")
            new_list = [item.text for item in result_list]
            new_list2 = []
            for item in new_list:
                if "ConnectException" in item or "finding" in item or "updating"  in item:
                    new_list2.append("No data")
                else:
                    new_list2.append(item)

            print(new_list2)
            # alexa_rank_list = new_list2[1:len(new_list2):6]

            alexa_list.extend(new_list2)
            print("Printing a set",new_list2)
    print(f"this is the alexa rank list {alexa_list}")
    return alexa_list

# get_da_pa_ss(["google.com","facebook.com"])
get_alexa_rank(urls=["https://google.com","https://facebook.com"])