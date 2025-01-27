"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db, app
from models.account import Account, DataValidationError
import datetime

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)
    
    def test_repr(self):
        """Test the representation of an account"""
        account = Account()
        account.name = "Foo"
        self.assertEqual(str(account), "<Account 'Foo'>")

    def test_to_dict(self):
        """ Test account to dict """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
        self.assertEqual(account.date_joined, result["date_joined"])
    
    def test_from_dict(self):
        """ Test creating an Account from a dictionary """
        data = ACCOUNT_DATA[self.rand]  # Get a random account data dictionary
        original_account = Account(**data)  # Create an Account object from the data

        # Convert the Account object back to a dictionary using from_dict
        new_account = Account()
        new_account.from_dict(original_account.to_dict())

        # Check if the attributes of the original and new accounts match
        self.assertEqual(original_account.name, new_account.name)
        self.assertEqual(original_account.email, new_account.email)
        self.assertEqual(original_account.phone_number, new_account.phone_number)
        self.assertEqual(original_account.disabled, new_account.disabled)
        self.assertEqual(original_account.date_joined, new_account.date_joined)

    def test_update(self):
        """ Test for updating an account in the database"""
        data = ACCOUNT_DATA[self.rand]  # Get a random account data dictionary
        account = Account(**data)  # Create an Account object from the data

        # Create the account in the database
        account.create()

        # Modify some attributes of the account
        updated_name = "Updated Name"
        updated_email = "updated@example.com"
        account.name = updated_name
        account.email = updated_email

        # Call the update method to save the changes
        account.update()

        # Retrieve the updated account from the database
        updated_account = Account.find(account.id)

        # Check if the attributes have been updated correctly
        self.assertEqual(updated_account.name, updated_name)
        self.assertEqual(updated_account.email, updated_email)

        # Attempt to call the update method without setting the ID
        account_without_id = Account(**data)

        with self.assertRaises(DataValidationError) as context:
            account_without_id.update()

        # Check if the correct exception was raised
        self.assertEqual(
            str(context.exception),
            "Update called with empty ID field"
        )


    def test_delete(self):
        """ Test deleting an existing Account """
        data = ACCOUNT_DATA[self.rand]  # Get a random account data dictionary
        account = Account(**data)  # Create an Account object from the data

        # Create the account in the database
        account.create()

        # Call the delete method to remove the account
        account.delete()

        # Attempt to retrieve the deleted account from the database
        deleted_account = Account.find(account.id)

        # Check if the retrieved account is None, indicating successful deletion
        self.assertIsNone(deleted_account)
        

