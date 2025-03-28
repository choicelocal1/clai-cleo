# ChatBot Application

A web-based chatbot application built with Python, Flask, and LangChain, integrated with the OpenAI API.

## Features

- User authentication system (register, login, logout)
- Chat functionality with OpenAI LLM integration through LangChain
- Dashboard for managing chat history
- Responsive design for desktop and mobile devices
- Real-time chat updates
- Automatic chat title generation
- Secure authentication with password hashing

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd chatbot-project
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy the `.env.example` file to `.env`
   - Update the `.env` file with your configuration values, especially:
     - `SECRET_KEY`: Generate a secure random key
     - `OPENAI_API_KEY`: Your OpenAI API key

5. Initialize the database:
   ```
   flask init-db
   ```

6. (Optional) Create an admin user:
   ```
   flask create-admin
   ```

## Running the Application

Start the application with:
```
python run.py
```

Visit `http://127.0.0.1:5000` in your web browser.

## Running Tests

To run the tests:
```
pytest
```

## Project Structure

```
chatbot-project/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── run.py                 # Application runner
├── auth/                  # Authentication module
├── chat/                  # Chat functionality
├── dashboard/             # Dashboard module
├── models/                # Database models
├── static/                # Static assets (CSS, JS)
├── templates/             # HTML templates
└── tests/                 # Test suite
```

## Development Guidelines

- Use Flask's built-in development server during development
- Update the requirements.txt when adding new dependencies
- Write tests for new features
- Follow PEP 8 style guidelines for Python code

## Deployment

For production deployment:

1. Set the `FLASK_ENV` environment variable to `production`
2. Configure a production-ready database (e.g., PostgreSQL)
3. Use a production WSGI server (e.g., Gunicorn)
4. Set up a reverse proxy (e.g., Nginx)
5. Consider using Docker for containerization

Example production setup with Gunicorn and Nginx:
```
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 "app:create_app('production')"
```

## License

[MIT License](LICENSE)

## Credits

- Flask - Web framework
- LangChain - Integration with language models
- OpenAI - Language model provider
- Bootstrap - Frontend framework
