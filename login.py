from core import get_data
import hashlib
import json

log_file = "files/logins.json"
settings_file = "files/settings.json"

# Метод логіну
def login(email, password):
    login_data = get_data(log_file)
    settings_data = get_data(settings_file)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user_found = None
    for user in login_data:
        if user["email"] == email:
            user_found = user
            print("Користувач знайдений")
            break

    if user_found:
        if user_found["password"] == hashed_password:
            settings_data["userName"] = user_found["name"]
            settings_data["isLogged"] = True
            
            print("Налаштування збережені")
            
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=4)
                
            return True
        else:
            print("Неправильний пароль")
            return False
    else:
        print("Користувача з такою поштою не знайдено")

# Пишемо метод регістрації
def register_user(name, email, password, repeated_password):    
    dataW = get_data(log_file)

    if any(user["email"] == email for user in dataW):
        return "Користувач з цією поштою вже існує"
    
    elif len(password)<8:
        return "Мінімальна довжина паролю 8 символів"
    
    elif repeated_password != password:
        return "Паролі не збігаються"
    
    elif email == "" or name == "" or password == 0:
        return "Всі поля повинні бути заповненні"
    
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        dataW.append({
            "email": email,
            "name": name,
            "password": hashed_password,
        })
        with open(log_file, "w", encoding="utf-8") as file:
            json.dump(dataW, file, ensure_ascii=False, indent=4)