import unittest
import pandas as pd
import api  

class TestAPI(unittest.TestCase):

    def test_get_age_category(self):
        # Test case 1: Age within the 'child' category
        data1 = pd.DataFrame({'age': [10]})
        expected1 = pd.DataFrame({'age': [10], 'age_category': ['child']})
        self.assertTrue(api.get_age_category(data1).equals(expected1))

        # Test case 2: Age within the 'adult' category
        data2 = pd.DataFrame({'age': [40]})
        expected2 = pd.DataFrame({'age': [40], 'age_category': ['adult']})
        self.assertTrue(api.get_age_category(data2).equals(expected2))

        # Test case 3: Age within the 'elderly' category
        data3 = pd.DataFrame({'age': [80]})
        expected3 = pd.DataFrame({'age': [80], 'age_category': ['elderly']})
        self.assertTrue(api.get_age_category(data3).equals(expected3))

    def test_calculate_family_fare(self):
        data = pd.DataFrame({
            'fare': [100, 50, 80],
            'family_size': [3, 1, 2]
        })
        expected = pd.DataFrame({
            'fare': [100, 50, 80],
            'family_size': [3, 1, 2],
            'fare_per_family_member': [25, 50, 26.666666666666668]
        })
        self.assertTrue(api.calculate_family_fare(data).equals(expected))

    def test_data_transformation(self):
        data = pd.DataFrame({
            'age': [10, 25, 45],
            'fare': [100, 50, 80],
            'family_size': [3, 1, 2],
            'gender': ['male', 'female', 'female'],
            'embarked_from': ['cherbourg', 'southampton', 'cherbourg']
        })
        # Mocking the load_file function to return identity transformers for testing
        api.config.SCALER_PATH = 'path/to/scaler.pkl'
        api.config.ONEHOT_PATH = 'path/to/onehot.pkl'

        # Assume the scaler and one-hot encoder used for training apply no transformation (identity transformers)
        def identity_transform(data):
            return data

        api.load_file = lambda path: identity_transform

        # Test the data_transformation function with identity transformers
        transformed_data = api.data_transformation(data)
        self.assertTrue(transformed_data.equals(data))  # The transformed data should be the same as the original data

if __name__ == "__main__":
    unittest.main()
