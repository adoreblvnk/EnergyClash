DROP TABLE IF EXISTS login;

CREATE TABLE login(
    user TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

INSERT INTO login (user, password)
VALUES
    ("user", "password123"),
    ("youseff", "str0ngPass");
