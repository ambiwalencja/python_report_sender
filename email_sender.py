from classes import Mailbox, Email


my_mailbox = Mailbox()
my_mailbox.register_mailbox('helena.sokolowska.dev')
my_email = Email()
recipients = {
    "Master Admin": 'helena.sokolowska.dev+recipient1@gmail.com',
    "None": 'helena.sokolowska.dev+recipient2@gmail.com'
}
for recipient in recipients:
    my_email.create_email(recipient)
    my_email.send_email(my_mailbox.username, recipients[recipient])
