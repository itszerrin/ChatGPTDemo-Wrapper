# Description: Default headers for all requests

def get_default_headers(user_agent, content_length: int):

    return {
        'authority': 'chat.chatgptdemo.net',
        'method': 'POST',
        'url': '/new_chat',
        'protocol': 'HTTP/3',
        'Host': 'chat.chatgptdemo.net',
        'User-Agent': f'{user_agent}',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Content-Length': f'{content_length}',
        'Origin': 'https://chat.chatgptdemo.net',
        'Alt-Used': 'chat.chatgptdemo.net',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
}

# Path: assets/scripts/headers/default_headers.py