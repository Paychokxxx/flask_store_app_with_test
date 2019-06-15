from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.items.all(), [], 'Store items length is not 0')

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_model', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_model')

    def test_store_json(self):
        store = StoreModel('test store')
        expected = {
            'name': 'test store',
            'items': []
        }

        self.assertDictEqual(store.json(), expected)

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test store',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected)