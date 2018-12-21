import json
import re


class CourseList:

    def __init__(self, driver):
        self.course = None
        self.course_id = None
        self.structure_dict = None
        self.driver = driver

    def get_course_list(self):
        self.driver.get('https://www.kerboodle.com/app')
        try:
            dropdown = self.driver.find_element_by_xpath('//a[@class="dropdown-toggle"]')
            dropdown.click()
        finally:
            print(self.driver.current_url)
            element_list = self.driver.find_elements_by_xpath('//div[@id="courses-dropdown"]//li//a')
            c_list = []
            for element in element_list:
                c_list.append(element.get_attribute('innerHTML'))
            return c_list

    def get_path_list(self, course):
        self.course = course
        self.course_id = self._get_unique_course_id()
        self.structure_dict = self._get_structure_data()
        if len(self.structure_dict) == 0:
            return False
        return self._extract_children(self.structure_dict)

    def _get_unique_course_id(self):
        print('Getting course information from frontend...')
        dropdown = self.driver.find_element_by_xpath('//a[@class="dropdown-toggle"]')
        dropdown.click()
        target_course = self.driver.find_element_by_xpath('//a[contains(text(),"' + self.course + '")]')
        target_course.click()
        unique_course_id = re.sub("[^0-9]", "", self.driver.current_url)
        return unique_course_id

    def _get_structure_data(self):
        print('Getting course structure info...')
        structure_url_template = 'https://www.kerboodle.com/api/courses/[COURSE_ID]/structures'
        structure_url = structure_url_template.replace('[COURSE_ID]', self.course_id)
        self.driver.get(structure_url)
        structure_string = self.driver.find_element_by_tag_name('pre').text
        dct = json.loads(structure_string)
        return dct

    def _extract_children(self, iterable, level=0, path="", p_list=None):
        # initialise list to avoid having a mutable value in the function declaration
        # this caused the function to 'remember' the value of path_list between calls
        if p_list is None:
            p_list = []

        for idx, item in enumerate(iterable):
            # define path of current item
            if level == 0:
                c_path = item['name']
            else:
                c_path = path + ' > ' + item['name']

            # add to path list
            current_path = {'path': c_path, 'id': item['id']}
            p_list.append(current_path)

            # if the current level has children values then go another level deeper by
            # recursively calling reduce_dict
            if len(item['children']) > 0:
                self._extract_children(item['children'], level=level + 1, path=c_path, p_list=p_list)

        # ending condition
        if level == 0:
            return p_list
