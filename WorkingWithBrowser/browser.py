import os
import sys
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from WorkingWithErrors.custom_error_handler import CustomErrorHandler






class Browser:
	"""docstring for Browser"""

	FIREFOX_BINARY = ""
	GECKODRIVER_BINNARY = ""
	PAGE_LOADING_DELAY = ""
	SLEEP_DELAY = ""
	BROWSER = ""
	error_handler = ""
	LOCATE_BY = {
		'id': By.ID,
		'xpath': By.XPATH,
		'link_text': By.LINK_TEXT,
		'partial_link_text': By.PARTIAL_LINK_TEXT,
		'name': By.NAME,
		'tag_name': By.TAG_NAME,
		'class_name': By.CLASS_NAME,
		'css_selector': By.CSS_SELECTOR
	}


	def __init__(self, firefox_binary_v2, geckodriver_binary, page_loading_delay, sleep_delay, headless):
		super(Browser, self).__init__()
		self.FIREFOX_BINARY = FirefoxBinary(firefox_binary_v2)
		self.GECKODRIVER_BINNARY = geckodriver_binary
		self.PAGE_LOADING_DELAY = page_loading_delay
		self.SLEEP_DELAY = sleep_delay
		self.error_handler = CustomErrorHandler()
		self.init_browser(headless)		


	def init_browser(self, headless=False):
		try:

			if headless:
				options = Options()
				options.headless = True
				self.BROWSER = webdriver.Firefox(options=options,firefox_binary=self.FIREFOX_BINARY, executable_path=self.GECKODRIVER_BINNARY)
			else:	
				self.BROWSER = webdriver.Firefox(firefox_binary=self.FIREFOX_BINARY, executable_path=self.GECKODRIVER_BINNARY)

		except Exception as e:
			print(f"{e} === cannot launch browser")
			sys.exit()

	def change_tab(self):
		cc_tab = self.BROWSER.current_window_handle
		self.BROWSER.switch_to.window(cc_tab)
		sleep(2)

	def go_to(self, path):
		try:
			self.BROWSER.get(path)
		except Exception as e:
			print(e)
			self.error_handler.print_page_loading_error(path)
			return False

	def go_to_and_wait_until(self, path, whait_by, whait_target):
		try:
			self.BROWSER.get(path)
		except Exception as e:
			print('ERROM FROM go_to_and_wait_until => ',e)
			return False

		try:
			check_on_load_element = WebDriverWait(self.BROWSER, self.PAGE_LOADING_DELAY).until(EC.presence_of_element_located((self.LOCATE_BY[whait_by.lower()], whait_target)))
			return True
		except Exception as e:
			print(e)
			self.error_handler.print_page_loading_error(path)
			return False

	def find_element(self, find_by, find_target, visible=None):
		try:
			wait = WebDriverWait(self.BROWSER, self.PAGE_LOADING_DELAY)
			if visible:
				element = wait.until(EC.visibility_of_element_located((self.LOCATE_BY[find_by.lower()], find_target)))
			else:
				element = wait.until(EC.element_to_be_clickable((self.LOCATE_BY[find_by.lower()], find_target)))
			if element:
				find_element = self.BROWSER.find_element(self.LOCATE_BY[find_by.lower()], find_target)
				return find_element

		except Exception as e:
			print(e)
			self.error_handler.print_find_element_error(find_target)
			return False

	def find_elements(self, find_by, find_target):
		try:
			wait = WebDriverWait(self.BROWSER, self.PAGE_LOADING_DELAY)
			element = wait.until(EC.element_to_be_clickable((self.LOCATE_BY[find_by.lower()], find_target)))
			if element:
				find_elements = self.BROWSER.find_elements(self.LOCATE_BY[find_by.lower()], find_target)
				return find_elements

		except Exception as e:
			print(e)
			self.error_handler.print_find_element_error(find_target)
			return False

	def find_element_from(self, find_from, find_by, find_target):
		try:
			find_element = find_from.find_element(self.LOCATE_BY[find_by.lower()], find_target)
			return find_element
		except Exception as e:
			print(e)
			self.error_handler.print_find_element_error(find_target)
			return False


	def find_elements_from(self, find_from, find_by, find_target):
		try:
			find_element = find_from.find_elements(self.LOCATE_BY[find_by.lower()], find_target)
			return find_element
		except Exception as e:
			print(e)
			self.error_handler.print_find_element_error(find_target)
			return False



	def find_element_and_wait_until(self, wait_delay, find_by, find_target, prinError=True):
		while True:
			if wait_delay:
				if(wait_delay <= 0):
					return False
				sleep(3)
			try:
				find_element = self.BROWSER.find_element(self.LOCATE_BY[find_by.lower()], find_target)
				return find_element
			except Exception as e:
				if prinError:
					print(e)
				wait_delay -= 5
				continue
			wait_delay -= 5
			continue
		return False

	def find_elements_and_wait_until(self, wait_delay, find_by, find_target):

		wait_until_dealy = False
		if(wait_delay != 0 and wait_delay != None):
			wait_until_dealy = True

		while True:
			if(wait_until_dealy):
				if(wait_delay <= 0):
					return False

				wait_delay -= 1

			try:
				find_element = self.BROWSER.find_elements(self.LOCATE_BY[find_by.lower()], find_target)
				return find_element
			except Exception as e:
				print(e)
				continue



	def wait_until_the_text_is_found(self, wait_delay, find_target, path, path_find_by, path_find_target, check_by=None, check_target=None):
		is_visible_object = False
		while True:
			if wait_delay:
				if(wait_delay <= 0):
					return False
				else:
					wait_delay -= 5
			if check_target:
				is_visible_object = self.check_if_element_is_visible(check_by,check_target)
				if is_visible_object: 
					sleep(3)
					continue

			if wait_delay % 15 == 0:
				if not is_visible_object:
					if path:
						self.go_to_and_wait_until(path,path_find_by,path_find_target)
			sleep(3)
			self.run_js(f"var node_{wait_delay} = document.createElement(\"span\"); document.getElementById(\"content-body\").appendChild(node_{wait_delay});")
			try:
				bodyText = self.find_element(By.ID, 'main').text
			except Exception:
				continue
			searchably_element = re.search(f"{find_target}", bodyText)
			if searchably_element:
				return False
			else:
				sleep(3)
				continue





	def click_on_element(self, element):
		try:
			element.click()
			return True
		except Exception as e:
			print(e)
			self.error_handler.print_find_element_and_click(element)
			return False



	def type_to_element(self, element, text):
		try:
			element.send_keys(text)
			return True
		except Exception as e:
			print(e)
			self.error_handler.print_find_element_and_type_to_it(element)
			return False

	def run_js(self, js_code):

		try:
			self.BROWSER.execute_script(js_code)
			return True
		except Exception as e:
			print(e)
			self.error_handler.printJsError()
			return False

	def click_on_element_when_its_clickable(self, click_by, click_target):
		try:
			WebDriverWait(self.BROWSER, self.PAGE_LOADING_DELAY).until(EC.element_to_be_clickable((self.LOCATE_BY[click_by.lower()],click_target))).click()
			return True
		except Exception as e:
			print(e)
			return False

	def check_if_element_is_visible(self, check_by, check_target):
		try:
			WebDriverWait(self.BROWSER, 3).until(EC.visibility_of_element_located((self.LOCATE_BY[check_by.lower()],check_target)))
			return True
		except Exception:
			return False

	def get_coockie(self, by_name=None):
		cockies_ = ""
		if by_name:
			cockies_ = self.BROWSER.get_cookie(by_name)
		else:
			cockies_ = self.BROWSER.get_cookies()
		return cockies_

	def recursive_parser_dict_and_list(self, data, match):
		while True:
			if isinstance(data, (dict, list)):
				for _key, _value in (data.items() if isinstance(data, dict) else enumerate(data)):
					if _key == match or _value == match:
						return True
					else:
						data = _value
			else:
				return False

	def compare_coockie(self, find_key=None, find_value=None, find_delay=600):
		while find_delay != 0:
			if find_key:
				coockie = self.get_coockie(find_key)
			else:
				coockie = self.get_coockie()
			if coockie:
				cookie_response = self.recursive_parser_dict_and_list(coockie, find_key)
				if cookie_response:
					find_delay = 0
					return coockie
			sleep(3)
			find_delay -= 10
		return False