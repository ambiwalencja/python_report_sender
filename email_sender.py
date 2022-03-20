from classes import Mailbox, Email


my_mailbox = Mailbox()
my_mailbox.register_mailbox('helena.sokolowska.dev')
my_email = Email()
my_email.create_email()
my_email.send_email(my_mailbox.username)
