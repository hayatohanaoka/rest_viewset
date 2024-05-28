import requests

def login_user(email, password):
    login_url = 'http://127.0.0.1:8000/user/login_token/'
    res = requests.post(
        login_url, 
        data={
            'username': 'test_user',
            'email': email,
            'password': password
        }
    )
    res_json = res.json()
    return res_json['token']
