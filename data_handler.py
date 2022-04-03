import requests
import json
import xlsxwriter
# getting the data from portal.futurecollars


class ApiData:
    def __init__(self):
        self.token_file = "token.txt"
        self.request_url = ''
        self.request_params = {}

    def get_token(self):
        with open(self.token_file, "r") as file:
            access_token = file.readline()
        return access_token

    def get_token_from_refresh_token(self):
        pass

    def get_data(self, url, request_params):
        self.request_url = url
        response = requests.post(
            self.request_url,
            json=request_params,
            headers={
                'authorization': f'Bearer {self.get_token()}'
            }
        )
        return response.json()

    def get_task_list(self):
        self.request_url = 'https://api.portal.futurecollars.com/api/query/' \
                           'FutureCollars.Core.Contracts.Mentor.MentorTasks.Queries.MentorTasksHistory'
        self.request_params = {
                'DateCreatedFrom': "2022-03-02T00:00:00.000Z",
                'DateCreatedTo': "2022-04-02T23:59:59.999Z"
            }
        return self.get_data(self.request_url, self.request_params)

    def get_meetings_list(self):
        self.request_url = 'https://api.portal.futurecollars.com/api/query/' \
                           'FutureCollars.Core.Contracts.Mentor.Statistics.Queries.PersonalMeetingsStatistics'

        self.request_params = {
                'DateFrom': "2022-03-02T00:00:00.000Z",
                'DateTo': "2022-04-02T23:59:59.999Z"
            }
        return self.get_data(self.request_url, self.request_params)


def save_json_data_to_file(json_filename, data):
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # json.dump puts the data into file
    return True


def read_data_from_json_file(filename):
    with open(filename, encoding="utf8") as json_file:  # musialam dodać encoding, bo inaczej nie chciało czytać
        data = json.load(json_file)
    return data


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


def create_mentor_list(data): # funkcja do opracowania
    mentor_list = []
    for task in data:
        if task['MentorName'] not in mentor_list:
            mentor_list.append(task['MentorName'])
    return mentor_list


def filter_data(mentor_name, data):
    filtered_data = []
    for task in data:
        if task['MentorName'] == mentor_name:
            filtered_data.append(task)
    return filtered_data


def create_files_for_mentors(mentor_list, data):
    for name in mentor_list:
        save_data_to_file(name, filter_data(name, data))
    return True




# ___________________________________________________________________________________________________________
# print(get_data()[0]["MentorName"])  # just test
# save_data_to_file(get_data())  # this i run once for writing data to file so i can use it for the further development

# my_data = read_data_from_json_file('data.json')
# save_data_to_file('test', my_data)  # just test
# my_mentor_list = create_mentor_list(my_data)
# create_files_for_mentors(my_mentor_list, my_data)
# print(my_mentor_list)
# print(len(my_filtered_data))

my_data = ApiData()
save_json_data_to_file('tasks2.json', my_data.get_task_list())