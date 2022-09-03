import sys
import urllib.parse

data = sys.argv

full_message = urllib.parse.unquote(data[1])
full_message = urllib.parse.unquote_plus(full_message)
full_message = full_message.lstrip('[')
full_message = full_message.rstrip(']')

parsed = full_message.split('&')
parsed_subject = parsed[0].split('=')
parsed_message = parsed[1].split('=')

subject = parsed_subject[1]
message = parsed_message[1]


if __name__ == '__main__':
    print('<html><body bgcolor="#808080"><center><table cellspacing="0"><tr height="32">')
    print('<td bgcolor="#202020"><center><font face="courier" size="-1" color="#ffffff">Contact</font></center></td></tr>')
    print('<tr><td bgcolor="#ffffff"><center><font face="courier" size="-1">Information received<br>Subject: ' + subject + '<br>Message: ' + message + '</font></center></td></tr>')
    print('<tr height="32"><td bgcolor="#202020"><font face="courier" size="-1">&nbsp;</font></td></tr></table></center></body></html>')
