import requests
import json

# getting the data from portal.futurecollars


def get_data():
    with open("token.txt", "r") as file:
        access_token = file.readline()
    request_url = 'https://api.portal.futurecollars.com/api/query/FutureCollars.Core.Contracts.Mentor.MentorTasks.Queries.MentorTasksHistory'
    response = requests.post(
        request_url,
        json={ # jak tutaj było "data" to nie działało (był błąd 400 bad request), po zmianie na json zadziałało!
            'DateCreatedFrom': "2022-02-19T00:00:00.000Z",
            'DateCreatedTo': "2022-03-19T23:59:59.999Z"
        },
        headers={
            'authorization': f'Bearer {access_token}'
            # 'authorization': access_token
        }
    )
    return response.json()


def save_json_data_to_file(json_filename, data):
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # json.dump puts the data into file
    return True


def save_data_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(data))
    return True


def read_data_from_json_file(filename):
    with open(filename, encoding="utf8") as json_file:  # musialam dodać encoding, bo inaczej nie chciało czytać
        data = json.load(json_file)
    return data


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


def create_files_for_mentors(mentor_list, data): # to mi na razie tworzy pliki z zapisanymi listami
    for name in mentor_list:
        save_data_to_file(f'{name}.txt', filter_data(name, data))
    return True

# print(get_data()[0]["MentorName"])  # this lets me check how does my data look
# save_data_to_file(get_data())  # this i run once for writing data to file so i can use it for the further development

# read_data_from_file('data.json')
# print(read_data_from_file('data.json')[0]["MentorName"])


my_data = read_data_from_json_file('data.json')
# my_filtered_data = filter_data('Arkadiusz Radek', my_data)
# save_data_to_file('Arkadiusz_Radek.txt', my_filtered_data)
my_mentor_list = create_mentor_list(my_data)
create_files_for_mentors(my_mentor_list, my_data)
# print(my_mentor_list)
# print(len(my_filtered_data))
