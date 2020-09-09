
import os
import sys
from time import sleep
import re 
from datetime import datetime
from WorkingWithBrowser.browser import Browser

########################### Constants ###########################
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCES_PATH = f"{ROOT_PATH}/Sources"
SYSTEM32_FILES = f"{SOURCES_PATH}/system32"
ACCESS_FILE_PATH = f"{SOURCES_PATH}/Access"
OUTPUT_PATH = f"{SOURCES_PATH}/output"

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


ROW = 2

COL = 1

LIST_OF_ACCESS = {input("Введите чистое доменное имя: "):{
	'login_path': input("Введите ссылку на авторизацию: "),
	'login_name': input("Введите логин: "),
	'login_password': input("Введите пароль: ")
}}

DATABASE_NAME = input("Введите название базы данных: ")
DATABASE_PREFIX = input("Введите префикс базы данных: ")
USERNAME = input("Введите логин админа сайта: ")
EMAIL = input("Введите email админа: ")

print("Выберите ваш путь:\n1)Разблокировать админку\n2)Сменить пароль в Modx Evolution\n3)Сменить пароль в Modx Revolution")
print("Писать только цифры иначе все.")

SQL_QUERY = ""

SQL_QUERY_DICT = {
	"1":f"UPDATE {DATABASE_PREFIX}user_attributes SET `blocked`=0, `blockeduntil`=0, `blockedafter`=0, `logincount`=0, `failedlogincount`=0 WHERE `email`='{EMAIL}'",
	"2": "UPDATE {DATABASE_PREFIX}manager_users SET `password`=MD5('{PASSWORD}') WHERE `username`='{USERNAME}'",
	"3": "UPDATE {DATABASE_PREFIX}users SET `password`=MD5('{PASSWORD}'), `salt`='', `hash_class`='hashing.modMD5' WHERE `username`='{USERNAME}' AND `sudo`=1"
}



try:
	destiny = int(input("Выбери свою сторону: "))
	if not destiny in [1, 2, 3]:
		sys.exit("Нужно выберать путь из существующих.")
	if destiny == 2 or destiny == 3:
		pss = input("Введите желаемый пароль: ")
		SQL_QUERY_DICT[str(destiny)] = SQL_QUERY_DICT[str(destiny)].format(DATABASE_PREFIX=DATABASE_PREFIX,PASSWORD=pss, USERNAME=USERNAME)
	SQL_QUERY = SQL_QUERY_DICT[str(destiny)]

except Exception as e:
	print(e)
	sys.exit("Выберать путь нужно цифрами.")

print(SQL_QUERY)

FIREFOX_BINARY = f"{SYSTEM32_FILES}/firefox/firefox"
GECKODRIVER_BINNARY = f"{SYSTEM32_FILES}/geckodriver-src/geckodriver"
PAGE_LOADING_DELAY = 20
SLEEP_DELAY = 5

PART_OF_PANEL_LINK_FOR_ALL_SITES = "smb/web/view/"
PART_OF_PANEL_LINK_FOR_STATISTICS = "smb/statistics/details/"

SEARCHABLE_FILE_FOR_DATABASE_NAME = "config"



global FALSE_BACKUP_DICT
FALSE_BACKUP_DICT = {}

global ERROR_COUNTER
ERROR_COUNTER = 0

COUNT_OF_ALL_SITES = len(LIST_OF_ACCESS.items())

########################### Constants ###########################


print(LIST_OF_ACCESS)


########################### Inits ###########################

try:
	browser = Browser(FIREFOX_BINARY, GECKODRIVER_BINNARY,PAGE_LOADING_DELAY,SLEEP_DELAY, True)
except Exception as e:
	os.system("pkill firefox-bin")
	os.system("pkill geckodriver")
	browser = Browser(FIREFOX_BINARY, GECKODRIVER_BINNARY,PAGE_LOADING_DELAY,SLEEP_DELAY, True)


########################### Inits ###########################


