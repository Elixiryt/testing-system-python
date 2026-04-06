import re, random, string, json, os, hashlib, smtplib
from email.message import EmailMessage

file_path = "tests/question.json"
login_file = "logins.json"

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

if __name__ == "__main__":
    runTest()
    
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
    
def generate_secure_code(lenght=6):
    return ''.join(random.choices(string.digits, k=lenght))

def find_user_by_email(email):
    users = get_data(login_file)
    return email in users

def update_password(email, new_password):
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    with open(login_file, "r+", encoding="utf-8") as f:
        users = json.load(f)
        users[email]["password"] = hashed_password
        f.seek(0)
        json.dump(users, f, indent=4)
        f.truncate()

def show_password(entry_widget):
    print("хз")
    
def send_email(subject, body, to_email):
    sender_email = "isnitko@lpc.ukr.education"
    sender_password = "wekk hwxr nbxm wwhj"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP_SSL("smpt@gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Помилка при відправці{e}")