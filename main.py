from tkinter import *
import tkinter.ttk
from kb import LoginToKerboodle
from list import CourseList
import pickle
import html
import csv
import threading


class Application(Frame):

    def __init__(self, master=None, Frame=None):
        Frame.__init__(self, master)
        super(Application, self).__init__()
        self.grid(column=5, row=20, padx=50, pady=50)
        self.cleansed_value = None
        self.course_combo = None
        self.status_message = None
        self.message1 = StringVar()
        self.credentials = {'user': '', 'pass': '', 'inst': ''}

        self.create_widgets()

    def create_widgets(self):
        Label(text='Kerboodle Course Structure Generator').grid(row=1, column=1, sticky='w', pady=10, padx=10)
        Label(text='Select Course:').grid(row=2, column=1, sticky='w', pady=2, padx=10)

        self.course_combo = tkinter.ttk.Combobox(width=50, state="readonly")
        self.course_combo.grid(row=6, column=1, sticky='w', pady=2, padx=10)

        # start button grid
        f1 = Frame()
        Button(f1, text='Get course structure', command=self.start_thread).pack(side="left", padx=5)
        Button(f1, text='Exit', command=self.start_thread).pack(side="left", padx=5)
        f1.grid(row=8, column=1, sticky='w', padx=5)

        self.message1.set('')
        self.status_message = Label(textvariable=self.message1)
        self.status_message.grid(column=1, row=7, sticky='w', padx=10)

    def output_to_csv(self, p_list):
        print(p_list)
        keys = p_list[0].keys()
        with open(self.cleansed_value + '.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(p_list)

    def populate_dropdown(self):
        print('hello world')
        course_list = self.get_existing_course_list()
        max_length = max(course_list, key=len)
        self.course_combo['values'] = course_list
        self.course_combo['width'] = len(max_length)

    def start_thread(self):
        threading.Thread(target=self.get_course_info).start()
        print('made it here')

    def get_course_info(self):
        selected_value = self.course_combo.get()
        if selected_value:
            # SIGN INTO KERBOODLE
            self.message1.set('Connecting to Kerboodle...')
            self.cleansed_value = html.unescape(selected_value)
            session = LoginToKerboodle(self.credentials, website="frontend")

            # GET STRUCTURE DATA
            self.message1.set('Getting folder structure data...')
            path_list = CourseList(session.driver).get_path_list(self.cleansed_value)

            # GET COURSE DATA
            self.message1.set('Tidying stuff up...')
            course_list = CourseList(session.driver).get_course_list()

            # OUTPUT TO CSV
            self.message1.set('Outputting data to CSV...')
            self.save_new_course_list(course_list)
            if path_list:
                self.output_to_csv(path_list)
                self.message1.set('Success!')
            else:
                self.message1.set('No folder structure detected for selected course')
            session.driver.close()
        else:
            self.message1.set('Invalid selection! Please select a course from the dropdown')

    @staticmethod
    def save_new_course_list(course_list):
        tidied_course_list = []
        for item in course_list:
            cleansed_value = html.unescape(item)
            tidied_course_list.append(cleansed_value)
        with open('./data/cl.pickle', 'wb') as handle:
            pickle.dump(tidied_course_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def get_existing_course_list():
        with open('./data/cl.pickle', 'rb') as handle:
            cl = pickle.load(handle)
        return cl


app = Application()
app.master.title('Get Kerboodle Course Structure')
app.after(0, app.populate_dropdown)
app.mainloop()
