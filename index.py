from main_screen import MainFrame
from login_screen import LoginFrame
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
        
    def switch_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(master=self, app_manager=self)
        self.current_frame.pack(expand=True, fill="both")
        
    def check_auth(self):
        settings_data = get_data("settings.json")
        
        if settings_data["isLogged"]:
            print(f"Користувач {settings_data["userName"]} залогінений")
            self.switch_frame(MainFrame)
        else: 
            print("Користувач не залогінений")
            self.switch_frame(LoginFrame)
        
def start_app():
    if __name__ == "__main__":
        app = App()
        app.mainloop()  
        
start_app()