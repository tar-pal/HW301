import sqlite3

# Підключаємося до бази даних або створюємо її
conn = sqlite3.connect('millionaire_game.db')
cursor = conn.cursor()

# Створюємо таблицю з питаннями
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer CHAR(1) NOT NULL,
    difficulty INTEGER NOT NULL
)
''')

# Додаємо питання до бази даних
questions = [
    ("What is the capital of France?", "Berlin", "Madrid", "Paris", "Rome", "C", 1),
    ("What is the largest planet in our solar system?", "Earth", "Jupiter", "Saturn", "Mars", "B", 2),
    ("Which element has the chemical symbol 'O'?", "Oxygen", "Gold", "Iron", "Nitrogen", "A", 1),
    ("Who wrote 'War and Peace'?", "Leo Tolstoy", "Fyodor Dostoevsky", "Alexander Pushkin", "Anton Chekhov", "A", 3),
    ("What is the speed of light?", "300,000 km/s", "150,000 km/s", "1,000,000 km/s", "500,000 km/s", "A", 3)
]

# Заповнюємо базу даних питаннями
cursor.executemany('''
    INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer, difficulty)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', questions)

conn.commit()
conn.close()

print("Базу даних успішно створено та заповнено!!!")
