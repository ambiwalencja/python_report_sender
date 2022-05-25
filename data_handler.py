from classes import ApiData, set_date, set_date_2_months
# from classes import read_data_from_json_file # ROBOCZA LINIJKA


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

# REAL PROGRAM WYWOLANIE
my_data = ApiData()
my_data.get_token_from_refresh_token()
my_data.get_task_list(set_date_2_months()[0], set_date_2_months()[1])
my_data.filter_tasks_by_close_date()
# my_data.meeting_list = my_data.get_meetings_list(set_date()[0], set_date()[1])
# wersja robocza na czas kiedy konsultacje się nie ładują:
my_data.get_meetings_list('2022-05-05T00:00:00.000Z', set_date()[1])
my_data.create_mentor_list(my_data.task_list)
my_data.create_files_for_mentors(my_data.task_list, my_data.meeting_list)

