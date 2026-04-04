from main_screen import MainFrame, TestingFrame
from login_screen import LoginFrame, RegistrationFrame
from main import get_data
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        # Налаштування екрану
        self.title("Тестування від Снітка")
        self.geometry("800x600")

        self.current_frame = None
        
        self.check_auth()
        
    def check_auth(self):
        settings_data = get_data("settings.json")
        
        if settings_data["isLogged"]:
            print(f"Користувач {settings_data["userName"]} залогінений")
        else: 
            print("Користувач не залогінений")
    
    # Метод переключення фрейму на фрейм тестів
    def show_main_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy

        self.current_frame = MainFrame(master=self, switch_callback=self.show_testing_frame)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    # Метод переключення фрейму на головний фрейм
    def show_testing_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy

        self.current_frame = TestingFrame(master=self, switch_callback=self.show_main_frame)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")
     
    # Метод переключення фрейму на логін    
    def show_login_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = LoginFrame(master=self, switch_callback=self.show_register_frame)
        self.current_frame.place(rely=0.5, relx=0.5, anchor="center")       

    # Метод переключення фрейму на регістрацію
    def show_register_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = RegistrationFrame(master=self, switch_callback=self.show_login_frame)
        self.current_frame.place(rely=0.5, relx=0.5, anchor="center")
        
def start_app():
    if __name__ == "__main__":
        app = App()
        app.mainloop()  
        
start_app()