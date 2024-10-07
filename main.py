import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""NOTES:
-the file reading system needs to be able to separate lists of accounts. 
Idea: The first line of the .txt file acts as a dictionary. The # character separates each entry, and the character after the # indicates what type of data it is. This is followed
by the username of the person that it's related to. For instance, if #F indicates a follower list, then #FJane_Doe02 would represent the follower list of Jane_Doe02. There should
be a function to create a dictionary using the first line, where the keys are the pound signs with the identifying character and username, and the values are ints that represent
the line numbers in the text file in which the corresponding array of accounts can be found. #F represents a follower list, #f represents a following list.
In the dictionary, the hashtags are omitted, so the keys are preceded by F or f only.



"""


#CLASS DEFINITIONS
class Account:
    name = ""
    tag = ""
    #following and followers should be sets of accounts
    following = 0
    followers = 0

    #def __init__(self)
    
    #accounts is a set of accounts
    #def check_for_changes(self, accounts)

class Changes:
    #can use set.contains() here. these are both sets of accounts
    new_accounts = 0
    missing_accounts = 0

    #def __init__(self, previous_account_set, new_account_set)


#METHODS
#returns the name of a file without leaving it open, creating it if needed
def open_or_create_save_file(user: str):
    with open(str(user) + ".txt", "a") as file:
        return file.name

#note that line 0 is the first line, not line 1
def write_to_line(file_name, line_to_append, text_to_add):
    #turns the file into a list of strings, adds the string to the specified line, and then overwrites the entire file with the list of strings, effectively applying the changes to
    # the target line
    lines = ""
    with open(file_name, 'r') as file:
        #looks like I have to add a character here if it's a new file, or else readlines() returns nothing
        lines = file.readlines()
        if lines == []:
            lines = [""]
            lines[line_to_append] += text_to_add
        #if the last char of the first line is a new line, remove it
        elif lines[0][len(lines[0]) - 1] == '\n':
            lines[0] = lines[0][0 : len(lines[0]) - 1]
            lines[line_to_append] += text_to_add + '\n'
    with open(file_name, 'w') as file:
        file.writelines(lines)

def overwrite_line(file_name, line_to_overwrite, text_to_add):
    #turns the file into a list of strings, replaces the specified line with the string, and then overwrites the entire file with the list of strings, effectively applying the changes to
    # the target line
    lines = ""
    with open(file_name, 'r') as file:
        lines = file.readlines()
        lines[line_to_overwrite] = text_to_add + '\n'
    with open(file_name, 'w') as file:
        file.writelines(lines)

#converts a string to a set
def line_to_set(line):
    current_element = ""
    out = set()
    for char in line:
        if char == ',':
            out.add(current_element)
            current_element = ""
        else:
            current_element += char
    return out

#reads an existing save file and converts it to a dictionary
def initialize_dictionary(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        current_key = ""
        c = 1
        hashtag_count = 0
        dictionary = {}
        for char in lines[0]:
            if char == '#':
                hashtag_count += 1
                #the second hashtag signals the beginning of the next key
                if hashtag_count == 2:
                    dictionary[current_key] = line_to_set(lines[c])
                    hashtag_count = 1
                    c += 1
                    current_key = ""
            elif char == '\n':
                #do nothing
                pass
            else:
                current_key += char
        #add the last element, which does not have a # after it
        dictionary[current_key] = line_to_set(lines[c])
        return dictionary

#writes a new list of followers/following
#data_set is a set of Accounts. this is for sets that weren't previously tracked. 'o' overwrites an
# existing line, so this is for overwriting sets that have changed since the last time they were written, updating them. 
# data_type is F for follower list or f for following list.
def overwrite_save_file_line(file_name: str, data_set: set, account_name: str, data_type: str):
    #add to the index, line 0
    write_to_line(file_name, 0, '#' + data_type + str(account_name))
    #append the new line
    with open(file_name, "a") as file:
        file.write("\n")
        c = 1
        for acc in data_set:
            file.write(acc)
            #separate each account with a comma. there should be a comma at the end, too
            file.write(',')

#overwrites an existing line, so this is for overwriting sets that have changed since the last time they were written, updating them.
def write_to_save_file(file_name: str, data_set: set, line_to_overwrite: int):
    with open(file_name, "a") as file:
        line = ""
        c = 1
        for acc in data_set:
            line += acc
            #separate each account with a comma
            line += ','
            #to find the line to write to here, we first need to have the dictionary so we can find the index of the key
        overwrite_line(file_name, line_to_overwrite, line)

#overload of above, with different parameters.
#def write_to_save_file(file_name: str, data_set: set, account_name: str, data_type: str):
    #want a method to return the line of info given the account name and data type. Should the save file be a class?


#compares 2 sets. returns a list containing 2 sets. the first set is the items missing from the new set, and the second is the items missing from the old set.
def compare_set(old_set: set, new_set: set):
    missing_items = old_set.difference(new_set)
    new_items = new_set.difference(old_set)
    return [missing_items, new_items]
    
            
            
"""
#get username and password from user - allow user to use previous credentials with a number menu?
username = input("Input instagram username, phone number, or email: \n")
password = input("Input instagram password: \n")

browser = webdriver.Chrome()

browser.get('https://instagram.com')

#time.sleep(1.5)
#Wait 15 seconds or until the login button is clickable (whichever is sooner) before attempting to locate the elements
WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))

#locating the username and password fields using their xpaths, which are found in chrome's inspect menu
username_field = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
password_field = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
login_button = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]')

#type in username and pw
username_field.send_keys(username)
password_field.send_keys(password)
login_button.click()

#If we are here then the credentials were valid, so now we either open or create a new txt file to save the data in
save_file_name = open_or_create_save_file(username)

#make it loop back to the beginning if credentials are incorrect

profile_button = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a')))
profile_button.click()

time.sleep(15)"""


testSet = {"kid","named","finger","jijijija"}
#test writing to a save file
overwrite_save_file_line(open_or_create_save_file("test_save"), testSet, "test7", "f")
print(initialize_dictionary(open_or_create_save_file("test_save")))

