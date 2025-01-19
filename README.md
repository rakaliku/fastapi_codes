# FastAPI Project

Welcome to my **first ever FastAPI Python project**! This project is a demonstration of building APIs using FastAPI, a modern web framework for Python that is high-performance and easy to use.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Project Structure](#project-structure)
7. [Technologies Used](#technologies-used)
8. [Contributing](#contributing)
9. [License](#license)

---

## Overview

This project is a simple API that manages a collection of heroes, including their details such as name, age, and a secret identity. It demonstrates the use of:

- **CRUD operations** (Create, Read, Update, Delete)
- **Database integration** using `SQLModel` (an ORM)
- **Dependency injection**
- **Form data handling**

---

## Features

- Add heroes with relevant details.
- Retrieve a list of heroes with pagination.
- Get a specific hero by ID.
- Delete heroes by ID.
- Built-in SQLite database support.
- Scalable and ready for further enhancements.

---

## Installation

To set up and run this project locally, follow these steps:

### Prerequisites

- **Python 3.9+** installed on your system.
- **Git** installed.

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API:**
   Open your browser or API client (e.g., Postman) and go to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Usage

Once the server is running, you can interact with the API using the following endpoints:

### Base URL
```
http://127.0.0.1:8000
```

---

## API Endpoints

### 1. **Create a Hero**
   **POST** `/heroes/`
   
   **Request Body:**
   ```json
   {
       "name": "Superman",
       "age": 35,
       "secret_name": "Clark Kent"
   }
   ```
   
   **Response:**
   ```json
   {
       "id": 1,
       "name": "Superman",
       "age": 35,
       "secret_name": "Clark Kent"
   }
   ```

### 2. **Retrieve All Heroes**
   **GET** `/heroes/?offset=0&limit=10`
   
   **Response:**
   ```json
   [
       {
           "id": 1,
           "name": "Superman",
           "age": 35,
           "secret_name": "Clark Kent"
       }
   ]
   ```

### 3. **Retrieve a Hero by ID**
   **GET** `/heroes/{hero_id}`
   
   **Response:**
   ```json
   {
       "id": 1,
       "name": "Superman",
       "age": 35,
       "secret_name": "Clark Kent"
   }
   ```

### 4. **Delete a Hero by ID**
   **DELETE** `/heroes/{hero_id}`
   
   **Response:**
   ```json
   {
       "ok": true
   }
   ```

---

## Project Structure

```
project-folder/
├── main.py              # Main FastAPI application file
├── database.db          # SQLite database file (auto-created)
├── requirements.txt     # Dependencies file
├── venv/                # Virtual environment folder
└── .gitignore           # Ignored files and folders
```

---

## Technologies Used

- **Python** (3.9+)
- **FastAPI**
- **SQLModel**
- **SQLite**
- **Uvicorn** (for ASGI server)

---

## Contributing

Contributions are welcome! If you'd like to contribute to this project:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

