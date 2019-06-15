from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():

                # data is sent as formdata so no need to json convers
                request = client.post('/register',
                                      data={'username': 'test',
                                            'password': '11111'})
                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User was created successfully'},
                                     json.loads(request.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                            data={
                                'username': 'test',
                                'password': '11111'
                            })
                # json.dumps Serialize obj to a JSON formatted
                auth_response = client.post('/auth',
                                            data=json.dumps({
                                               'username': 'test',
                                               'password': '11111'
                                            }),
                                            headers={
                                                'Content-Type':
                                                    'application/json'
                                            })
                # checking returned access token
                self.assertIn('access_token',
                              json.loads(auth_response.data).keys()) # ['access token ']

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register',
                            data={
                                'username': 'test',
                                'password': '11111'
                            })
                response = client.post('/register',
                                       data={
                                           'username': 'test',
                                           'password': '11111'
                                       })

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exist'},
                                     json.loads(response.data))