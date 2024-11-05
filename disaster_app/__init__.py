from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Import routes at the end to avoid circular imports
from .backend import routes  # Adjusted import statement


