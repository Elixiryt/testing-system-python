import json

file_path = "tests/question.json"

def loadTest():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Помилка: Файл {file_path} не знайдено!")
        return []

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

if __name__ == "__main__":
    #editTest()
    runTest()