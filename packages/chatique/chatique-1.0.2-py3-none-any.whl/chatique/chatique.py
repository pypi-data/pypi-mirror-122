import requests
import coolname

ADDRESS = "http://82.148.30.33:7878/"
NAME = "-".join(coolname.generate_slug().split("-")[:2])


def change_name(new_name):
    global NAME
    NAME = new_name
    print(f"Nickname changed")


def send(message, name=None):
    '''send the message to the chat'''
    if name is None:
        name = NAME
    requests.post(f"{ADDRESS}", data=f"msg~~~{message}|name~~~{name}".encode('utf-8'))


def get(top=10):
    '''get top n messages from the chat'''
    resp = requests.post(f"{ADDRESS}", data=f"top~~~{top}".encode('utf-8'))
    print(resp.content.decode('utf-8'))
