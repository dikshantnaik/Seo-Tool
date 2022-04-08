from operator import index
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from pprint import pprint
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


def get_website_for_ahref(NO_OF_WEBSITE_PER_SCRIPT = 10):
    sheet = file.open("DA_Checker")  # open sheet
    sheet = sheet.sheet1  # replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

    websit_list = sheet.col_values(1)
    UR_LIST = sheet.col_values(5)

    # Website list with no data
    websit_list = websit_list[len(UR_LIST):]

    websit_list = websit_list[:NO_OF_WEBSITE_PER_SCRIPT]
    for i in range(len(websit_list)):
        if "http" not in websit_list[i]:
            websit_list[i] = "http://"+ websit_list[i]
    
    return websit_list


pprint(get_website_for_ahref())
# pprint(UR_LIST)

# pprint(sheet.get_all_values())

# sheet.update("E369:G370",[[1,2,3],[3,4,5]])