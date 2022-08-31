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

    docker build -t energyclash .
    docker run -d -p 5000:5000 energyclash

Docker debugging:

    docker run -p 5000:5000 -it energyclash:<tag> bash
    
To run SQLite3 command on Windows:
1. Download sqlite-tools-win32-x86-3390200.zip from (https://www.sqlite.org/download.html). 1.88 MiB.
2. Assuming both the SQLite binary folder and the project repo are in the same parent folder:


    `..\sqlite-tools-win32-x86-3390200\sqlite3.exe database/energyclash.db < database/energyclash.sql`

Local URL: http://localhost:5000
