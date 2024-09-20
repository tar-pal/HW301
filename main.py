from fastapi import FastAPI, HTTPException,Query
from pydantic import BaseModel
import sqlite3
import random

# Ініціалізація FastAPI додатку
app = FastAPI()

# Модель для отримання відповідей від користувача
class Answer(BaseModel):
    question_id: int
    selected_answer: str


# Підключаємося до бази даних та отримуємо з'єднання
def get_db_connection():
    conn = sqlite3.connect('millionaire_game.db')
    conn.row_factory = sqlite3.Row  # Для отримання результатів у вигляді словника
    return conn


# 1. Ендпоінт для отримання питань
@app.get("/questions/")
def get_questions(limit: int = 5, difficulty: int = Query(0, description="Рівень складності питання")):
    """
    Отримуємо рандомні питання з бази даних для гри.
    Параметр 'limit' визначає кількість питань, які повертаються.
    Параметр 'difficulty' дозволяє фільтрувати питання за рівнем складності.

    приклади запитів:
    http://127.0.0.1:8000/questions/?limit=1
    http://127.0.0.1:8000/questions/?limit=5&difficulty=1

    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Якщо рівень складності не задано, вибираємо всі питання, інакше фільтруємо за складністю
    if difficulty == 0:
        cursor.execute("SELECT * FROM questions")
    else:
        cursor.execute("SELECT * FROM questions WHERE difficulty = ?", (difficulty,))

    questions = cursor.fetchall()

    # Перевіряємо, чи є доступні питання
    if not questions:
        conn.close()
        raise HTTPException(status_code=404, detail="Питання не знайдено для заданого рівня складності")

    # Вибираємо випадкові питання
    random_questions = random.sample(questions, min(len(questions), limit))

    # Форматуємо питання в зручний формат
    formatted_questions = []
    for question in random_questions:
        formatted_questions.append({
            "id": question["id"],
            "question": question["question"],
            "options": {
                "A": question["option_a"],
                "B": question["option_b"],
                "C": question["option_c"],
                "D": question["option_d"]
            },
            "difficulty": question["difficulty"]
        })

    conn.close()
    return formatted_questions


# 2. Ендпоінт для перевірки відповіді
@app.post("/check_answer/")
def check_answer(answer: Answer):
    """
    Приймаємо відповідь від користувача та перевіряємо її правильність.
    тіло запиту:
    {
      "question_id": 1,
      "selected_answer": "C"
    }

    відповідь:
    {
      "question_id": 1,
      "correct": true
    }
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Отримуємо правильну відповідь з бази даних
    cursor.execute("SELECT correct_answer FROM questions WHERE id = ?", (answer.question_id,))
    question = cursor.fetchone()

    if question is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Питання не знайдено")

    # Перевіряємо правильність відповіді
    correct = question["correct_answer"].upper() == answer.selected_answer.upper()

    conn.close()

    return {"question_id": answer.question_id, "correct": correct}