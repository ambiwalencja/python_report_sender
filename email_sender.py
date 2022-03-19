import yagmail
import keyring
import requests


class Mailbox:
    def __init__(self):
        self.username = ''
        self.password = ''

    def register_mailbox(self, my_username):
        # username = input("Please write your username:")
        # self.username = 'helena.sokolowska.dev'
        self.username = my_username
        self.password = input(f'Please write the password for user {self.username}:')
        # self.password = my_password
        yagmail.register(self.username, self.password)
        return True


class Email:
    def __init__(self):
        self.subject = ''
        self.content = ''
        self.attachment = ''
        # self.mailbox = Mailbox()

    def create_email(self):
        self.subject = input("Write the subject of your e-mail:")
        self.content = input("And the message:")
        self.attachment = 'attachments/sheet1.xlsx'
        return True

    def send_email(self, my_username):
        recipients = ['helena.sokolowska.dev+recipient1@gmail.com', 'helena.sokolowska.dev+recipient2@gmail.com',
              'helena.a.sokolowska@gmail.com']
        yag = yagmail.SMTP(my_username)
        yag.send(recipients, self.subject, self.content, self.attachment)
        return True

# to nie działało dopóki nie wyłączyłam dwuetapowej weryfikacji oraz nie włączyłam dostępu mniej bezpiecznych aplikacji
# próbowałam korzystać z artykułu sugerowanego w wyświetlanym błędzie -
# https://support.google.com/mail/?p=BadCredentials ale to nie zadziałało


my_mailbox = Mailbox()
my_mailbox.register_mailbox('helena.sokolowska.dev')
my_email = Email()
my_email.create_email()
my_email.send_email(my_mailbox.username)

# and now getting the data from portal.futurecollars


def get_data():
    with open("token_2.txt", "r") as file:
        access_token = file.readline()
    request_url = 'https://api.portal.futurecollars.com/api/query/FutureCollars.Core.Contracts.Mentor.MentorTasks.Queries.MentorTasksHistory'
    response = requests.post(
        request_url,
        data={
            'DateCreatedFrom': "2022-02-19T00:00:00.000Z",
            'DateCreatedTo': "2022-03-19T23:59:59.999Z"
        },
        headers={
            'authorization': f'Bearer {access_token}'
            # 'authorization': access_token
        }
    )
    return response


# print(get_data())

