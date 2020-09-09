class CustomErrorHandler:
	"""docstring for CustomErrorHandler"""

	PAGE_LOADING_TEXT = "Loading took too much time, on page {}"
	PAGE_IS_READY = "Page {} is ready!"
	FIND_ELEMENT_TEXT = "Cannot find {} element"
	FIND_ELEMENT_TEXT_AND_CLICK_ON_IT = "Cannot find {} element and click on it"
	FIND_ELEMENT_TEXT_AND_TYPE_TO_IT = "Cannot find {} element and type into it"
	JS_CODE_ERROR = "Cannot run your js!"

	def __init__(self):
		super(CustomErrorHandler, self).__init__()
		

	def print_page_loading_error(self, path):
		print(self.PAGE_LOADING_TEXT.format(path))

	def page_is_ready(self, path):
		print(self.PAGE_IS_READY.format(path))

	def print_find_element_error(self, element):
		print(self.FIND_ELEMENT_TEXT.format(element))

	def print_find_element_and_click_on_it_error(self, element):
		print(self.FIND_ELEMENT_TEXT_AND_CLICK_ON_IT.format(element))

	def print_find_element_and_type_to_it(self, element):
		print(self.FIND_ELEMENT_TEXT_AND_TYPE_TO_IT.format(element))

	def print_js_error(self):
		print(self.JS_CODE_ERROR)


















