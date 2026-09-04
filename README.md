# EDTL

## Description
EDTL is a web-based application built using the Django (Python) framework. This application is designed to facilitate data management and visualization, providing a responsive and user-friendly interface.

*(Note: You can further customize this description according to the specific goals of the EDTL project)*

## Key Features
- Integrated data management
- Responsive user interface with a modern template
- Integration with various external services (including AI/Gemini features)
- Authentication and authorization system

## Prerequisites
Ensure your system has the following installed:
- Python 3.8 or newer
- pip (Python package installer)

## Local Setup & Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Akara96/EDTL.git
   cd EDTL
   ```

2. **Create and activate a virtual environment (optional but highly recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. Access the application via your web browser at `http://127.0.0.1:8000/`.

## Technologies Used
- Python
- Django
- SQLite (Default database)
- HTML, CSS, JavaScript (Bootstrap / AdminLTE)
- Docker (Docker support included)
