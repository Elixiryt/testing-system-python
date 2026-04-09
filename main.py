import re, random, string, json, os, hashlib, smtplib
from email.message import EmailMessage
from datetime import datetime

file_path = "tests/question.json"
login_file = "files/logins.json"

#Метод завантаження тесту з файлу
def loadTest():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Помилка: Файл {file_path} не знайдено!")
        return []

# Метод додавання питань до тесту
def editTest():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        new_question_number = int(input("Введіть кількість нових питань"))
        file_length = len(data)

        for i in range(new_question_number):
            question = input("Введіть питання")
            number_of_options = int(input("Введіть кількість варіантів відповідей"))
            options = []

            for i in range(number_of_options):
                option = input(f"Введіть варіант відповіді №{i+1}")
                options.append(option)

            answer = input("Введіть правильну відповідь")
            data.append({"id": file_length + i + 1, "question": question, "options": options, "answer": answer})

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except FileNotFoundError:                
        print(f"Помилка: Файл {file_path} не знайдено!")
        return []        

# Метод запуску тесту
def runTest():
    questions = loadTest()
    score = 0
    
    if not questions:
        return

    print("=== Ласкаво просимо до системи тестування ===\n")

    for q in questions:
        print(f"Питання №{q['id']}: {q['question']}")
        
        # Виводимо варіанти відповідей
        for i, option in enumerate(q['options'], 1):
            print(f"{i}. {option}")
        
        user_choice = input("\nВаша відповідь (напишіть текст або номер): ").strip()

        # Перевірка: користувач міг ввести або текст, або номер
        if user_choice == q['answer'] or (user_choice.isdigit() and q['options'][int(user_choice)-1] == q['answer']):
            print("✅ Правильно!\n")
            score += 1
        else:
            print(f"❌ Неправильно. Правильна відповідь: {q['answer']}\n")

    print("--- Тест завершено ---")
    print(f"Ваш результат: {score} з {len(questions)}")
    
# Метод отримання даних з файлу
def get_data(new_file):
    if not os.path.exists(new_file) or os.path.getsize(new_file) == 0:
        return []
    with open(new_file, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
    
#  Метод для перевірки на email
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Метод для живої перевірки на email
def enable_email_verification(entry_widget):
    def validate(event):
        email = entry_widget.get()
        if email == "":
            entry_widget.configure(border_color=["#979da2", "#565b5e"])
        elif is_valid_email(email):
            entry_widget.configure(border_color="green")
        else:
            entry_widget.configure(border_color="red")
    entry_widget.bind("<KeyRelease>", validate)
    
# Для створення рандомної послідовності з 6 цифр
def generate_secure_code(lenght=6):
    return ''.join(random.choices(string.digits, k=lenght))

# Пошук користувача за поштою
def find_user_by_email(user_email):
    users = get_data(login_file)
    for user in users:
        if user.get("email") == user_email:
            return True
    return False

# Зміна паролю
def update_password(email, new_password):
    users = get_data(login_file)
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    user_found = None
    for user in users:
        if user.get("email") == email:
            user["password"] = hashed_password
            user_found = True
            break
        
    if user_found:
        with open(login_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
            print(f"Пароль для користувача {email} успішно змінений")
    else:
        print("Помилка: Користувача не знайдено при оновленні")
        
# Вислати ел. листа
def send_email(subject, body, to_email):
    sender_email = "isnitko@lpc.ukr.education"
    sender_password = "wekk hwxr nbxm wwhj"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Помилка при відправці{e}")
        
# Метод для створення списку з наявними тестами
def get_test_files():
    folder_path = "tests"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return []
    
    return [f for f in os.listdir(folder_path) if f.endswith(".json")]

# Метод для завантаження метаданих тесту
def get_test_metadata(filename):
    path = os.path.join("tests", filename)
    try:
        data = get_data(path)
        
        # Перевіряємо, чи отримані дані є словником
        if isinstance(data, dict):
            info = data.get("info", {})
            return {
                "filename": filename,
                "title": info.get("title", filename.replace(".json", "")),
                "creator": info.get("creator", "Aнонім"),
                "description": info.get("description", ""),
                "max_score": info.get("max_score", 12)
            }
        
        # Якщо це список (просто питання без метаданих)
        elif isinstance(data, list):
            return {
                "filename": filename,
                "title": filename.replace(".json", ""), # Назва - це ім'я файлу
                "creator": "Невідомий (JSON-list)",
                "description": "Метадані відсутні у списку",
                "max_score": 12
            }
            
    except Exception as e:
        # Тепер ми побачимо, якщо вилетить щось інше
        print(f"Помилка в метаданих для {filename}: {e}")
        return None
    
def save_history(test_title, score, max_score, percentage):
    history_file = "files/history.json"

    new_entry = {
        "test": test_title,
        "score": f"{score}/{max_score}",
        "percentage": f"{percentage}%",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    history = get_data(history_file)

    history.append(new_entry)
    
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)