import requests
import json
import xlsxwriter
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# getting the data from portal.futurecollars


class ApiData:
    def __init__(self):
        self.token_file = "token.txt"
        self.refresh_token_file = "refresh_token.txt"
        self.request_url = ''
        self.request_params = {}
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


def write_headers_to_file(worksheet, data):
    row = 0
    col = 0
    headers_dict = data[0]
    for key in headers_dict:
        if key == "Metadata":
            for metadata_key in headers_dict[key].keys():
                worksheet.write(row, col, f'{key}: {metadata_key}')
                col += 1
        else:
            worksheet.write(row, col, key)
            col += 1
    return True


def save_data_to_file(filename, data):
    workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    write_headers_to_file(worksheet, data)
    for task in data:
        col = 0
        row += 1
        for key in task:
            if key == "Metadata":
                for metadata_key in task[key].keys():
                    worksheet.write(row, col, task[key][metadata_key])
                    col += 1
            else:
                worksheet.write(row, col, task[key])
                col += 1
    workbook.close()
    return True

# TODO: trzy poniższe funkcje są do zrobienia jako metody klasy DataApi; przy okazji trzeba je dostosować tez do
# TODO: konsultacji, bo na razie działają na taskach tylko, podobnie zresztą jak zapisywanie do excela
def create_mentor_list(data): # funkcja do opracowania; ta funkcja działa bezpośrednio na danych pobranych z api, więc może być metodą klasy ApiData
    mentor_list = []
    for task in data:
        if task['MentorName'] not in mentor_list:
            mentor_list.append(task['MentorName'])
    return mentor_list


def filter_data(mentor_name, data):  # j.w.
    filtered_data = []
    for task in data:
        if task['MentorName'] == mentor_name:
            filtered_data.append(task)
    return filtered_data


def create_files_for_mentors(mentor_list, data):
    for name in mentor_list:
        save_data_to_file(name, filter_data(name, data))
    return True

# tutaj pobieram dane z api i zapisuję do pliku. działa.
my_data = ApiData()
my_data.get_token_from_refresh_token()
save_json_data_to_file('meetings.json', my_data.get_meetings_list(set_date()[0], set_date()[1]))
# my_data = read_data_from_json_file('data.json')
# save_data_to_file('test', my_data)  # just test
# my_mentor_list = create_mentor_list(my_data)
# create_files_for_mentors(my_mentor_list, my_data)


