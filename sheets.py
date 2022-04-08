
from pprint import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join('Sheets-key.json'), scopes) #access the json key you downloaded earlier
file = gspread.authorize(credentials)

# file = gspread.service_account(os.path.join(os.path.dirname(os.path.dirname(__file__)),'utils/Sheets-key.json')  # access the json key you downloaded earlier

# # creating and sharing a spreadsheet

# new_file = file.create("DA_Checker")
# new_file.share('magesvijay2000@gmail.com', perm_type='user', role='writer')

sheet = file.open("DA_Checker")  # open sheet
sheet = sheet.sheet1  # replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1


def input_websites(NO_OF_WEBSITE=7)-> list:
    
    da_list = sheet.col_values(2)
    da_list.remove(da_list[0])
    indexx = len(da_list)
    print(indexx," No. of Data Found")
 
    web_list = sheet.col_values(1)
    print(len(web_list)," No. of WEbsite")

    web_list.remove(web_list[0])
    
    if len(web_list[indexx:]) <= 20:
        print(f"Total no of inputs are {len(web_list[indexx:])}")
        web_list=  web_list[indexx:]
    elif len(web_list[indexx:]) > 20:
        print(f"real Total no of inputs are {len(web_list[indexx:])}")
        print(f"Total no of inputs are {len(web_list[indexx:(indexx + 20)])}")
        web_list =  web_list[indexx:(indexx + 20)]
    for i in range(len(web_list)):
            if "http" not in web_list[i]:
                web_list[i] = "http://"+ web_list[i]
    web_list = web_list[:NO_OF_WEBSITE]
    print("Getting Data:")
    pprint(web_list)
    return web_list

def get_website_for_ahref(NO_OF_WEBSITE_PER_SCRIPT = 200):
    sheet = file.open("DA_Checker")  # open sheet
    sheet = sheet.sheet1  # replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

    websit_list = sheet.col_values(1)
    websit_list.remove(websit_list[0])
    UR_LIST = sheet.col_values(5)
    UR_LIST.remove(UR_LIST[0])

    # Website list with no data
    websit_list = websit_list[len(UR_LIST):]

    websit_list = websit_list[:NO_OF_WEBSITE_PER_SCRIPT]
    for i in range(len(websit_list)):
        if "http" not in websit_list[i]:
            websit_list[i] = "http://"+ websit_list[i]
    
    return websit_list


def to_repeat(isUR=False):
    if isUR==False:
        if len(sheet.col_values(2)) != len(sheet.col_values(1)):
            return True
        else:
            print("No more Data Found Exiting !")
            return False
    else:
        if len(get_website_for_ahref()) == 0:
            print("No more Data Found Exiting !")
            return False
        else:
            return True
            


def updating_sheet(data,forAhref=False):
    print("filling the sheets")
    if forAhref==False:
        da_list = sheet.col_values(2)
        da_list.remove(da_list[0])
        n1 = len(da_list) + 2
        n2 = n1 + len(input_websites()) - 1
        print(f"B{n1}:H{n2} is to be filled")
        sheet.update(f"B{n1}:H{n2}", data)
    else:
        ur_list = sheet.col_values(5)
        ur_list.remove(ur_list[0])
        n1 = len(ur_list) + 2
        
        n2 = n1 +  len(get_website_for_ahref())- 1  
        print(f"E{n1}:G{n2} is to be filled")
        sheet.update(f"E{n1}:G{n2}", data)

# updating_sheet([[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]],forAhref=True)
# print(sheet.get_all_records())  # gets all the values of the worksheet in the format of dictionary
# print(sheet.col_values(1))
# print(input_websites())
# print(to_repeat(isUR=True))
# pprint(sheet.col_values(5))