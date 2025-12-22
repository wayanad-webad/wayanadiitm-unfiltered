# Anonymous Feedback App

A production-ready anonymous feedback application built with Flask, MongoDB, Vue 3, and Tailwind CSS.

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (running on `mongodb://localhost:27017` by default)

## Setup

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file (example provided in `.env`):
    ```env
    SECRET_KEY=your_secret_key
    MONGO_URI=mongodb://localhost:27017/hushup_db
    JWT_SECRET_KEY=your_jwt_secret_key
    ```
5.  Create an admin user:
    ```bash
    python create_admin.py <username> <password>
    # Example: python create_admin.py admin password123
    ```
6.  Run the server:
    ```bash
    python app.py
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## Usage

1.  **Public User**: Go to the homepage (e.g., `http://localhost:5173`) to submit feedback anonymously.
2.  **Admin**: Go to `/admin/login` (e.g., `http://localhost:5173/admin/login`) to log in and view/moderate feedbacks.

