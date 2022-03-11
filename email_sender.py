import yagmail
import keyring

# username = input("Please write your username:")
username = 'helena.sokolowska.dev'
password = input(f'Please write the password for user {username}:')

yagmail.register(username, password)

yag = yagmail.SMTP(username)
subject = input("And now subject of your e-mail:")
contents = input("And the message:")
attachment = 'attachments/sheet1.xlsx'
# attachment = 'sheet1.xlsx'
recipients = ['helena.sokolowska.dev+recipient1@gmail.com', 'helena.sokolowska.dev+recipient2@gmail.com',
              'helena.a.sokolowska@gmail.com']
yag.send(recipients, subject, contents, attachment)

# to nie działało dopóki nie wyłączyłam dwuetapowej weryfikacji oraz nie włączyłam dostępu mniej bezpiecznych aplikacji
# próbowałam korzystać z artykułu sugerowanego w wyświetlanym błędzie -
# https://support.google.com/mail/?p=BadCredentials ale to nie zadziałało



