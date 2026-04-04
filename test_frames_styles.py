import customtkinter as ctk
from all_styles import ENTRY_LABEL_STYLE, ENTRY_STYLE, MAIN_LABEL_STYLE, BUTTON_STYLE

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Тестування стилів всіх атрибутів")
        self.geometry("600x500")

        self.main_label = ctk.CTkLabel(self, text="Тест стилю головного лейбла", **MAIN_LABEL_STYLE)
        self.main_label.pack(pady=(0, 20))
        
        self.entry_label_style = ctk.CTkLabel(self, text="Тест стилю лейбла над ентрі", **ENTRY_LABEL_STYLE)
        self.entry_label_style.pack()     

        self.entry = ctk.CTkEntry(self, placeholder_text="Тест стилю ентрі", **ENTRY_STYLE)   
        self.entry.pack(pady=(0,20))

        self.button = ctk.CTkButton(self, text="Тест стилю кнопки", **BUTTON_STYLE)
        self.button.pack(pady=(20,0))

if __name__ == "__main__":
    app = App()
    app.mainloop()