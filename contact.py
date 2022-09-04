import sys
from urllib import parse


def get_template():
    with open('template.html', 'r') as file:
        contents = file.read()
    return contents


def span(in_text):
    return '<span style="font-family:courier;font-size:14px">' + in_text + '</span>'


data = sys.argv

full_message = data[1]
full_message = full_message.lstrip('[').rstrip(']')
full_message = parse.unquote_plus(full_message)
params = {x[0]: x[1] for x in [x.split("=") for x in full_message.split("&")]}

if __name__ == '__main__':
    response = get_template()
    response = response.replace('#header#', 'Contact')
    response = response.replace('#body#', span('<b>Information received</b><br>Name: ' + params['name'] + '<br>Email: ' + params['email'] + '<br>Subject: ' + params['subject'] + '<br>Message: ' + params['message']))
    response = response.replace('#footer#', '&nbsp;')
    print(response)
