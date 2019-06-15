from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        # need to call BaseTest setUp method because setUP of ItemTest
        # is overriding it
        # call setup method of SUPER class, way in python
        # get super class super(ItemTest, self) and "." call method on it
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(401, response.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test',
                                      headers={'Authorization': self.access_token})
                self.assertEqual(404, response.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test',
                                      headers={'Authorization': self.access_token})
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 19.99},
                                     json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.delete('/item/test')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1} )
                self.assertEqual(201, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 19.99},
                                     json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1} )
                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "An item with name 'test' already exists."},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()

                response = client.put('/item/test',
                                      data={'price': 19.99, 'store_id': 1})
                self.assertEqual(200, response.status_code)
                self.assertEqual(19.99, ItemModel.find_by_name('test').price)
                self.assertDictEqual(
                    {'name': 'test', 'price': 19.99},
                    json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                ItemModel('test', 1.79, 1).save_to_db()

                self.assertEqual(1.79, ItemModel.find_by_name('test').price)

                response = client.put('/item/test',
                                      data={'price': 19.99, 'store_id': 1})
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(
                    {'name': 'test', 'price': 19.99},
                    json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.get('/items')
                self.assertDictEqual(
                    {'items': [{'name': 'test', 'price': 19.99}]},
                    json.loads(response.data))
