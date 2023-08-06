import requests

def main():
    print('Sending request...')
    response = requests.post('http://127.0.0.1:3000', data={'message': 'hi'})
    print(response.text)

if __name__ == '__main__':
    main()
