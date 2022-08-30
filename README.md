Requirements:

- Any Python version between 3.6 & 3.9 inclusive.


To run:

    python -m venv venv
    pip install -r requirements.txt
    python app.py

Docker steps:

```sh
docker build -t energyclash:1.0 .
docker run -d -p 5000:5000 energyclash:1.0
```

Local URL: http://localhost:5000
