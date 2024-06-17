import json

from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth.models import User

from app.models import Column
# 変数の用意
USERNAME1 = 'testuser1'
USERNAME2 = 'testuser2'
PASSWORD = 'testpassword'

COLUMN_TITLE1 = 'title_1'
COLUMN_TITLE2 = 'title_2'
COLUMN_TITLE3 = 'title_3'
COLUMN_TITLE4 = 'title_4'
COLUMN_TITLE5 = 'title_5'
COLUMN_DESCRIPTION1 = 'description_1'
COLUMN_DESCRIPTION2 = 'description_2'
COLUMN_DESCRIPTION3 = 'description_3'
COLUMN_DESCRIPTION4 = 'description_4'
COLUMN_DESCRIPTION5 = 'description_5'

class ColumnTestCase(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1   = User.objects.create_user(username=USERNAME1, password=PASSWORD)
        cls.user2   = User.objects.create_user(username=USERNAME2, password=PASSWORD)
        cls.column1 = Column.objects.create(title=COLUMN_TITLE1, description=COLUMN_DESCRIPTION1, user=cls.user1)
        cls.column2 = Column.objects.create(title=COLUMN_TITLE2, description=COLUMN_DESCRIPTION2, user=cls.user1)
        cls.column3 = Column.objects.create(title=COLUMN_TITLE3, description=COLUMN_DESCRIPTION3, user=cls.user2)
        cls.column4 = Column.objects.create(title=COLUMN_TITLE4, description=COLUMN_DESCRIPTION4, user=cls.user2)

    def test_column_query(self):
        res = self.query(
            '''
            query MyQuery {
                columnQuery {
                    allColumns {
                        edges {
                            node {
                                title
                                description
                                user{
                                    username
                                }
                            }
                        }
                    }
                }
            }
            '''
        )
        col_data = json.loads(res.content)['data']['columnQuery']['allColumns']['edges']

        # 単体テストのチェック
        self.assertEqual(len(col_data), 3)
        expected_columns = [
            (COLUMN_TITLE1, COLUMN_DESCRIPTION1, USERNAME1),
            (COLUMN_TITLE2, COLUMN_DESCRIPTION2, USERNAME1),
            (COLUMN_TITLE3, COLUMN_DESCRIPTION3, USERNAME2),
            (COLUMN_TITLE4, COLUMN_DESCRIPTION4, USERNAME2)
        ]
        for i, col in enumerate(col_data):
            node = col['node']
            self.assertEqual(node['title'], expected_columns[i][0])
            self.assertEqual(node['description'], expected_columns[i][1])
            self.assertEqual(node['user']['username'], expected_columns[i][2])
    

    def test_column_by_title(self):
        res      = self._fetch_column_by_title(COLUMN_TITLE1)
        col_data = json.loads(res.content)['data']['columnQuery']['allColumns']['edges']
        node     = col_data[0]['node']
        self.assertEqual(len(col_data), 1)
        self.assertEqual(node['title'], COLUMN_TITLE1)
        self.assertEqual(node['description'], COLUMN_DESCRIPTION1)
        self.assertEqual(node['user']['username'], USERNAME1)
    
    def test_create_column_no_login(self):
        res = self.query(
            '''
            mutation MyMutation($title: String!, $description: String!) {
                createColumn(input: {title: $title, description: $description}) {
                    column {
                        title
                        description
                    }
                }
            }
            ''',
            variables={ 'title': COLUMN_TITLE5, 'description': COLUMN_DESCRIPTION5 }
        )
        self.assertIn('errors', json.loads(res.content))  # errors が res.content に入っているかどうか

    def login(self, username, password):
        res = self.client.post(
            '/api/token/',  # config.urls で指定したトークンログインURL
            {'username': username, 'password': password}
        )
        return json.loads(res.content)['access']  # JWTアクセストークンを返す


    def test_create_column_login(self):
        jwt_token = self.login(USERNAME1, PASSWORD)  # ログイン処理
        self.query( # 作成処理
            '''
            mutation MyMutation($title: String!, $description: String!){
                createColumn(input: {title: $title, description: $description}){
                    column {
                        title
                        description
                    }
                }
            }
            ''',
            variables={'title': COLUMN_TITLE5, 'description': COLUMN_DESCRIPTION5},
            headers={'AUTHORIZATION': f'Bearer {jwt_token}'}
        )

        # 作成データの照合
        res      = self._fetch_column_by_title(COLUMN_TITLE5)
        col_data = json.loads(res.content)['data']['columnQuery']['allColumns']['edges']
        node     = col_data[0]['node']
        self.assertEqual(node['title'], COLUMN_TITLE5)
        self.assertEqual(node['description'], COLUMN_DESCRIPTION5)
        self.assertEqual(node['user']['username'], USERNAME1)

    def _fetch_column_by_title(self, title):
        return self.query(
            '''
            query MyQuery($title: String!) {
                columnQuery {
                    allColumns(title: $title) {
                        edges {
                            node {
                                title
                                description
                                user {
                                    username
                                }
                            }
                        }
                    }
                }
            }
            ''',
            variables={'title': title}
        )