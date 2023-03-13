CREATE TABLE Letter
(
  letter_id INTEGER PRIMARY KEY AUTOINCREMENT,
  unicode CHAR NOT NULL,
  UNIQUE (unicode)
);

CREATE TABLE WordCore
(
  word_id INTEGER PRIMARY KEY AUTOINCREMENT,
  word VARCHAR NOT NULL,
  length INT NOT NULL,
  last_letter_id INTEGER,
  FOREIGN KEY (last_letter_id) REFERENCES Letter(letter_id),
  UNIQUE (word)
);

CREATE TABLE Contains
(
  word_id INTEGER NOT NULL,
  letter_id INTEGER NOT NULL,
  FOREIGN KEY (word_id) REFERENCES WordCore(word_id),
  FOREIGN KEY (letter_id) REFERENCES Letter(letter_id)
);

CREATE TABLE GoesAfter
(
  letter_before_id INTEGER NOT NULL,
  letter_after_id INTEGER NOT NULL,
  FOREIGN KEY (letter_before_id) REFERENCES Letter(letter_id),
  FOREIGN KEY (letter_after_id) REFERENCES Letter(letter_id)
);

CREATE TABLE IsDiactricOf
(
  diactric_letter_id INTEGER NOT NULL,
  original_letter_id INTEGER NOT NULL,
  FOREIGN KEY (diactric_letter_id) REFERENCES Letter(letter_id),
  FOREIGN KEY (original_letter_id) REFERENCES Letter(letter_id)
  UNIQUE(diactric_letter_id)
);
