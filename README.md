Requirements:

- Any Python version between 3.6 & 3.9 inclusive.
- sqlite3
- tesseract binary


To run:

    python -m venv venv
    pip install -r requirements.txt
    sqlite3 database/energyclash.db < database/energyclash.sql
    python app.py

Docker steps:

    docker build -t energyclash:<tag> .
    docker run -d -p 5000:5000 energyclash:<tag>

- where `tag` is the version, eg `1.0`.

Docker debugging:

    docker run -p 5000:5000 -it energyclash:<tag> bash

Local URL: http://localhost:5000