def login_into_hosting_panel(browser: 'Browser with Selenium instances', path: 'link to login page', login: 'username for sing in', password: 'password for sign in'):
	print('\n\tLog in to hosting panel')

	browser.go_to_and_wait_until(path, 'id', 'loginSection')
	login_input = browser.find_element('id','login_name')
	if not login_input:
		return False
	password_input = browser.find_element('id','passwd')
	submit_btn = browser.find_element('class_name', 'pul-button.pul-button--lg.pul-button--primary.pul-button--fill')
	browser.type_to_element(login_input, login)
	browser.type_to_element(password_input, password)
	browser.click_on_element(submit_btn)
	is_loggin = browser.find_element_and_wait_until(15,'id', 'buttonAddDomain', None)
	if is_loggin: return True

	return False




def login_to_php_my_admin(browser: Browser, path:str, needed_db_base_name: str, site_url: str, sql_query: str):


	browser.go_to_and_wait_until(f"{path}smb/database/list", 'id', 'databases-active-list')

	try:
		all_db_blocks = browser.find_elements('class_name', 'active-list-item')
		needed_db_block = ""
		for block in all_db_blocks:
			try:
				text = re.search(needed_db_base_name, block.text)
			except:
				continue
			if(text is not None and text != ''):
				needed_db_block = block
				break
			else:
				continue
		if needed_db_block:
			find_all_links = browser.find_elements_from(needed_db_block, 'tag_name', 'a')
			for link in find_all_links:
				db_attr = link.get_attribute('data-action-name')
				if db_attr == 'openWebAdmin':
					browser.click_on_element(link)
					sleep(3)		

		else:
			print('VISHOL TUTT')
			return False

	except Exception as e:
		print("NE MOGU NAITI\n", e)

	browser.go_to_and_wait_until(f"{path}phpMyAdmin/db_sql.php?db={needed_db_base_name}&lang=ru", 'id', 'queryfieldscontainer')
	find_body = browser.find_element('id', 'sqlquery')
	browser.type_to_element(find_body, sql_query)
	submit_query = browser.find_element('id', 'button_submit_query')
	browser.click_on_element(submit_query)
	sleep(3)



def log_error_on_function_output(error_str, site_url):
	global FALSE_BACKUP_DICT
	global ERROR_COUNTER
	FALSE_BACKUP_DICT[site_url] = error_str
	ERROR_COUNTER += 1
	
	return FALSE_BACKUP_DICT

def logout(browser, path):
	print('\n\tLogout \n\n\n')

	try:
		browser.go_to(f"{path}logout.php")
	except Exception as e:
		print('CANNOT LOG OUT\n\t', e)
	return True



for num,site in enumerate(LIST_OF_ACCESS.items(),1):
	try:
		login_path = site[1]['login_path']

		login_username = site[1]['login_name']
		login_password = site[1]['login_password']
		site_url = site[0]
		INTERMIDIATE_PATH_TO_SITE_FOLDER = ""
		print("ENROLED NOW ==> \n\t",login_path,login_username,login_password,site_url)
		print(f"\n\tSite number #{num} <==> from {COUNT_OF_ALL_SITES}")
		print(f"\n\tError counter is = {ERROR_COUNTER}")
		logout(browser,login_path)
		sleep(2)
		try:
			with open('error.txt', "w") as file:
				file.write(str(FALSE_BACKUP_DICT))
		except Exception as e:
			print("WRTIE\t",e)

		is_signed_in = login_into_hosting_panel(browser, login_path, login_username, login_password)
		if not is_signed_in:
			log_error_on_function_output(f"Cannot to login into {site_url}",site_url)
			continue

		log_php_my_admin = login_to_php_my_admin(browser, login_path, DATABASE_NAME, site_url, SQL_QUERY)

	except Exception as e:
		print(e)
		continue
	
print(FALSE_BACKUP_DICT)

os.system("pkill firefox-bin")
os.system("pkill geckodriver")


