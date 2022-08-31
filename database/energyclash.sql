DROP TABLE IF EXISTS login;

CREATE TABLE login(
    user TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    district TEXT NOT NULL
);

INSERT INTO login (user, password, district)
VALUES
    ("user", "password123", "YISHUN"),
    ("youseff", "str0ngPass", "BEDOK");
