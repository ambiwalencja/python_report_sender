import yagmail
import requests
import json
import xlsxwriter
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

class Mailbox:
    def __init__(self):
        self.username = ''
        self.password = ''

    def register_mailbox(self, my_username):
        self.username = my_username
        self.password = input(f'Please write the password for user {self.username}:')
        yagmail.register(self.username, self.password)
        return True


class Email:  # to może być modelem, jeśli chciałabym zapisywać to do bazy danych
    def __init__(self):
        self.subject = ''
        self.content = ''
        self.attachment = ''
        # self.recipient = ''

    def create_email(self, filename):
        self.subject = "Podsumowanie konsultacji"
        self.content = "Wysyłam podsumowanie konsultacji za ostatni miesiąc"
        self.attachment = f'attachments/{filename}.xlsx'
        return True

    def send_email(self, my_username, recipient):
        yag = yagmail.SMTP(my_username)  # to może przestać działać, jak wrzucę to na serwer. możliwe, że trzeba będzie
            # wtedy poprosić digital ocean, żeby zezwolili  na wysyłanie maili (otwarcie portu 465)
        yag.send(recipient, self.subject, self.content, self.attachment)
        return True


class ApiData:
    def __init__(self):
        self.token_file = "token.txt"  # dodatkowy model trzymający wyłącznie autoryzację
        self.refresh_token_file = "refresh_token.txt"
        self.task_list = []
        self.meeting_list = []
        self.mentor_list = []

    def get_token_from_refresh_token(self):
        request_url = os.environ.get('TOKEN_URL')
        response = requests.post(
            request_url,
            data= {
                'grant_type': 'refresh_token',
                'scope': 'openid offline_access future-collars.api',
                'refresh_token': self.get_token_from_file(self.refresh_token_file)  # one-time
            },
            headers={
                'authorization': os.environ.get('AUTHORIZATION')
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
        response = requests.post(
            url,
            json=request_params,
            headers={
                'authorization': f'Bearer {self.get_token_from_file(self.token_file)}'
            }
        )
        return response.json()

    def get_task_list(self, date_from, date_to):
        # to mogłoby być w pliku models.py jako metoda tej klasy/modelu autoryzacyjnego
        request_url = os.environ.get('TASKS_URL')
        request_params = {
                'DateCreatedFrom': date_from,
                'DateCreatedTo': date_to
            }
        self.task_list = self.get_data(request_url, request_params)
        return True
        # zamiast tworzyć listę tasków to będę wpisywać każdy task jako rekord do bazy danych w modelu Task

    def filter_tasks_by_close_date(self):
        temporary_task_list = []
        for task in self.task_list:
            if task['DateCompleted'] == None:
                continue
            else:
                date_of_completion = datetime.strptime(task['DateCompleted'][0:10], '%Y-%m-%d')
                date = datetime.today() - relativedelta(months=1)
                if date_of_completion.month == date.month:
                    temporary_task_list.append(task)
        self.task_list = temporary_task_list
        return True

    def get_meetings_list(self, date_from, date_to):
        request_url = os.environ.get('MEETINGS_URL')
        request_params = {
                'DateFrom': date_from,
                'DateTo': date_to
            }
        self.meeting_list = self.get_data(request_url, request_params)
        return True

    def create_mentor_list(self, data):
        for element in data:
            if element['MentorName'] not in self.mentor_list:
                self.mentor_list.append(element['MentorName'])
        return True

    def create_mentor_list_static(self):
        self.mentor_list = [
            'Michał Ćwiok',
            'Przemysław Baran',
            'Joanna Hryniewicz',
            'Marcin Przybylski',
            'Maciej Jędrzejewski',
            'Arkadiusz Modzelewski',
            'Adrianna Napiórkowska',
            'Jakub Miksa',
            'Mateusz Dalba',
            'Tomasz Siarnecki',
            'Mikołaj Gronowski',
            'Rafał Kamiński',
            'Mateusz Rajek',
            'Krzysztof Mendrek',
            'Tomasz Wasilonek',
            'Agnieszka Majmurek',
            'Rafał Chełkowski',
            'Tomasz Sochacki',
            'Jakub Pisula',
            'Patryk Stępniak',
            'Ewa Kułakowska',
            'Marek Wiśniewski',
            'Bartosz Kamyszek',
            'Konrad Strzelecki',
            'Dagmara Leśniak',
            'Dominika Zeliasz',
            'Łukasz Kozarski',
            'Mateusz Wiśniewicz',
            'Artur Dwojak',
            'Michał Miętus',
            'Wojciech Niekrasz',
            'Michał Ziętkowski',
            'Robert Górzyński',
            'Izabela Taborowska',
            'Damian Wojewoda',
            'Bartosz Jarek',
            'Marcin Trochonowicz',
            'Marta Taborowska-Grącka',
            'Andżelika Kowal',
            'Rafał Kielar',
            'Natalia Nitkowska',
            'Nicol Górecka',
            'Małgorzata Kowalska',
            'Mariusz Duda',
            'Anna Kaliska',
            'Tomasz Gens',
            'Olga Wojnarowska',
            'Olga Skoczek',
            'Anna Liszewska-Molenda',
            'Aleksander Sadowski',
            'Karol Kudła',
            'Mateusz Głasek',
            'Paweł Babul',
            'Damian Marek',
            'Bazyli Chodor',
            'Rafał Juczewski',
            'Hubert Pietroń',
            'Jan Sandorski',
            'Rafał Sochacki',
            'Łukasz Daszkiewicz',
            'Daniel Ziółkowski',
            'Konrad Dziedzina',
            'Wojciech Sławiński',
            'Tomasz Różowski',
            'Mateusz Dobrychłop',
            'Hubert Kamiński'
        ]
        return True

    def filter_tasks(self, mentor_name):
        filtered_data = []
        for element in self.task_list:
            if element['MentorName'] == mentor_name:
                filtered_data.append(element)
        return filtered_data

    def filter_meetings(self, mentor_name):
        filtered_data = []
        for element in self.meeting_list:
            if '{} {}'.format(element['Mentor']['FirstName'], element['Mentor']['LastName']) == mentor_name:
                filtered_data.append(element)
        return filtered_data

    def create_files_for_mentors(self):
        # self.create_mentor_list(self.task_list)
        self.create_mentor_list_static()
        xlsx_file = XlsxFile()
        for name in self.mentor_list:
            xlsx_file.create_xlsx_file(name)
            xlsx_file.mentor_task_list = self.filter_tasks(name)
            xlsx_file.mentor_meetings_list = self.filter_meetings(name)
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

    def create_task_headers_list(self):
        headers = [
            'MentorName',
            'DateCompleted',
            'DateAssigned',
            'StudentName',
            'Metadata: AssignmentName',
            'Metadata: ProjectName',
            'DateCreated',
            'CourseName'
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
        self.workbook = xlsxwriter.Workbook(f'attachments/{filename}.xlsx')

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
            duration = timedelta(hours=int(h), minutes=int(m), seconds=float(s))
            time_sum += duration
        return str(time_sum)

    def add_summary_to_file(self):
        worksheet = self.workbook.add_worksheet('Summary')
        worksheet.write(0, 0, "Number of completed tasks")
        worksheet.write(0, 1, len(self.mentor_task_list))
        worksheet.write(1, 0, "Meetings duration sum")
        worksheet.write(1, 1, self.sum_meetings_duration())


# FUNKCJE, KTÓRE ZOSTAJĄ LUZEM
# te klasy mogą własnie siedzieć w pliku utils/util, jako takie, które mogą się przydać w kilku miejscach

# def save_json_data_to_file(json_filename, data):  # funkcja robocza, aby nie wysyłac zapytania do api za kazdym razem
#     with open(json_filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)  # json.dump puts the data into file
#     return True
#
#
# def read_data_from_json_file(filename): # funkcja robocza 2
#     with open(filename, encoding="utf8") as json_file:  # musialam dodać encoding, bo inaczej nie chciało czytać
#         data = json.load(json_file)
#     return data


def set_date():  # sets date range to the month before current one
    date_from = datetime.today()
    date_from = date_from.replace(day=1)
    date_to = date_from - timedelta(days=1)
    date_from = date_from - relativedelta(months=1)
    date_from = '{}T00:00:00.000Z'.format(date_from.strftime('%Y-%m-%d'))
    date_to = '{}T23:59:59.999Z'.format(date_to.strftime('%Y-%m-%d'))
    return date_from, date_to


# version of date setting for tasks, to catch tasks from previous month that were completed that month
def set_date_2_months():
    date_from = datetime.today()
    date_from = date_from.replace(day=1)
    date_to = date_from - timedelta(days=1)
    date_from = date_from - relativedelta(months=2)  # we take tasks from 2 months and then filter by close date
    date_from = '{}T00:00:00.000Z'.format(date_from.strftime('%Y-%m-%d'))
    date_to = '{}T23:59:59.999Z'.format(date_to.strftime('%Y-%m-%d'))
    return date_from, date_to
