from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('bob', 'bobpassword')

        self.assertEqual(user.username, 'bob')
        self.assertEqual(user.password, 'bobpassword')