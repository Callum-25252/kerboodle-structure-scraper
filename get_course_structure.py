from kb import LoginToKerboodle
from list import CourseList
import pickle
import html

if __name__ == '__main__':
    credentials_frontend = {
        'user': '',
        'pass': '',
        'inst': ''
    }

    frontend_session = LoginToKerboodle(credentials_frontend, website="frontend")
    course_list = CourseList(frontend_session.driver).get_course_list()
    tidied_course_list = []
    for item in course_list:
        cleansed_value = html.unescape(item)
        tidied_course_list.append(cleansed_value)

    with open('./data/cl.pickle', 'wb') as handle:
        pickle.dump(tidied_course_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
