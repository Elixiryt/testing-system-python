import customtkinter as ctk
from login import log, reg
from all_styles import ENTRY_LABEL_STYLE, ENTRY_STYLE, MAIN_LABEL_STYLE, BUTTON_STYLE

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master, fg_color="transparent")
       
        #робимо кнопки да надписи та додаємо їх в фрейм
        self.main_label = ctk.CTkLabel(self, text="Вітаємо у тестуванні!", **MAIN_LABEL_STYLE)
        self.main_label.pack(pady=(0, 20))
       
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Введіть ім'я користувача", **ENTRY_STYLE)
        self.email_entry.pack(pady=10)
       
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Введіть пароль", show="*", **ENTRY_STYLE)
        self.password_entry.pack(pady=10)
       
        self.forget_password_label = ctk.CTkLabel(self, width=150, text="Забули пароль?", text_color="blue")
        self.forget_password_label.pack()
        self.forget_password_label.bind("<Button-1>", lambda e: self.on_label_click)

        self.registration_label = ctk.CTkLabel(self, width=150, text="Немаєте аккаунта?", text_color="blue")
        self.registration_label.pack()
        self.registration_label.bind("<Button-1>", lambda e: switch_callback())

        self.login_button = ctk.CTkButton(self,
                                          **BUTTON_STYLE,
                                          text="Увійти",
                                          command=lambda: log(self.email_entry.get(), self.password_entry.get()))
        self.login_button.pack(pady=10)

class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master, fg_color="transparent")
        
        #робимо кнопки да надписи та додаємо їх в фрейм
        self.main_label = ctk.CTkLabel(self, text="Реєстрація", font=("CtkFont", 36))
        self.main_label.pack(pady=20)

        self.name_surname_label = ctk.CTkLabel(self, text="Прізвище та ім'я", **ENTRY_LABEL_STYLE)
        self.name_surname_label.pack()

        self.name_surname_entry = ctk.CTkEntry(self, **ENTRY_STYLE)
        self.name_surname_entry.pack()

        self.email_label = ctk.CTkLabel(self, text="Електронна пошта", **ENTRY_LABEL_STYLE)
        self.email_label.pack(pady=(10, 0))

        self.email_entry = ctk.CTkEntry(self, **ENTRY_STYLE)
        self.email_entry.pack()
        
        self.password_label = ctk.CTkLabel(self, text="Пароль", **ENTRY_LABEL_STYLE)
        self.password_label.pack(pady=(10, 0))

        self.password_entry = ctk.CTkEntry(self, show="*", **ENTRY_STYLE)
        self.password_entry.pack()

        self.password_again_label = ctk.CTkLabel(self, text="Повторіть пароль", **ENTRY_LABEL_STYLE)
        self.password_again_label.pack(pady=(10, 0))

        self.password_again_entry = ctk.CTkEntry(self, show="*", **ENTRY_STYLE)
        self.password_again_entry.pack(pady=(0, 20))
        
        self.register_button = ctk.CTkButton(
            self,
            text="Зареєструватися",
            command=lambda: reg(self.name_surname_entry.get(), self.email_entry.get(), self.password_entry.get(), self.password_again_entry.get())
            **BUTTON_STYLE)
        self.register_button.pack()

def on_label_click(self):
    print("Ви натиснули на лейбл")