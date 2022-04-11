from classes import ApiData, set_date

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



