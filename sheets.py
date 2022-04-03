from operator import index
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


def input_websites()-> list:
    print("Taking the inputs from spreadsheet")
    da_list = sheet.col_values(2)
    da_list.remove(da_list[0])
    indexx = len(da_list)
    print(indexx," No. of Data Found")
 
    web_list = sheet.col_values(1)
    print(len(web_list)," No. of WEbsite")

    web_list.remove(web_list[0])
    if len(web_list[indexx:]) <= 20:
        print(f"Total no of inputs are {len(web_list[indexx:])}")
        return web_list[indexx:]
    elif len(web_list[indexx:]) > 20:
        print(f"real Total no of inputs are {len(web_list[indexx:])}")
        print(f"Total no of inputs are {len(web_list[indexx:(indexx + 20)])}")
        return web_list[indexx:(indexx + 20)]


def to_repeat():
    if len(sheet.col_values(2)) != len(sheet.col_values(1)):
        return True
    else:
        return False


def updating_sheet(data):
    print("filling the sheets")
    da_list = sheet.col_values(2)
    da_list.remove(da_list[0])
    n1 = len(da_list) + 2
    n2 = n1 + len(input_websites()) - 1
    print(f"B{n1}:H{n2} is to be filled")
    sheet.update(f"B{n1}:H{n2}", data)

# print(sheet.get_all_records())  # gets all the values of the worksheet in the format of dictionary
# print(sheet.col_values(1))
# print(input_websites())
