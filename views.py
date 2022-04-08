import shelve
import time
from urllib.parse import urlparse
# from matplotlib.pyplot import text
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint

import sheets



API_KEY = "50e99d1ef912ed612ec08d1612372c8e"
AHREFS_EMAIL = "rahulthepcl@gmail.com"
AHREFS_PASSWORD = "Ganesh007#%"

error = ""


# def getDriver( ):
#     print("Getting the driver ready")
#     # print(settings.DEBUG)
#     DEBUG = True
#     if not DEBUG:
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_experimental_option("detach", True)
#         chrome_driver_path = Service(r"D:\viji\Aries\Development\chromedriver.exe")

#         driver = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)
#         driver.maximize_window()
#     else:
#         chromeOptions = webdriver.ChromeOptions()
#         chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#         chromeOptions.add_argument("--headless")
#         chromeOptions.add_argument("--no-sandbox")
#         chromeOptions.add_argument("--disable-dev-sh-usage")
#         chromeOptions.add_argument('--disable-dev-shm-usage')
#         chrome_driver_path = Service(os.environ.get("CHROMEDRIVER_PATH"))

#         driver = webdriver.Chrome(service=chrome_driver_path, options=chromeOptions)
#         driver.maximize_window()
#     print("Driver is ready")
#     return driver

# For Local Testing
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

def get_da_pa_ss(driver,urls):
    # driver = getDriver()
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
    


def get_alexa_rank(driver,urls):
    # driver = getDriver()
    print("Getting alexa rank")
    # alexa_list = []
    driver.get("https://www.rankwatch.com/free-tools/alexa-rank-checker")
    text_area = WebDriverWait(driver, 7).until(EC.presence_of_element_located(("id", "search-by-url")))
    alexa_list = []
    for url in urls:
        text_area.send_keys(url+"\n")
        # time.sleep(2)
        find_rank = driver.find_element("id", "find-alexa")
        find_rank.click()
        time.sleep(5)
        try:
            # result_list = WebDriverWait(driver,7).until_not(EC.presence_of_all_elements_located((By.XPATH,'/html/body/section[1]/div/div/div[2]/section/div/div/div/div[2]/div[3]/div/table/tbody/tr')))
            result_list = driver.find_elements("css selector", "table#res-table td")
            new_list=[]
            # new_list = [item.text for item in result_list]
            # temp_list = []
            for item in result_list:
                    if "ConnectException" in item.text or "finding" in item.text or "updating"  in item.text:
                        new_list.append("No data")
                    else:
                        new_list.append(item.text)
            
            alexa_list.extend([new_list[1]])
            new_list = []
            text_area.send_keys(Keys.CONTROL+"a"+Keys.CONTROL)
            text_area.send_keys(Keys.BACK_SPACE)
        except (IndexError,TimeoutException) as e:
            alexa_list.extend(["No data"])
            driver.get("https://www.rankwatch.com/free-tools/alexa-rank-checker")
            text_area = WebDriverWait(driver, 7).until(EC.presence_of_element_located(("id", "search-by-url")))

    return alexa_list

def ahrefs_login(driver):
    try:
        driver.get("https://app.ahrefs.com/user/login")
        email_field = driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[1]/input')
        password_field = driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[2]/div/input')

        email_field.send_keys(AHREFS_EMAIL)
        password_field.send_keys(AHREFS_PASSWORD)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/button/div').click()
        print("Login Done to ahrefs")
    except Exception as e:
        print(e)

def get_ahref_ur_dr():
    AHREF_UR_DR_LIST = []
    driver =getDriver()
    ahrefs_login(driver)
    time.sleep(7)
    while sheets.to_repeat(isUR=True):
        print("Getting Data")
        urls = sheets.get_website_for_ahref(200)
        pprint(urls)
        driver.get("https://app.ahrefs.com/batch-analysis")
        time.sleep(7)
        text_area = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div[2]/div/form/fieldset/textarea")
        for url in urls:
            text_area.send_keys(url+"\n")
        analyse_btn = driver.find_element_by_xpath('//*[@id="startAnalysisButton"]')
        analyse_btn.click()
        time.sleep(5)
        num_rows =len(driver.find_elements_by_xpath(r'//*[@id="batch_data_table"]/tbody/tr'))
        for no_of_row in range(1,num_rows+1):
            xpath_str = r'//*[@id="batch_data_table"]/tbody/tr['+str(no_of_row)+']/td'
            cols =driver.find_elements_by_xpath(xpath_str)
            UR = cols[5].text
            DR = cols[6].text
            AR = cols[7].text
            if "—" in UR:
                UR = "No data"
            if "—" in AR:
                AR = "No data"
            if "—" in DR:
                DR = "No Data"
            AHREF_UR_DR_LIST.append([UR,DR,AR])
        pprint(AHREF_UR_DR_LIST)
        sheets.updating_sheet(AHREF_UR_DR_LIST,forAhref=True)
    
def cleanup( driver):
    driver.close()
    driver.quit()
    driver = None
    print("IN CLEANUP")

# get_da_pa_ss(["google.com","facebook.com"])
# print(get_alexa_rank(["https://google.xyz","https://facebook.com","https://youtube.com","https://godaddy.com","https://www.geeksforgeeks.org/"]))

def Main():
    # try:
        # urls = ["https://google.xyz","https://facebook.com","https://youtube.com","https://godaddy.com","https://www.geeksforgeeks.org/"]
        # DA_list, SS_list, PA_list = get_da_pa_ss(urls)
        # dr_list, ur_list, ahrefs_traffic_list = get_dr_ur_ahrefs_traffic(urls)
        while sheets.to_repeat():
            driver = getDriver()   
            urls = sheets.input_websites()
            print(urls)
            DA_list, SS_list, PA_list = get_da_pa_ss(driver,urls)  # DA_list, SS_list, Alexa_list = get_values(driver, urls)
            # dr_list, ur_list, ahrefs_traffic_list = get_dr_ur_ahrefs_traffic(driver,urls)

            dr_list, ur_list, ahrefs_traffic_list = [],[],[]
            alexa_list =get_alexa_rank(driver,urls)
            for i in range(len(SS_list)):
                dr_list.append("")
                ur_list.append("")
                ahrefs_traffic_list.append("")
            print(alexa_list)
            data_list = []
            print(f"DA:{len(DA_list)}, SS:{len(SS_list)}, PA:{len(PA_list)}, DR:{len(dr_list)}, UR:{len(ur_list)}, ahrefs traffic:{len(ahrefs_traffic_list)}, Alexa Rank:{len(alexa_list)}")
            print("creating a datalist")
            for i in range(0, len(SS_list)):
                data_list.append([DA_list[i], SS_list[i], PA_list[i], ur_list[i], dr_list[i], ahrefs_traffic_list[i], alexa_list[i]])  # data_list.append([DA_list[i], SS_list[i], Alexa_list[i]])
            print(data_list)
            sheets.updating_sheet(data=data_list)
            pprint(data_list)
            print("sheet filled")
                
            cleanup(driver)
        
    # except Exception as e:
    #     global error
    #     print("Somthing Went Wrong :",str(e))
    #     error = str(e)
    #     return "Somthing Went Wrong :"+str(e)





# Main()
get_ahref_ur_dr()