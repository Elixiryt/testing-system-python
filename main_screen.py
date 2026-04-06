import customtkinter as ctk
from all_styles import MAIN_LABEL_STYLE, SECTION_LABEL_STYLE, FRAME_BG_COLOR
from login import get_data
   
data = get_data("settings.json")

# Це буде фрейм для гловного екрану
class MainFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent", width=800, height=600)
        self.pack_propagate=False
        
        self.app_manager = app_manager

        # Цьо хеадер
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=FRAME_BG_COLOR)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        self.header_label = ctk.CTkLabel(self.header, text="Тестування", **MAIN_LABEL_STYLE)
        self.header_label.pack(side="left", padx=20)
        
        self.header_profile_label = ctk.CTkLabel(self.header, text=data["userName"], **MAIN_LABEL_STYLE)
        self.header_profile_label.pack(side="right", padx=20)
        
        # Цьо футер
        self.footer = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=FRAME_BG_COLOR)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.footer_label = ctk.CTkLabel(self.footer, text="Курсова робота | Снітко Ілля | Версія 1.0", **SECTION_LABEL_STYLE)
        self.footer_label.pack(side="left", padx=20)
        
        # Цьо головний блок
        self.main = ctk.CTkFrame(self, fg_color="transparent") 
        self.main.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.main_label = ctk.CTkLabel(self.main, text="Вітаємо в програмі для тестування", **MAIN_LABEL_STYLE)
        self.main_label.pack(side="top", anchor="w", pady=(40, 5), padx=40)
        
        # Тут треба додати підв'язку останньої спроби(напевне через функцію)
        self.last_attempt_label = ctk.CTkLabel(self.main, text="Остання спроба:", **SECTION_LABEL_STYLE)
        self.last_attempt_label.pack(side="top", anchor="w", pady=(0, 40), padx=40)
        
        self.grid = ctk.CTkFrame(self.main, fg_color="transparent")
        self.grid.pack(expand=True)
        
        #Додаємо картки
        self.btn_tests = self.create_card(self.grid, "📝", "ТЕСТИ", "Пройти наявні тести та перевірити знання", self.btn_click, 0, 0)
        self.btn_construtor = self.create_card(self.grid, "🛠️", "КОНСТРУКТОР", "Створити власний тест", self.btn_click, 0, 1)
        self.btn_history = self.create_card(self.grid, "📊", "ІСТОРІЯ", "Переглянути пройдені тести", self.btn_click, 1, 0) 
        self.btn_settings = self.create_card(self.grid, "⚙️", "НАЛАШТУВАННЯ", "Налаштувати клієнт тестів від Снітка", self.btn_click, 1, 1)

        self.bind_all("<Button-4>", self.on_mouse_wheel)
        self.bind_all("<Button-5>", self.on_mouse_wheel)

    # Метод для скроллу на лінуксі
    def on_mouse_wheel(self, event):
        if event.num == 4:
            self._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self._parent_canvas.yview_scroll(1, "units")
        else:
            self._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    # Метод створення карточки
    def create_card(self, master, icon, title, desc, command, row, col):
        card = ctk.CTkFrame(master, width=250, height=250, corner_radius=15, border_width=1)
        card.grid(row=row, column=col, pady=20, padx=20)
        card.grid_propagate(False)
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=icon, font=("Arial", 40)).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=title, font=("Arial", 18, "bold")).pack()
        ctk.CTkLabel(card, text=desc, font=("Arial", 13), text_color="gray", wraplength=240).pack(pady=10)

        btn = ctk.CTkButton(card, text="Відкрити", command=command)
        btn.pack(side="bottom", pady=20)
        return card

    # Тимчасова Метод кнопки
    def btn_click(self):
        print("кнопка нажата")

#Це буде фрейм для екрану тестів
class TestingFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master,fg_color="transparent")