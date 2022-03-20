import yagmail
import keyring


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
