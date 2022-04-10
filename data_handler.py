import requests
import json
import xlsxwriter
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ApiData:
    def __init__(self):
        self.token_file = "token.txt"
        self.refresh_token_file = "refresh_token.txt"
        self.request_url = ''
        self.request_params = {}
        self.task_list = []
        self.meeting_list = []
        self.mentor_list = []  # moge raz pobrać liste mentorów z api a potem już brać z tego

    def get_token_from_refresh_token(self):
        self.request_url = 'https://api.portal.futurecollars.com/auth/connect/token'
        response = requests.post(
            self.request_url,
            data= {  # to jest niezmiennie z zakładki payload wzięte
                'grant_type': 'refresh_token',
                'scope': 'openid offline_access future-collars.api',
                'refresh_token': self.get_token_from_file(self.refresh_token_file)  # jednorazowy
            },
            headers={
                'authorization': 'Basic ZnV0dXJlLWNvbGxhcnMubWVudG9yOnNlY3JldA=='
            }
        )
        self.write_token_to_file(response.json(), 'access_token', self.token_file)
        self.write_token_to_file(response.json(), 'refresh_token', self.refresh_token_file)
        return response.json()

    def write_token_to_file(self, json_data, token_type, filename): # wyjąć z klasy?
        with open(filename, "w") as file:
            file.write(json_data[token_type])
        return True

    def get_token_from_file(self, filename): # wyjąć z klasy?
        with open(filename, "r") as file:
            token = file.readline()
        return token

    def get_data(self, url, request_params):
        self.request_url = url
        response = requests.post(
            self.request_url,
            json=request_params,
            headers={
                'authorization': f'Bearer {self.get_token_from_file(self.token_file)}'
            }
        )
        return response.json()

    def get_task_list(self, date_from, date_to):
        self.request_url = 'https://api.portal.futurecollars.com/api/query/' \
                           'FutureCollars.Core.Contracts.Mentor.MentorTasks.Queries.MentorTasksHistory'
        self.request_params = {
                'DateCreatedFrom': date_from,
                'DateCreatedTo': date_to
            }
        return self.get_data(self.request_url, self.request_params)

    def get_meetings_list(self, date_from, date_to):
        self.request_url = 'https://api.portal.futurecollars.com/api/query/' \
                           'FutureCollars.Core.Contracts.Mentor.Statistics.Queries.PersonalMeetingsStatistics'

        self.request_params = {
                'DateFrom': date_from,
                'DateTo': date_to
            }
        return self.get_data(self.request_url, self.request_params)

    def create_mentor_list(self, data):
        for element in data:
            if element['MentorName'] not in self.mentor_list:
                self.mentor_list.append(element['MentorName'])
        return self.mentor_list

    def filter_tasks(self, mentor_name, task_list):
        filtered_data = []
        for element in task_list:
            if element['MentorName'] == mentor_name:
                filtered_data.append(element)
        return filtered_data

    def filter_meetings(self, mentor_name, meeting_list):
        filtered_data = []
        for element in meeting_list:
            if '{} {}'.format(element['Mentor']['FirstName'], element['Mentor']['LastName']) == mentor_name:
                filtered_data.append(element)
        return filtered_data

    def create_files_for_mentors(self, task_list, meeting_list):
        xlsx_file = XlsxFile()
        for name in self.mentor_list:
            xlsx_file.create_xlsx_file(name)
            xlsx_file.mentor_task_list = self.filter_tasks(name, task_list)
            xlsx_file.mentor_meetings_list = self.filter_meetings(name, meeting_list)
            xlsx_file.save_tasks_to_file()
            xlsx_file.save_meetings_to_file()
            xlsx_file.add_summary_to_file()
            xlsx_file.close_workbook()
        return True


