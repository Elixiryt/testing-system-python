import sys
import os

# Цей блок каже програмі шукати модулі всередині тимчасової папки EXE
if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
    if basedir not in sys.path:
        sys.path.insert(0, basedir)

from main_screen import MainFrame
from login_screen import LoginFrame
from core import get_data
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        # Налаштування екрану
        self.title("Тестування від Снітка")
        self.geometry("800x600")

        self.current_frame = None
        
        settings_data=get_data("files/settings.json")
        ctk.set_appearance_mode(settings_data["theme"])
        
        self.check_auth()

    def switch_frame(self, frame_class, **kwargs):
        for child in self.winfo_children():
            child.destroy()

        try:
            self.current_frame = frame_class(master=self, app_manager=self, **kwargs)
            self.current_frame.pack(expand=True, fill="both")
            self.update_idletasks()
        except Exception as e:
            print(f"Не вдалось створити фрейм: {e}")
        
    def check_auth(self):
        settings_data = get_data("files/settings.json")
        
        if settings_data["isLogged"]:
            print(f"Користувач {settings_data['userName']} залогінений")
            self.switch_frame(MainFrame)
        else: 
            print("Користувач не залогінений")
            self.switch_frame(LoginFrame)
        
def start_app():
    if __name__ == "__main__":
        app = App()
        app.mainloop()  
        
start_app()
