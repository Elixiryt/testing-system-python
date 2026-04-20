import customtkinter as ctk
import json
from core import enable_email_verification, generate_secure_code, find_user_by_email, send_email, update_password, get_data, resource_path
from login import login, register_user
from all_styles import ENTRY_LABEL_STYLE, ENTRY_STYLE, MAIN_LABEL_STYLE, BUTTON_STYLE, BACK_BUTTON_STYLE, ACCENT_COLOR

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent")
       
        self.app_manager = app_manager
              
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        #робимо кнопки да надписи та додаємо їх в фрейм
        self.main_label = ctk.CTkLabel(self.container, text="Вітаємо у тестуванні!", **MAIN_LABEL_STYLE)
        self.main_label.pack(pady=(0, 20))
        
        self.error_label = ctk.CTkLabel(self.container, text_color="red", text="")
        self.error_label.pack()
       
        self.email_label = ctk.CTkLabel(self.container, text="Введіть електронну пошту", **ENTRY_LABEL_STYLE)
        self.email_label.pack(pady=(10, 0))
       
        self.email_entry = ctk.CTkEntry(self.container, placeholder_text="example@gmail.com", **ENTRY_STYLE)
        self.email_entry.pack()
        enable_email_verification(self.email_entry)
       
        self.password_label = ctk.CTkLabel(self.container, text="Введіть пароль", **ENTRY_LABEL_STYLE)
        self.password_label.pack(pady=(10, 0))
       
        self.password_entry = ctk.CTkEntry(self.container, placeholder_text="", show="*", **ENTRY_STYLE)
        self.password_entry.pack()
        
        self.show_password_checkbox = ctk.CTkCheckBox(self.container, text="Показати пароль", checkbox_height=20, checkbox_width=20, command=self.toogle_show_password)
        self.show_password_checkbox.pack(anchor="w", padx=40, pady=5)

        self.grid = ctk.CTkFrame(self.container, fg_color="transparent")
        self.grid.pack()
        
        self.forget_password_label = ctk.CTkLabel(self.grid, width=150, text="Забули пароль?", text_color=ACCENT_COLOR)
        self.forget_password_label.grid(row=0, column=0, pady=5, padx=20)
        self.forget_password_label.bind("<Button-1>", lambda e: self.app_manager.switch_frame(ForgetPasswordFrame))

        self.registration_label = ctk.CTkLabel(self.grid, width=150, text="Немаєте аккаунта?", text_color=ACCENT_COLOR)
        self.registration_label.grid(row=0, column=1, pady=5, padx=20)
        self.registration_label.bind("<Button-1>", lambda e: self.app_manager.switch_frame(RegistrationFrame))

        self.login_button = ctk.CTkButton(self.container,
                                          text="Увійти",
                                          command=lambda: self.log(self.email_entry.get(), self.password_entry.get()),
                                          **BUTTON_STYLE)
        self.login_button.pack(pady=10)
        
        self.guest_label = ctk.CTkLabel(self.container, text="Увійти як гість", text_color="gray")
        self.guest_label.pack()
        self.guest_label.bind("<Button-1>", lambda e: self.login_as_guest())
        
    def toogle_show_password(self):
        if self.show_password_checkbox.get() == 1:
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
        
    def log(self, email, password):
        if login(email, password):
            from main_screen import MainFrame
            self.app_manager.switch_frame(MainFrame)
        else:
            self.password_entry.configure(border_color="red")
            self.email_entry.configure(border_color="red")
            self.error_label.configure(text="Неправильний пароль або ел. адреса")
            print("Користувач не залогінений")
            
    def login_as_guest(self):
        settings_file = resource_path("files/settings.json")
        from main_screen import MainFrame
        self.app_manager.switch_frame(MainFrame)
        
        data = get_data(settings_file)
        data["isLogged"] = True
        data["userName"] = "Гість"
        
        with open(settings_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

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
        
        self.error_label = ctk.CTkLabel(self.container, text="", text_color="red")
        self.error_label.pack()

        self.name_surname_label = ctk.CTkLabel(self.container, text="Прізвище та ім'я", **ENTRY_LABEL_STYLE)
        self.name_surname_label.pack()

        self.name_surname_entry = ctk.CTkEntry(self.container, placeholder_text="Іванов Іван", **ENTRY_STYLE)
        self.name_surname_entry.pack()

        self.email_label = ctk.CTkLabel(self.container, text="Електронна пошта", **ENTRY_LABEL_STYLE)
        self.email_label.pack(pady=(10, 0))

        self.email_entry = ctk.CTkEntry(self.container, placeholder_text="example@gmail.com", **ENTRY_STYLE)
        self.email_entry.pack()
        enable_email_verification(self.email_entry)
        
        self.password_label = ctk.CTkLabel(self.container, text="Пароль", **ENTRY_LABEL_STYLE)
        self.password_label.pack(pady=(10, 0))

        self.password_entry = ctk.CTkEntry(self.container, show="*", **ENTRY_STYLE)
        self.password_entry.pack()
        
        self.password_again_label = ctk.CTkLabel(self.container, text="Повторіть пароль", **ENTRY_LABEL_STYLE)
        self.password_again_label.pack(pady=(10, 0))

        self.password_again_entry = ctk.CTkEntry(self.container, show="*", **ENTRY_STYLE)
        self.password_again_entry.pack()

        self.show_password_checkbox = ctk.CTkCheckBox(self.container, text="Показати пароль", checkbox_height=20, checkbox_width=20, command=self.toogle_show_password)
        self.show_password_checkbox.pack(anchor="w", pady=(5, 20), padx=0)
        
        self.register_button = ctk.CTkButton(
            self.container,
            text="Зареєструватися",
            command=lambda: self.reg(),
            **BUTTON_STYLE)
        self.register_button.pack()
        
    def reg(self):
        if register_user(self.name_surname_entry.get(), self.email_entry.get(), self.password_entry.get(), self.password_again_entry.get()) == "Користувач з цією поштою вже існує":
            self.email_entry.configure(border_color="red")
            self.error_label.configure(text="Користувач з такою поштою вже зареєстрований")
        elif register_user(self.name_surname_entry.get(), self.email_entry.get(), self.password_entry.get(), self.password_again_entry.get()) == "Мінімальна довжина паролю 8 символів":
            self.password_entry.configure(border_color="red")
            self.password_again_entry.configure(border_color="red")
            self.error_label.configure(text="Мінімальна довжина паролю це 8 символів")
        elif register_user(self.name_surname_entry.get(), self.email_entry.get(), self.password_entry.get(), self.password_again_entry.get()) == "Паролі не збігаються":
            self.password_again_entry.configure(border_color="red")
            self.password_entry.configure(border_color="red")
            self.error_label.configure(text="Паролі не збігаються")
        elif register_user(self.name_surname_entry.get(), self.email_entry.get(), self.password_entry.get(), self.password_again_entry.get()) == "Всі поля повинні бути заповненні":
            self.error_label.configure(text="Всі поля повинні бути заповненні")
            if self.name_surname_entry.get() == "":
                self.name_surname_entry.configure(border_color="red")
            elif self.email_entry.get() == "":
                self.email_entry.configure(border_color="red")                
            elif self.password_entry.get() == "":
                self.password_entry.configure(border_color="red")
            elif self.password_again_entry.get() == "":
                self.password_again_entry.configure(border_color="red")
        else:
            register_user(self.name_surname_entry.get(), self.email_entry.get(), self.password_entry.get(), self.password_again_entry.get())
        
    def toogle_show_password(self):
        if self.show_password_checkbox.get() == 1:
            self.password_entry.configure(show="")
            self.password_again_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
            self.password_again_entry.configure(show="*")
        
class ForgetPasswordFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent")
        
        self.app_manager = app_manager
        
        # Кнопка назад
        self.back_button = ctk.CTkButton(self, command=lambda: self.app_manager.switch_frame(LoginFrame), **BACK_BUTTON_STYLE)
        self.back_button.place(rely=0.05, relx=0.05, anchor= "nw")
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.main_label = ctk.CTkLabel(self.container, text="Забули пароль?", **MAIN_LABEL_STYLE)
        self.main_label.pack()
        
        self.error_label = ctk.CTkLabel(self.container, text="", text_color="red")
        self.error_label.pack()

        self.email_label = ctk.CTkLabel(self.container, text="Введіть email", **ENTRY_LABEL_STYLE)
        self.email_label.pack(pady=(20,0))
        # Етап 1
        self.email_entry = ctk.CTkEntry(self.container, placeholder_text="example@gmail.com", **ENTRY_STYLE)
        self.email_entry.pack(pady=(0,20))
        enable_email_verification(self.email_entry)
        self.isVisible = True
        
        self.send_email_button = ctk.CTkButton(self.container,
                                              text="Відправити код",
                                              command=lambda: self.process_step1(),
                                              **BUTTON_STYLE)
        self.send_email_button.pack(pady=(0,20))

        # Етап 2
        self.code_entry = ctk.CTkEntry(self.container, **ENTRY_STYLE)
        
        self.code_button = ctk.CTkButton(self.container, text="Підтвердити", command=lambda: self.process_step2(), **BUTTON_STYLE)
        
        self.rewrite_email_label = ctk.CTkLabel(self.container, text="Неправильно введений email?")
        self.rewrite_email_label.bind("<Button-1>", lambda e: self.hide_email_screen())
        
        # Етап 3
        self.new_password_entry = ctk.CTkEntry(self.container, show="*", placeholder_text="********", **ENTRY_STYLE)
        self.commit_password_button = ctk.CTkButton(self.container, text="Змінити пароль", command=lambda: self.process_step3(), **BUTTON_STYLE)
        
    # Метод для кроку 1
    def process_step1(self):
        email = self.email_entry.get()
        if find_user_by_email(email):
            self.user_email = email
            self.generated_code = generate_secure_code()
            
            send_email("Відновлення паролю в тестах", self.generated_code, self.user_email)
            
            self.email_label.configure(text="Введіть код з листа")
            self.email_entry.pack_forget()
            self.send_email_button.pack_forget()
            self.error_label.configure(text="")

            self.code_entry.pack(pady=(0,20))
            self.code_button.pack(pady=(20, 0))
            self.rewrite_email_label.pack()
        else:
            print("Користувача з такою поштою не існує")
            self.email_entry.configure(border_color="red")
            self.error_label.configure(text="Не зареєстровано користувача з такою поштою")
            
    # Метод для кроку 2
    def process_step2(self):
        if self.code_entry.get() == self.generated_code:
            self.email_label.configure(text="Введіть новий пароль")
            self.code_entry.pack_forget()
            self.code_button.pack_forget()
            self.rewrite_email_label.pack_forget()
            self.error_label.configure(text="")

            self.new_password_entry.pack(pady=(0,20))
            self.commit_password_button.pack(pady=20)
        else:
            self.code_entry.configure(border_color="red")
            self.error_label.configure(text="Код не співпадає")

    # Метод для кроку 3
    def process_step3(self):
        new_password = self.new_password_entry.get()
        if len(new_password)>=8:
            update_password(self.user_email, new_password)
            self.app_manager.switch_frame(LoginFrame)
            
    # Метод для зміни ел. пошти
    def hide_email_screen(self):
        if self.isVisible:
            self.email_entry.pack_forget()
            self.send_email_button.pack_forget()
            self.code_entry.pack(pady=20)
            self.code_button.pack(pady=(20, 0))
            self.rewrite_email_label.pack()
            self.isVisible = False
        else:
            self.code_entry.pack_forget()
            self.code_button.pack_forget()
            self.rewrite_email_label.pack_forget()
            self.email_entry.pack(pady=20)
            self.send_email_button.pack(pady=20)
            self.isVisible = True