class XlsxFile:
    def __init__(self):
        self.filename = ''
        self.workbook = xlsxwriter.Workbook()
        self.task_headers_list = self.create_task_headers_list()
        self.meeting_headers_list = self.create_meeting_headers_list()
        self.mentor_task_list = []
        self.mentor_meetings_list = []
        # self.task_number_for_mentor = 0
        # self.meeting_duration_sum = ''

    def create_task_headers_list(self):
        headers = [
            'MentorName',
            'DateCompleted',
            'DateAssigned',
            'StudentName',
            'Metadata: AssignmentName',
            'Metadata: ProjectName',
            'DateCreated'
        ]
        return headers

    def create_meeting_headers_list(self):
        headers = [
            'MentorName',
            'StudentName',
            'Description',
            'MeetingDate',
            'TotalMeetingDuration',
            'Rating'
        ]
        return headers

    def create_xlsx_file(self, filename):
        self.workbook = xlsxwriter.Workbook(f'{filename}.xlsx')

    def close_workbook(self):
        self.workbook.close()

    def write_headers_to_file(self, worksheet, headers_list):
        row = 0
        col = 0
        for header in headers_list:
            worksheet.write(row, col, header)
            col += 1
        return True

    def save_tasks_to_file(self):
        worksheet = self.workbook.add_worksheet('Tasks')
        self.write_headers_to_file(worksheet, self.task_headers_list)
        row = 0
        for task in self.mentor_task_list:
            col = 0
            row += 1
            for header in self.task_headers_list:
                if header == 'Metadata: AssignmentName':
                    worksheet.write(row, col, task['Metadata']['AssignmentName'])
                    col += 1
                elif header == 'Metadata: ProjectName':
                    worksheet.write(row, col, task['Metadata']['ProjectName'])
                    col += 1
                else:
                    worksheet.write(row, col, task[header])
                    col += 1
        return True

    def save_meetings_to_file(self):
        worksheet = self.workbook.add_worksheet("Meetings")
        self.write_headers_to_file(worksheet, self.meeting_headers_list)
        row = 0
        for meeting in self.mentor_meetings_list:
            col = 0
            row += 1
            for header in self.meeting_headers_list:
                if header == 'MentorName':
                    worksheet.write(row, col, '{} {}'.format(meeting['Mentor']['FirstName'], meeting['Mentor']['LastName']))
                    col += 1
                elif header == 'StudentName':
                    worksheet.write(row, col, '{} {}'.format(meeting['Student']['FirstName'], meeting['Student']['LastName']))
                    col += 1
                else:
                    worksheet.write(row, col, meeting[header])
                    col += 1
        return True

    def sum_meetings_duration(self):
        meeting_duration_list = []
        for meeting in self.mentor_meetings_list:
            meeting_duration_list.append(meeting['TotalMeetingDuration'])
        time_sum = timedelta()
        for time in meeting_duration_list:
            (h, m, s) = time.split(':')
            duration = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            time_sum += duration
        return str(time_sum)

    def add_summary_to_file(self):
        worksheet = self.workbook.add_worksheet('Summary')
        worksheet.write(0, 0, "Number of completed tasks")
        worksheet.write(0, 1, len(self.mentor_task_list))
        worksheet.write(1, 0, "Meetings duration sum")
        worksheet.write(1, 1, self.sum_meetings_duration())


# FUNKCJE, KTÓRE ZOSTAJĄ LUZEM
def save_json_data_to_file(json_filename, data):  # funkcja robocza, aby nie wysyłac zapytania do api za kazdym razem
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # json.dump puts the data into file
    return True


def read_data_from_json_file(filename): # funkcja robocza 2
    with open(filename, encoding="utf8") as json_file:  # musialam dodać encoding, bo inaczej nie chciało czytać
        data = json.load(json_file)
    return data


def set_date():
    date_from = datetime.today()
    date_from = date_from.replace(day=1)
    date_to = date_from - timedelta(days=1)
    date_from = date_from - relativedelta(months=1)
    date_from = '{}T00:00:00.000Z'.format(date_from.strftime('%Y-%m-%d'))
    date_to = '{}T23:59:59.999Z'.format(date_to.strftime('%Y-%m-%d'))
    return date_from, date_to


# POBIERAM DANE I ZAPISUJĘ DO PLIKU
# my_data = ApiData()
# my_data.get_token_from_refresh_token()
# save_json_data_to_file('meetings.json', my_data.get_meetings_list(set_date()[0], set_date()[1]))  # wersja robocza
# save_json_data_to_file('tasks.json', my_data.get_task_list(set_date()[0], set_date()[1]))  # wersja robocza
# CZYTAM Z PLIKU I ZAPISUJĘ DO XLSX:
# my_task_list = read_data_from_json_file('tasks.json')
# my_meetings_list = read_data_from_json_file('meetings.json')
# my_data.create_mentor_list(my_task_list)
# my_data.create_files_for_mentors(my_task_list, my_meetings_list)

my_data = ApiData()
my_data.get_token_from_refresh_token()
my_data.task_list = my_data.get_task_list(set_date()[0], set_date()[1])
my_data.meeting_list = my_data.get_meetings_list(set_date()[0], set_date()[1])
my_data.create_mentor_list(my_data.task_list)
my_data.create_files_for_mentors(my_data.task_list, my_data.meeting_list)



