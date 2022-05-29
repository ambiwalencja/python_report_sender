from classes import ApiData, set_date, set_date_2_months

my_data = ApiData()
my_data.get_token_from_refresh_token()
my_data.get_task_list(set_date_2_months()[0], set_date_2_months()[1])
my_data.filter_tasks_by_close_date()
my_data.get_meetings_list(set_date()[0], set_date()[1])
my_data.create_files_for_mentors()

