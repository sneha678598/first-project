import unittest
import pandas as pd
from src.idms_functions import clean_data, create_features

class TestDataProcessing(unittest.TestCase):

    def test_clean_data(self):
        # Example raw data with missing values
        raw_data = pd.DataFrame({
            'col1': [1, 2, None],
            'col2': [4, None, 6]
        })
        
        # Process raw data
        processed_data = clean_data(raw_data)
        
        # Check if missing values are removed
        self.assertEqual(processed_data.isnull().sum().sum(), 0, "There should be no missing values after cleaning.")

    def test_create_features(self):
        # Example raw data for feature creation
        raw_data = pd.DataFrame({
            'existing_feature': [1, 2, 3]
        })
        
        # Create new features
        processed_data = create_features(raw_data)
        
        # Check if the new feature is created correctly
        self.assertTrue('new_feature' in processed_data.columns, "The new feature should be created.")
        self.assertTrue(all(processed_data['new_feature'] == raw_data['existing_feature'] * 2), "The new feature values are incorrect.")

if __name__ == '__main__':
    unittest.main()
