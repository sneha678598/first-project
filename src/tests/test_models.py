import unittest
from src.idms_functions import load_model, predict

class TestModels(unittest.TestCase):

    def test_load_model(self):
        model = load_model("example_model.pkl")
        self.assertIsNotNone(model)
    
    def test_predict(self):
        model = load_model("example_model.pkl")
        sample_data = {...}  # Example input data
        prediction = predict(model, sample_data)
        
        self.assertIn(prediction, ["expected_output1", "expected_output2"])
        # Add more assertions based on model output

if __name__ == '__main__':
    unittest.main()
