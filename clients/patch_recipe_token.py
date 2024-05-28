import requests

from login_user_client import login_user

token = login_user(email='aaa@aaa.aaa', password='123345678')
print(token)

res = requests.patch(
    'http://127.0.0.1:8000/recipe/recipe/1/',
    data={
        'title': 'test_patch',
        'instruction': 'クライアントテスト パッチ',
    },
    headers={
        'Authorization': f'Token {token}'
    }
)

print(res.status_code)
print(res.json())
