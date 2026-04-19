import re, random, string, json, os, hashlib, smtplib
from email.message import EmailMessage
from datetime import datetime

file_path = "tests/question.json"
login_file = "files/logins.json"
    
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
    
# Метод для збереження в історію
def save_history(test_title, score, max_score, percentage):
    history_file = "files/history.json"

    new_entry = {
        "test": test_title,
        "score": f"{score:.0f}/{max_score}",
        "percentage": f"{percentage:.1f}%",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    history = get_data(history_file)

    history.append(new_entry)
    
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
        
def set_latest_attempt():
    data_all = get_data("files/history.json")
    data = data_all[-1]

    if data:
        return f"Остання спроба: {data['test']} - {data['score']}({data['percentage']})"
    else:
        return "Ви ще не проходили тест"
    
def get_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()