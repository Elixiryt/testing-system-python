import customtkinter as ctk
import secrets, hashlib
from main import enable_email_verification, generate_secure_code, find_user_by_email, send_email, update_password
from login import login, register
from all_styles import ENTRY_LABEL_STYLE, ENTRY_STYLE, MAIN_LABEL_STYLE, BUTTON_STYLE, BACK_BUTTON_STYLE

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent")
       
        self.app_manager = app_manager
              
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        #робимо кнопки да надписи та додаємо їх в фрейм
        self.main_label = ctk.CTkLabel(self.container, text="Вітаємо у тестуванні!", **MAIN_LABEL_STYLE)
        self.main_label.pack(pady=(0, 20))
       
        self.email_label = ctk.CTkLabel(self.container, text="Введіть електронну пошту", **ENTRY_LABEL_STYLE)
        self.email_label.pack(pady=(10, 0))
       
        self.email_entry = ctk.CTkEntry(self.container, placeholder_text="Введіть ім'я користувача", **ENTRY_STYLE)
        self.email_entry.pack()
        enable_email_verification(self.email_entry)
       
        self.password_label = ctk.CTkLabel(self.container, text="Введіть пароль", **ENTRY_LABEL_STYLE)
        self.password_label.pack(pady=(10, 0))
       
        self.password_entry = ctk.CTkEntry(self.container, placeholder_text="Введіть пароль", show="*", **ENTRY_STYLE)
        self.password_entry.pack()

        self.grid = ctk.CTkFrame(self.container, fg_color="transparent")
        self.grid.pack()
        
        self.forget_password_label = ctk.CTkLabel(self.grid, width=150, text="Забули пароль?", text_color="blue")
        self.forget_password_label.grid(row=0, column=0, pady=5, padx=20)
        self.forget_password_label.bind("<Button-1>", lambda e: self.app_manager.switch_frame(ForgetPasswordFrame))

        self.registration_label = ctk.CTkLabel(self.grid, width=150, text="Немаєте аккаунта?", text_color="blue")
        self.registration_label.grid(row=0, column=1, pady=5, padx=20)
        self.registration_label.bind("<Button-1>", lambda e: self.app_manager.switch_frame(RegistrationFrame))

        self.login_button = ctk.CTkButton(self.container,
                                          text="Увійти",
                                          command=lambda: self.log(self.email_entry.get(), self.password_entry.get()),
                                          **BUTTON_STYLE)
        self.login_button.pack(pady=10)
        
    def log(self, email, password):
        if login(email, password):
            from main_screen import MainFrame
            self.app_manager.switch_frame(MainFrame)
        else:
            print("Користувач не залогінений")

class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent")
        
        self.app_manager = app_manager
        
        self.back_button = ctk.CTkButton(self, command=lambda: self.app_manager.switch_frame(LoginFrame), **BACK_BUTTON_STYLE)
        self.back_button.place(rely=0.05, relx=0.05, anchor="nw")
        
        #робимо кнопки да надписи та додаємо їх в фрейм
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.main_label = ctk.CTkLabel(self.container, text="Реєстрація", **MAIN_LABEL_STYLE)
        self.main_label.pack(pady=20)

        self.name_surname_label = ctk.CTkLabel(self.container, text="Прізвище та ім'я", **ENTRY_LABEL_STYLE)
        self.name_surname_label.pack()

        self.name_surname_entry = ctk.CTkEntry(self.container, **ENTRY_STYLE)
        self.name_surname_entry.pack()

        self.email_label = ctk.CTkLabel(self.container, text="Електронна пошта", **ENTRY_LABEL_STYLE)
        self.email_label.pack(pady=(10, 0))

        self.email_entry = ctk.CTkEntry(self.container, **ENTRY_STYLE)
        self.email_entry.pack()
        enable_email_verification(self.email_entry)
        
        self.password_label = ctk.CTkLabel(self.container, text="Пароль", **ENTRY_LABEL_STYLE)
        self.password_label.pack(pady=(10, 0))

        self.password_entry = ctk.CTkEntry(self.container, show="*", **ENTRY_STYLE)
        self.password_entry.pack()

        self.password_again_label = ctk.CTkLabel(self.container, text="Повторіть пароль", **ENTRY_LABEL_STYLE)
        self.password_again_label.pack(pady=(10, 0))

        self.password_again_entry = ctk.CTkEntry(self.container, show="*", **ENTRY_STYLE)
        self.password_again_entry.pack(pady=(0, 20))
        
        self.register_button = ctk.CTkButton(
            self.container,
            text="Зареєструватися",
            command=lambda: register(self.name_surname_entry.get(), self.email_entry.get(), self.password_entry.get(), self.password_again_entry.get()),
            **BUTTON_STYLE)
        self.register_button.pack()
        
class ForgetPasswordFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent")
        
        self.app_manager = app_manager
        
        # Кнопка назад
        self.back_button = ctk.CTkButton(self, **BACK_BUTTON_STYLE)
        self.back_button.place(rely=0.05, relx=0.05, anchor= "nw")
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.main_label = ctk.CTkLabel(self.container, text="Забули пароль?", **MAIN_LABEL_STYLE)
        self.main_label.pack()
        
        # Етап 1
        self.email_entry = ctk.CTkEntry(self.container)
        self.email_entry.pack(pady=20)
        enable_email_verification(self.email_entry)
        self.isVisible = True
        
        self.send_email_button = ctk.CTkButton(self.container,
                                              text="Відправити код",
                                              command=lambda: self.procces_step1(),
                                              **BUTTON_STYLE)
        self.send_email_button.pack(pady=20)

        # Етап 2
        self.code_entry = ctk.CTkEntry(self.container)
        
        self.code_button = ctk.CTkButton(self.container, text="Підтвердити", command=lambda: self.process_step1() **BUTTON_STYLE)
        
        self.rewrite_email_label = ctk.CTkLabel(self.container, text="Неправильно введений email?")
        self.rewrite_email_label.bind("<Button-1>", lambda e: self.hide_email_screen())
        
        # Етап 3
        self.new_password_entry = ctk.CTkEntry(self.container, show="*")
        self.commit_password_button = ctk.CTkButton(self.container, text="Змінити пароль", command=lambda: self.process_step3(), **BUTTON_STYLE)
        
    def procces_step1(self):
        email = self.email_entry.get()
        if find_user_by_email(email):
            self.user_email = email
            self.generated_code = generate_secure_code()
            
            send_email("Відновлення паролю в тестах", self.generated_code, self.user_email)
            
            self.main_label.configure(text="Введіть код підтвердження")
            self.email_entry.pack_forget()
            self.send_email_button.pack_forget()

            self.code_entry.pack(pady=20)
            self.code_button.pack(pady=(20, 0))
            self.rewrite_email_label.pack()
        else:
            print("Користувача з такою поштою не існує")
            
    def process_step2(self):
        if self.code_entry.get() == self.generated_code:
            self.code_entry.pack_forget()
            self.code_button.pack_forget()
            self.rewrite_email_label.pack_forget()

            self.new_password_entry.pack(pady=20)
            self.commit_password_button.pack(pady=20)
        else:
            self.code_entry.configure(border_color="red")

    def process_step3(self):
        new_password = hashlib.sha256(self.new_password_entry.get().encode()).hexdigest()
        if len(new_password)>=8:
            update_password(self.user_email, new_password)
            self.app_manager.switch_frame(LoginFrame)
            
    def hide_email_screen(self):
        if self.isVisible:
            self.email_entry.pack_forget()
            self.send_email_entry.pack_forget()
            self.code_entry.pack(pady=20)
            self.code_button.pack(pady=(20, 0))
            self.rewrite_email_label.pack()
            self.isVisible = False
        else:
            self.code_entry.pack_forget()
            self.code_button.pack_forget()
            self.rewrite_email_label.pack_forget()
            self.email_entry.pack(pady=20)
            self.send_email_entry.pack(pady=20)
            self.isVisible = True

# Для запуску скріна напряму
if __name__ == "__main__":
    root = ctk.CTk()
    
    class FakeManager:
        def switch_frame(self, frame_class):
            print(f"Хочу запустити фрейм {frame_class}")

    frame = LoginFrame(master=root, app_manager=FakeManager())
    frame.pack(expand=True, fill="both")
    
    root.mainloop()