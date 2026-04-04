import customtkinter as ctk
from login import log, reg
from all_styles import ENTRY_LABEL_STYLE, ENTRY_STYLE, MAIN_LABEL_STYLE, BUTTON_STYLE

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Вхід")
        self.geometry("500x600")

        self.current_frame = None

        self.show_login_frame()

    def show_login_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = LoginFrame(master=self, switch_callback=self.show_register_frame)
        self.current_frame.place(rely=0.5, relx=0.5, anchor="center")       

    def show_register_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = RegistrationFrame(master=self, switch_callback=self.show_login_frame)
        self.current_frame.place(rely=0.5, relx=0.5, anchor="center")

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

def start_app():
    if __name__ == "__main__":
        app = App()
        app.mainloop()  

start_app()