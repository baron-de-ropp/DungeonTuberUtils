from app import create_app
import os

app = create_app()

print("Template Directory:", os.path.join(os.path.dirname(__file__), 'templates'))

if __name__ == "__main__":
    app.run(debug=True)
