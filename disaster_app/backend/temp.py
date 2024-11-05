import joblib

def load_model(model_path):
    """Load a trained machine learning model from a specified path."""
    model = joblib.load(model_path)
    return model

# Example usage
if __name__ == "__main__":
    model_path = 'Data/models/pipeline.pkl'  # Replace with your model's path
    model = load_model(model_path)

    # Print model summary
    print(model)
