import sys
from urllib import parse
import smtplib
from email.message import EmailMessage


def get_template():
    with open('template.html', 'r') as file:
        contents = file.read()
    return contents


def span(in_text):
    return '<span style="font-family:courier;font-size:14px">' + in_text + '</span>'


def send_mail(to_email, subject, message, server, from_email, user, password):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    msg.set_content(message)
    server = smtplib.SMTP(server)
    server.set_debuglevel(1)
    server.login(user, password)  # user & password
    server.send_message(msg)
    server.quit()


data = sys.argv

full_message = data[1]
full_message = full_message.lstrip('[').rstrip(']')
full_message = parse.unquote_plus(full_message)
params = {x[0]: x[1] for x in [x.split("=") for x in full_message.split("&")]}

if __name__ == '__main__':
    # send_mail(to_email=['your_email@gmail.com', 'some_other@gmail.com'], subject=params['subject'], message=params['message'], server='smtp.gmail.com', from_email=params['email'], user='user@some.com', password='password')
    response = get_template()
    response = response.replace('#header#', 'Contact')
    response = response.replace('#body#', span('<b>Information received</b><br>Name: ' + params['name'] + '<br>Email: ' + params['email'] + '<br>Subject: ' + params['subject'] + '<br>Message: ' + params['message']))
    response = response.replace('#footer#', span('<a href="/">&lt;-Back</a>'))
    print(response)
