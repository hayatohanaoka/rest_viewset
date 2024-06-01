import random
import requests

import graphene

class Address(graphene.ObjectType):
    city = graphene.String()
    is_primary_address = graphene.Boolean(default_value=True)
    latitude = graphene.Float(description='住所の緯度')
    longitude = graphene.Float(description='住所の経度')


class User(graphene.ObjectType):
    user_id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    address = graphene.Field(Address)


class UserType(graphene.ObjectType):
    name = graphene.String(description="名前")
    age = graphene.Int(description="年齢")
    address = graphene.Field(Address)
    addresses = graphene.List(Address)

    def resolve_name(root, info):
        names = ['Bob', 'Alice', 'Charlie']
        return random.choice(names)
    
    def resolve_age(root, info):
        return 30
    
    def resolve_address(root, info):
        user_address = {'city': 'example_city'}
        return Address(**user_address)
    
    def resolve_addresses(root, info):
        user_addresses = [
            {'city': 'example_city'},
            {'city': 'example_city2', 'latitude': 219},
        ]
        return [
            Address(**user_address) for user_address in user_addresses
        ]


class UserAPIType(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())
    user_list = graphene.List(User)

    def resolve_user(root, info, **kwarg):
        search_id = kwarg['id']
        res = requests.get(f'https://jsonplaceholder.typicode.com/users/{search_id}')
        res.raise_for_status()
        user = res.json()

        return User(
            user_id=user['id'],
            name=user['name'],
            email=user['email'],
            address=Address(
                city=user['address']['city'],
                latitude=user['address']['geo']['lat'],
                longitude=user['address']['geo']['lng']
            )
        )
    
    def resolve_user_list(root, info):
        res = requests.get(f'https://jsonplaceholder.typicode.com/users')
        users = res.json()
        
        res_users = []
        for user in users:
            res_users.append(
                User(
                    user_id=user['id'],
                    name=user['name'],
                    email=user['email'],
                    address=Address(
                        city=user['address']['city'],
                        latitude=user['address']['geo']['lat'],
                        longitude=user['address']['geo']['lng']
                    )
                )
            )
        print(res_users)
        return res_users


class Query(graphene.ObjectType):
    user_query = graphene.Field(UserType)
    user_api_query = graphene.Field(UserAPIType)

    def resolve_user_query(parent, info):
        return UserType()
    
    def resolve_user_api_query(parent, info):
        return UserAPIType()


schema = graphene.Schema(query=Query)
