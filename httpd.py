import socket
import os
import grp
import pwd
import sys
import random
from multiprocessing import Process
from datetime import date
import time


def plural(num, tag):
    if tag == 'directory':
        if num == 1:
            return '1 directory'
        else:
            return str(num) + ' directories'
    else:
        if num == 1:
            return '1 file'
        else:
            return str(num) + ' files'


def dir_unix(path):
    if os.path.isdir(path):
        return 'd'
    else:
        return '-'


def get_unix(perm):
    if perm == '0':
        out = '---'
    elif perm == '1':
        out = '--x'
    elif perm == '2':
        out = '-w-'
    elif perm == '3':
        out = '-wx'
    elif perm == '4':
        out = 'r--'
    elif perm == '5':
        out = 'r-x'
    elif perm == '6':
        out = 'rw-'
    elif perm == '7':
        out = 'rwx'
    else:
        out = '???'
    return out

def cat_unix(perm):
    out = get_unix(perm[0]) + get_unix(perm[1]) + get_unix(perm[2])
    return out


def get_icon(file):
    out = '<img src="/images/file.png">'
    if os.path.isdir(file):
        out = '<img src="/images/folder.png">'
    else:
        if file.endswith('.wav'):
            out = '<img src="/images/wav.png">'
        elif file.endswith('.mp3'):
            out = '<img src="/images/wav.png">'
        elif file.endswith('.txt'):
            out = '<img src="/images/txt.png">'
        elif file.endswith('.py'):
            out = '<img src="/images/py.png">'
        elif file.endswith('.png'):
            out = '<img src="/images/image.png">'
        elif file.endswith('.jpg'):
            out = '<img src="/images/image.png">'
        elif file.endswith('.bmp'):
            out = '<img src="/images/image.png">'
        elif file.endswith('.gif'):
            out = '<img src="/images/image.png">'
        elif file.endswith('.webp'):
            out = '<img src="/images/image.png">'
        elif file.endswith('.xml'):
            out = '<img src="/images/xml.png">'
        elif file.endswith('.csv'):
            out = '<img src="/images/sql.png">'
        elif file.endswith('.sql'):
            out = '<img src="/images/sql.png">'
        elif file.endswith('.htm'):
            out = '<img src="/images/html.png">'
        elif file.endswith('.html'):
            out = '<img src="/images/html.png">'
        elif file.endswith('.mov'):
            out = '<img src="/images/mov.png">'
        else:
            out = '<img src="/images/file.png">'
    return out


def change_size(in_int):
    if in_int > 1024:
        if in_int > 1024000:
            out_size = str("{:.2f}".format(in_int / 1024000)) + ' Mb'
        else:
            out_size = str("{:.2f}".format(in_int / 1024)) + ' Kb'
    else:
        out_size = str(in_int) + ' bytes'
    return out_size


def zpad(in_str, pad=2):
    if len(in_str) < pad:
        out_str = in_str
        for i in range(len(in_str), pad):
            out_str = '0' + out_str
        return out_str
    else:
        return in_str


def log_request(request):
    datet = date.today()
    with open('httpd_' + str(datet.year) + zpad(str(datet.month)) + zpad(str(datet.day)) + '.log', 'a') as f:
        f.write(request)


