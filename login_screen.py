import customtkinter as ctk
from login import log, reg

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Вхід")
        self.geometry("500x400")
        
        #робимо кнопки да надписи
        self.label = ctk.CTkLabel(self, text="Вітаємо у тестуванні!", font=("CtkFont", 24))
        self.usernameEntry = ctk.CTkEntry(self, placeholder_text="Введіть ім'я користувача", width=300)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Введіть пароль", width=300, show="*")
        self.start_button = ctk.CTkButton(self, text="Увійти", width=300, command=log)
        self.register_button = ctk.CTkButton(self, text="Немає аккаунта? Зареєструватись", width=300, command=reg)

        #додаємо їх в програму
        self.label.pack(pady=20)
        self.usernameEntry.pack(pady=10)
        self.password_entry.pack(pady=10)
        self.start_button.pack(pady=10)
        self.register_button.pack()
    
if __name__ == "__main__":
    app = App()
    app.mainloop()  