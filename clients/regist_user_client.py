import requests

regist_url = 'http://127.0.0.1:8000/user/regist/'

res = requests.post(regist_url, data={
    'username': 'test_user',
    'password': '123345678',
    'confirm_password': '123345678',
    'age': '18',
    'email': 'aaa@aaa.aaa',
})

print(res.status_code)
print(res)