def handle_request(connection):
    request = connection.recv(1024).decode('utf-8')
    log_request(request)
    string_list = request.split(' ')  # Split request from spaces

    method = string_list[0]
    requesting_file = string_list[1]

    print('Client request ', requesting_file)

    myfile = requesting_file.split('?')[0]  # After the "?" symbol not relevent here
    myfile = myfile.lstrip('/')
    response = ''
    bgDark = False
    file_count = 0
    dir_count = 0
    if (myfile == ''):
        # myfile = 'index.html'  # Load index file as default
        if not os.path.isdir(myfile):
            pass
        else:
            response = '<html><body bgcolor="#808080"><center><table cellspacing="0"><tr height="32"><td colspan="6" bgcolor="#202020"><center><font face="courier" size="-1" color="#ffffff">Index of /</font></center></td></tr>'
            files = os.listdir('.')
            files.sort()
            for x in files:
                status = os.stat(x)
                uid = status.st_uid
                gid = status.st_gid
                bgDark = not bgDark
                if os.path.isdir(x):
                    dir_count += 1
                else:
                    file_count += 1
                if bgDark:
                    response += '<tr><td bgcolor="#efefef"><a href="' + x + '">' + get_icon(x) + '</a></td><td bgcolor="#efefef"><a href="' + x + '"><font face="courier" size="-1">' + x + '</a>&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" color="#808080" size="-1">' + pwd.getpwuid(uid)[0] + '.' + grp.getgrgid(gid)[0] + '&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" color="#808080" size="-1">' + dir_unix(x) + cat_unix(str(oct(status.st_mode)[-3:])) + '&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" size="-1">' + change_size(os.path.getsize(x)) + '&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" color="#808080" size="-1">' + str(time.ctime(os.path.getmtime(x))) + '</font></td></tr>'
                else:
                    response += '<tr><td bgcolor="#ffffff"><a href="' + x + '">' + get_icon(x) + '</a></td><td bgcolor="#ffffff"><a href="' + x + '"><font face="courier" size="-1">' + x + '</a>&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" color="#808080" size="-1">' + pwd.getpwuid(uid)[0] + '.' + grp.getgrgid(gid)[0] + '&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" color="#808080" size="-1">' + dir_unix(x) + cat_unix(str(oct(status.st_mode)[-3:])) + '&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" size="-1">' + change_size(os.path.getsize(x)) + '&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" color="#808080" size="-1">' + str(time.ctime(os.path.getmtime(x))) + '</font></td></tr>'
            response += '<tr height="32"><td colspan="6" bgcolor="#202020"><center><font face="courier" color="#ffffff" size="-1">' + plural(file_count, 'file') + ', ' + plural(dir_count, 'directory') + '</font></center></td></tr></table></center></body></html>'
    else:
        if not os.path.isdir(myfile):
            pass
        else:
            response = '<html><body bgcolor="#808080"><center><table cellspacing="0"><tr height="32"><td colspan="6" bgcolor="#202020"><center><font face="courier" size="-1" color="#ffffff">Index of /' + myfile + '</font></center></td></tr>'
            files = os.listdir(myfile)
            files.sort()
            print(myfile)
            up_dir = myfile.rfind('/')
            if up_dir == -1:
                dir_link = '/'
            else:
                dir_link = '/' + myfile[0:up_dir]
            response += '<tr><td bgcolor="#ffffff"><a href="' + dir_link + '"><img src="/images/folder.png"></a></td><td colspan="5" bgcolor="#ffffff"><a href="' + dir_link + '">..</a></td></tr>'
            for x in files:
                status = os.stat(myfile + '/' + x)
                uid = status.st_uid
                gid = status.st_gid
                bgDark = not bgDark
                if os.path.isdir(myfile + '/' + x):
                    dir_count += 1
                else:
                    file_count += 1
                if bgDark:
                    response += '<tr><td bgcolor="#efefef"><a href="/' + myfile + '/' + x + '">' + get_icon(myfile + '/' + x) + '</a></td><td bgcolor="#efefef"><a href="/' + myfile + '/' + x + '"><font face="courier" size="-1">' + x + '</a>&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" color="#808080" size="-1">' + pwd.getpwuid(uid)[0] + '.' + grp.getgrgid(gid)[0] + '&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" color="#808080" size="-1">' + dir_unix(myfile + '/' + x) + cat_unix(str(oct(status.st_mode)[-3:])) + '&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" size="-1">' + change_size(os.path.getsize(myfile + '/' + x)) + '&nbsp;&nbsp;</font></td><td bgcolor="#efefef"><font face="courier" color="#808080" size="-1">' + str(time.ctime(os.path.getmtime(myfile + '/' + x))) + '</font></td></tr>'
                else:
                    response += '<tr><td bgcolor="#ffffff"><a href="/' + myfile + '/' + x + '">' + get_icon(myfile + '/' + x) + '</a></td><td bgcolor="#ffffff"><a href="/' + myfile + '/' + x + '"><font face="courier" size="-1">' + x + '</a>&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" color="#808080" size="-1">' + pwd.getpwuid(uid)[0] + '.' + grp.getgrgid(gid)[0] + '&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" color="#808080" size="-1">' + dir_unix(myfile + '/' + x) + cat_unix(str(oct(status.st_mode)[-3:])) + '&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" size="-1">' + change_size(os.path.getsize(myfile + '/' + x)) + '&nbsp;&nbsp;</font></td><td bgcolor="#ffffff"><font face="courier" color="#808080" size="-1">' + str(time.ctime(os.path.getmtime(myfile + '/' + x))) + '</font></td></tr>'
            response += '<tr height="32"><td colspan="6" bgcolor="#202020"><center><font face="courier" color="#ffffff" size="-1">' + plural(file_count, 'file') + ', ' + plural(dir_count, 'directory') + '</font></center></td></tr></table></center></body></html>'
    try:
        if response == '':
            file = open(myfile, 'rb')  # open file , r => read , b => byte format
            response = file.read()
            file.close()

        header = 'HTTP/1.1 200 OK\n'

        if myfile.endswith(".jpg"):
            mimetype = 'image/jpg'
        elif myfile.endswith('.png'):
            mimetype = 'image/png'
        elif myfile.endswith('.gif'):
            mimetype = 'image/gif'
        elif myfile.endswith(".css"):
            mimetype = 'text/css'
        elif myfile.endswith(".py"):
            mimetype = 'text/plain'
        elif myfile.endswith(".txt"):
            mimetype = 'text/plain'
        elif myfile.endswith(".log"):
            mimetype = 'text/plain'
        elif myfile.endswith(".xml"):
            mimetype = 'application/xml'
        elif myfile.endswith(".mp3"):
            mimetype = 'audio/x-mp3'
        elif myfile.endswith(".wav"):
            mimetype = 'audio/x-wav'
        elif myfile.endswith(".csv"):
            mimetype = 'text/csv'
        elif myfile.endswith(".mov"):
            mimetype = 'video/quicktime'
        elif myfile.endswith(".html"):
            mimetype = 'text/html'
        elif myfile.endswith(".htm"):
            mimetype = 'text/html'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404<br>not found</h3></center></body></html>'

    if response != '':
        if type(response) != bytes:
            response = response.encode('utf-8')
    final_response = header.encode('utf-8')
    if response != '':
        final_response += response
    connection.send(final_response)
    connection.close()
    sys.exit(0)


if __name__ == '__main__':
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect(('8.8.8.8', 53))
    HOST = my_socket.getsockname()[0]
    PORT = 8000
    my_socket.close()
    my_socket = None
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.bind((HOST, PORT))
    my_socket.listen(1)

    print('Serving on ' + HOST + ':', PORT)

    while True:
        connection, address = my_socket.accept()
        p = Process(target=handle_request, args=(connection,))
        p.start()
