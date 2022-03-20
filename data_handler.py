import requests
import json

# and now getting the data from portal.futurecollars


def get_data():
    with open("token_2.txt", "r") as file:
        access_token = file.readline()
    request_url = 'https://api.portal.futurecollars.com/api/query/FutureCollars.Core.Contracts.Mentor.MentorTasks.Queries.MentorTasksHistory'
    response = requests.post(
        request_url,
        json={ # jak tutaj było "data" to nie działałom (był błąd 400 bad request), po zmianie na json zadziałało!
            'DateCreatedFrom': "2022-02-19T00:00:00.000Z",
            'DateCreatedTo': "2022-03-19T23:59:59.999Z"
        },
        headers={
            'authorization': f'Bearer {access_token}'
            # 'authorization': access_token
        }
    )
    return response.json()


def save_data_to_file(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_data_from_file(filename):



# def filter_data(mentor_name, response):


# print(get_data()[0]["MentorName"])

# save_data_to_file(get_data())
