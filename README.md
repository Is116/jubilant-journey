# Facial Recognition Attendance System

## Setup Instructions

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Download the required models for dlib and place them in `app/models/`.

3. Create the database:
    ```python
    from app.database import create_database
    create_database()
    ```

4. Run the application:
    ```
    python main.py
    ```

5. Open your browser and go to `http://127.0.0.1:5000` to see the attendance records.

## File Structure

