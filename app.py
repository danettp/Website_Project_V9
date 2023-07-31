"""This script runs a Flask application in debug mode."""

from website import create_app

if __name__ == "__main__":
    app = create_app()  # Create a Flask app with the create_app function
    app.run(debug=True)  # Run the app in debug mode
