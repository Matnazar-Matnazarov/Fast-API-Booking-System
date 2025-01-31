# FastAPI Project

![FastAPI](https://upload.wikimedia.org/wikipedia/commons/1/1a/FastAPI_logo.svg)

## Overview

This project is a simple FastAPI application that demonstrates the use of middleware, caching, and exception handling.

## Features

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Middleware**: Custom middleware to add processing time headers.
- **Caching**: Redis and in-memory caching for improved performance.
- **Exception Handling**: Custom exception handlers for better error management.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/fastapi-project.git
    cd fastapi-project
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000` to see the application in action.

## API Endpoints

- `GET /`: Returns a welcome message.
- `GET /hello/{name}`: Returns a personalized greeting with caching.
- `POST /clear-cache`: Clears the cache.

## Example Usage

### Get Welcome Message

```http
GET http://127.0.0.1:8000/
Accept: application/json
```

### Say Hello

```http
GET http://127.0.0.1:8000/hello/YourName
Accept: application/json
```

### Clear Cache

```http
POST http://127.0.0.1:8000/clear-cache
Accept: application/json
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) 
- [Redis](https://redis.io/)

