import time
from urllib.parse import urlparse
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
import sheets

API_KEY = "50e99d1ef912ed612ec08d1612372c8e"
userid = "rahulthepcl@gmail.com"
password = "Adsense007##"


# def get_driver():
#     print("Getting the driver ready")
#     print(settings.DEBUG)
#     if not settings.DEBUG:
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


def get_da_pa_ss(driver, urls):
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
        if m > 15:
            cleanup(driver)
            main_program()
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


def ahrefs_login(driver):
    try:
        email_field = driver.find_element(By.XPATH,
                                          '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[1]/input')
        password_field = driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/div[2]/div/input')

        email_field.send_keys(userid)
        password_field.send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/form/div/button/div').click()
        print("Login Done to ahrefs")
    except Exception as e:
        return e


def get_ahref_values(driver):
    ur,dr,traffic = "","",""
    try:
        ur = WebDriverWait(driver, 15).until(EC.presence_of_element_located(("css selector", "div#UrlRatingContainer span")))
        ur = ur.text
    except TimeoutException:
        ur = "No data"
    
    try:
        dr = WebDriverWait(driver, 15).until(EC.presence_of_element_located(("css selector", "div#DomainRatingContainer span")))
        dr = dr.text
    except TimeoutException:
        dr = "No data"
    
    try:
        traffic = WebDriverWait(driver, 15).until(EC.presence_of_element_located(("css selector", "h5#numberOfOrganicTraffic span")))
        traffic  = traffic.text
    except TimeoutException:
        traffic = "No data"
    
    return ur,dr,traffic


def get_dr_ur_ahrefs_traffic(driver, urls):
    n = 0
    ur_list = []
    dr_list = []
    ahrefs_traffic_list = []
    print("getting ur dr and ahrefs traffic")
    for url in urls:
        try:
            driver.get(f"https://app.ahrefs.com/site-explorer/overview/v2/prefix/live?target={url}")
            print(urlparse(url).hostname)
            if n == 0:
                ahrefs_login(driver)
                n += 1
        except TimeoutException:
            try:
                ahrefs_login(driver)
                ur, dr, traffic = get_ahref_values(driver)
                ur_list.append(ur)
                dr_list.append(dr)
                ahrefs_traffic_list.append(traffic)
            except TimeoutException:
                driver.get(
                    f"https://app.ahrefs.com/site-explorer/overview/v2/prefix/live?target={url}")
                print(urlparse(url).hostname)
                ur, dr, traffic = get_ahref_values(driver)
                ur_list.append(ur)
                dr_list.append(dr)
                ahrefs_traffic_list.append(traffic)
            except NoSuchElementException:
                driver.get(
                    f"https://app.ahrefs.com/site-explorer/overview/v2/prefix/live?target={url}")
                print(urlparse(url).hostname)
                ur, dr, traffic = get_ahref_values(driver)
                ur_list.append(ur)
                dr_list.append(dr)
                ahrefs_traffic_list.append(traffic)
        except NoSuchElementException:
            driver.get(f"https://app.ahrefs.com/site-explorer/overview/v2/prefix/live?target={url}")
            print(urlparse(url).hostname)
            ur, dr, traffic = get_ahref_values(driver)
            ur_list.append(ur)
            dr_list.append(dr)
            ahrefs_traffic_list.append(traffic)
        except WebDriverException:
            driver.get(f"https://app.ahrefs.com/site-explorer/overview/v2/prefix/live?target={url}")
            ur, dr, traffic = get_ahref_values(driver)
            ur_list.append(ur)
            dr_list.append(dr)
            ahrefs_traffic_list.append(traffic)
        else:
            ur, dr, traffic = get_ahref_values(driver)
            ur_list.append(ur)
            dr_list.append(dr)
            ahrefs_traffic_list.append(traffic)
    print(f"DR: {dr_list} UR: {ur_list} Traffic: {ahrefs_traffic_list}")
    return dr_list, ur_list, ahrefs_traffic_list


def get_alexa_rank(driver, urls):
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


def get_semrush_traffic(driver, urls):
    driver.get("https://www.thehoth.com/website-traffic/")
    try:
        time.sleep(4)
        ad_close_button = WebDriverWait(driver, 7).until(EC.presence_of_element_located(("css selector", "div.frederika-c-wrapper button.CloseButton__ButtonElement-sc-79mh24-0")))
        # ad_close_button = WebDriverWait(driver, 7).until(EC.presence_of_element_located(("id", '//*[@id="om-x5sfn8q4fabjf6flj5qz-optin"]/div/button')))
        ad_close_button.click()
    except Exception as e:
        print(e)

    else:
        text_area = WebDriverWait(driver, 3).until(EC.presence_of_element_located(("id", "targeturl")))
        for url in urls:
            text_area.send_keys(url+"\n")
        time.sleep(1)
        submit = driver.find_element("css selector", "form.form div.mt-3 button.btn-dark")
        submit.click()


def cleanup(driver):
    driver.close()
    driver.quit()
    driver = None
    print("IN CLEANUP")


def main_program():
    driver = get_driver()
    while sheets.to_repeat():
        urls = sheets.input_websites()
        urls = urls[:3]
        print(urls)
        DA_list, SS_list, PA_list = get_da_pa_ss(driver, urls)  # DA_list, SS_list, Alexa_list = get_values(driver, urls)
        dr_list, ur_list, ahrefs_traffic_list = get_dr_ur_ahrefs_traffic(driver, urls)
        alexa_list = get_alexa_rank(driver, urls)
        print(alexa_list)
        data_list = []
        print(f"DA:{len(DA_list)}, SS:{len(SS_list)}, PA:{len(PA_list)}, DR:{len(dr_list)}, UR:{len(ur_list)}, ahrefs traffic:{len(ahrefs_traffic_list)}, Alexa Rank:{len(alexa_list)}")
        print("creating a datalist")
        for i in range(0, len(SS_list)):
            data_list.append([DA_list[i], SS_list[i], PA_list[i], ur_list[i], dr_list[i], ahrefs_traffic_list[i], alexa_list[i]])  # data_list.append([DA_list[i], SS_list[i], Alexa_list[i]])
        print(data_list)
        sheets.updating_sheet(data=data_list)
        print("sheet filled")
    cleanup(driver)

#######
# driver.get("https://websiteseochecker.com/domain-authority-checker/")
#
# search = driver.find_element("name", "checkURL")
# for url in urls:
#     search.send_keys(url+"\n")
# time.sleep(2)
#
# solve_captcha(driver)
#
# analyse_btn = WebDriverWait(driver, 7).until(EC.element_to_be_clickable(("id", "formsubmitbutton")))
# analyse_btn.click()
#
# time.sleep(10)
# values = driver.find_elements("css selector", "table#tblresult tbody tr td")
# values_str = [value.text for value in values]
# DA_list = values_str[1::18]  # [for i in range(1, len(values_str), 10)]
# SS_list = values_str[7::18]  # [for j in range(7, len(values_str), 10)]
# Alexa_list = values_str[10::18]  # [for k in range(10, len(values_str), 10)]
# print(values_str)


# for i in range(0, len(DA_list)):
#     data = [DA_list[i], SS_list[i], Alexa_list[i]]
#     sheets.write(data=data)

#############
# driver = get_driver()
# urls = sheets.input_websites()
# # # get_dr_ur_ahrefs_traffic(driver, urls)
# get_alexa_rank(driver, urls)
# get_semrush_traffic(driver, urls)