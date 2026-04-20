import customtkinter as ctk
import os, json
from all_styles import MAIN_LABEL_STYLE, BORDER_COLOR, FRAME_BG_COLOR, BACK_BUTTON_STYLE, BUTTON_STYLE, HEADER_STYLE, BG_COLOR, TEXT_SECONDARY, TABLE_SECONDARY, BUTTON_STYLE_WITHOUT_COLOR
from login import get_data
from core import get_test_files, get_test_metadata, save_history, set_latest_attempt, get_hash

settings_data = get_data("files/settings.json")

# Це буде фрейм для гловного екрану
class MainFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color=BG_COLOR)
        
        self.app_manager = app_manager

        # Цьо хеадер
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=FRAME_BG_COLOR)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        self.header_label = ctk.CTkLabel(self.header, text="Тестування", **HEADER_STYLE)
        self.header_label.pack(side="left", padx=20)
        
        self.header_profile_label = ctk.CTkLabel(self.header, text=settings_data["userName"], **MAIN_LABEL_STYLE)
        self.header_profile_label.pack(side="right", padx=20)
        
        # Цьо футер
        self.footer = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=FRAME_BG_COLOR)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.footer_label = ctk.CTkLabel(self.footer, text="Курсова робота | Снітко Ілля | Версія 1.0", text_color=TEXT_SECONDARY, font=("Arial", 16))
        self.footer_label.pack(side="left", padx=20)
        
        # Цьо головний блок
        self.main = ctk.CTkFrame(self, fg_color="transparent") 
        self.main.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.main_label = ctk.CTkLabel(self.main, text="Вітаємо в програмі для тестування", **MAIN_LABEL_STYLE)
        self.main_label.pack(side="top", anchor="w", pady=(40, 5), padx=40)
        
        # Тут треба додати підв'язку останньої спроби(напевне через функцію)
        self.last_attempt_label = ctk.CTkLabel(self.main, text=set_latest_attempt(), text_color=TEXT_SECONDARY)
        self.last_attempt_label.pack(side="top", anchor="w", pady=(0, 40), padx=40)
        
        self.grid = ctk.CTkFrame(self.main, fg_color="transparent")
        self.grid.pack(expand=True)
        
        #Додаємо картки
        self.btn_tests = self.create_card(
            self.grid,
            "📝",
            "ТЕСТИ",
            "Пройти наявні тести та перевірити знання",
            lambda: self.app_manager.switch_frame(TestsListFrame),
            0, 0)
        
        self.btn_construtor = self.create_card(
            self.grid,
            "🛠️",
            "КОНСТРУКТОР",
            "Створити власний тест",
            lambda: self.app_manager.switch_frame(ConstructorFrame),
            0, 1)
        self.btn_history = self.create_card(
            self.grid,
            "📊",
            "ІСТОРІЯ",
            "Переглянути пройдені тести",
            lambda: self.app_manager.switch_frame(HistoryFrame),
            1, 0) 
        self.btn_settings = self.create_card(
            self.grid,
            "⚙️",
            "НАЛАШТУВАННЯ",
            "Налаштувати клієнту тестів від Снітка",
            lambda: self.app_manager.switch_frame(SettingsFrame),
            1, 1)

        self.bind_all("<Button-4>", self.on_mouse_wheel)
        self.bind_all("<Button-5>", self.on_mouse_wheel)

    # Метод для скроллу на лінуксі
    def on_mouse_wheel(self, event):
        if not self.winfo_exists():
            return
        
        try:
            if event.num == 4:
                self._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self._parent_canvas.yview_scroll(1, "units")
            else:
                self._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
            
    # Метод створення карточки
    def create_card(self, master, icon, title, desc, command, row, col):
        card = ctk.CTkFrame(master, width=250, height=250, corner_radius=15, border_width=1)
        card.grid(row=row, column=col, pady=20, padx=20)
        card.grid_propagate(False)
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=icon, font=("Arial", 40)).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=title, font=("Arial", 18, "bold")).pack()
        ctk.CTkLabel(card, text=desc, font=("Arial", 13), text_color="gray", wraplength=240).pack(pady=10)

        btn = ctk.CTkButton(card, text="Відкрити", command=command, **BUTTON_STYLE)
        btn.pack(side="bottom", pady=20)
        return card

    # Тимчасова Метод кнопки
    def btn_click(self):
        print("кнопка нажата")

#Це буде фрейм для екрану списку тестів
class TestsListFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color=BG_COLOR)
        self.app_manager = app_manager
        
        # Робим хеадер
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=FRAME_BG_COLOR)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        self.back_button = ctk.CTkButton(self.header, command=lambda: self.app_manager.switch_frame(MainFrame), **BACK_BUTTON_STYLE)
        self.back_button.place(relx=0.01, rely=0.25, anchor="nw")
        
        self.header_label = ctk.CTkLabel(self.header, text="Виберіть тест для проходження", **HEADER_STYLE)
        self.header_label.pack(padx=60, pady=10, side="left")
        
        # Основний контейнер для списку
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both")
        
        # Запускаємо рендер
        self.render_test_list()
        
    # Метод для рендеру списку
    def render_test_list(self):
        tests = get_test_files()

        # Перевіряємо чи є папка "tests"
        if not tests:
            ctk.CTkLabel(self.container, text="Тестів поки що не знайдено").pack(pady=20)
            print("нема тестів")
            return

        for test_file in tests:
            # Загружаємо метадані
            metadata = get_test_metadata(test_file)
            if not metadata:
                continue
            
            # Елесент списку
            list_chunk = ctk.CTkFrame(self.container, height=80, corner_radius=20, fg_color=FRAME_BG_COLOR)
            list_chunk.pack(fill="x", pady=5, padx=20)
            list_chunk.pack_propagate(False)
            
            # Контейнер щоб назва і автор тесту були в 1 стовпці
            text_container = ctk.CTkFrame(list_chunk, fg_color="transparent")
            text_container.pack(side="left", padx=20)
            
            ctk.CTkLabel(text_container, text=metadata["title"], font=("Arial", 24, "bold")).pack(anchor="w")
            ctk.CTkLabel(text_container, text=metadata["creator"], text_color="gray").pack(anchor="w")
            
            # Кнопка запуску тесту
            ctk.CTkButton(list_chunk, text="Відкрити тест", command=lambda f=test_file: self.open_test(f), **BUTTON_STYLE).pack(padx=20, side="right")

    # Метод запуску тесту
    def open_test(self, filename):
        self.app_manager.switch_frame(TestingFrame, test_file=filename)
        print(f"Запускаємо тест: {filename}")
        
# Фрейм тестування
class TestingFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager, test_file):
        super().__init__(master, fg_color=BG_COLOR)
        self.app_manager = app_manager
        self.test_file = test_file
        
        # Створюємо словник для відповідей (КРИТИЧНО)
        self.user_answers = {}
        
        self.test_data = self.load_test_data()
        self.questions = self.test_data.get("questions", [])
        self.current_question_index = 0
        
        # Запускаємо UI та Навігацію
        self.setup_ui()
        self.setup_navigation()
        self.display_question()
    
    def load_test_data(self):
        path = os.path.join("tests", self.test_file)
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    # Метод для створення UI
    def setup_ui(self):
        self.header = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, height=60)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(self.header, text=self.test_data.get("title", "Тест"), **HEADER_STYLE)
        self.title_label.pack(side="left", padx=40)

        self.progress_label = ctk.CTkLabel(self.header, text="")
        self.progress_label.pack(side="right", padx=40)
        
        self.progress_bar = ctk.CTkProgressBar(self.header, width=200)
        self.progress_bar.pack(side="right", padx=20)
        self.progress_bar.set(0)
                
        self.question_container = ctk.CTkFrame(self, fg_color="transparent")
        self.question_container.pack(fill="both", expand=True, padx=50, pady=20)

        self.question_label = ctk.CTkLabel(self.question_container, text="", font=("Arial", 24, "bold"), wraplength=700)
        self.question_label.pack(pady=40)

        self.optins_container = ctk.CTkFrame(self.question_container, fg_color="transparent")
        self.optins_container.pack(fill="both", expand=True)
        
    # Метод для збереження 
    def save_current_answer(self):
        # Зберігаємо те, що ввів/вибрав користувач
        q_data = self.questions[self.current_question_index]
        if q_data["type"] == "radio":
            self.user_answers[self.current_question_index] = self.radio_var.get()
        elif q_data["type"] == "checkbox":
            selected = [cb.cget("text") for cb in self.checkbox_widgets if cb.get() == 1]
            self.user_answers[self.current_question_index] = selected
        elif q_data["type"] == "text":
            self.user_answers[self.current_question_index] = self.answer_entry.get()
        
    # Метод для показу питань
    def display_question(self):
        # Очищуємо старі віджети
        for child in self.optins_container.winfo_children():
            child.destroy()
            
        total = len(self.questions)
        if total > 0:
            self.progress_bar.set(self.current_question_index / total)
            self.progress_label.configure(text=f"{self.current_question_index + 1} / {total}")

        question_data = self.questions[self.current_question_index]
        self.question_label.configure(text=question_data["question"])
        
        if question_data["type"] == "radio":
            saved = self.user_answers.get(self.current_question_index, "")
            self.radio_var = ctk.StringVar(value=saved)
            for option in question_data["options"]:
                ctk.CTkRadioButton(self.optins_container, text=option, variable=self.radio_var, value=option).pack(pady=5, anchor="w")

        elif question_data["type"] == "checkbox":
            self.checkbox_widgets = []
            saved_answers = self.user_answers.get(self.current_question_index, [])
            for option in question_data["options"]:
                checkbox = ctk.CTkCheckBox(self.optins_container, text=option)
                if option in saved_answers:
                    checkbox.select()
                checkbox.pack(pady=5, anchor="w")
                self.checkbox_widgets.append(checkbox)

        elif question_data["type"] == "text":
            saved_text = self.user_answers.get(self.current_question_index, "")
            self.answer_entry = ctk.CTkEntry(self.optins_container, width=400, placeholder_text="Введіть відповідь...")
            self.answer_entry.insert(0, saved_text)
            self.answer_entry.pack(pady=20)

    # Метод для навігації
    def setup_navigation(self):
        self.footer = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, height=70)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.previous_question_button = ctk.CTkButton(
            self.footer, text="← Назад", command=self.previous_question, **BUTTON_STYLE
        )
        self.previous_question_button.pack(side="left", padx=40)

        self.next_question_button = ctk.CTkButton(
            self.footer, text="Далі →", command=self.next_question, **BUTTON_STYLE
        )
        self.next_question_button.pack(side="right", padx=40)
        
    # Метод для показу наступного питання
    def next_question(self):
        self.save_current_answer()
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_question()
        else:
            self.show_results()

    # Метод для показу попереднього питання
    def previous_question(self):
        if self.current_question_index > 0:
            self.save_current_answer()
            self.current_question_index -= 1
            self.display_question()

    # Метод для обчислення балу
    def calculate_score(self):
        total_score = 0
        for i, q in enumerate(self.questions):
            user_value = self.user_answers.get(i)
            stored_hash = q.get("answer")

            if user_value is None:
                continue

            if q["type"] == "checkbox":
                if isinstance(user_value, list):
                    # ПРАВКА: приводимо кожен вибраний варіант до нижнього регістру перед сортуванням
                    normalized_user = sorted([str(opt).strip().lower() for opt in user_value])
                    user_hash = get_hash("".join(normalized_user))
                    
                    if user_hash == stored_hash:
                        total_score += 1
            else:
                # Для radio та text: теж обов'язково .lower()
                user_hash = get_hash(str(user_value).strip().lower())
                if user_hash == stored_hash:
                    total_score += 1
                
        return total_score

    # Метод для показу результатів
    def show_results(self):
        # Повне очищення
        for child in self.question_container.winfo_children():
            child.destroy()
        if hasattr(self, "footer"):
            self.footer.destroy()

        total = len(self.questions)
        if total == 0: 
            return

        final_score = self.calculate_score()
        info = self.test_data.get("info", {})
        max_score = info.get("max_score", 12)
        
        # Математика результату
        score_val = (final_score / total) * max_score
        percents = (final_score / total) * 100
        
        if percents >= 90:
            result_color = "#2ecc71"; comment = "Відмінно!"
        elif percents >= 60:
            result_color = "#3498db"; comment = "Гарний результат"
        else:
            result_color = "#e74c3c"; comment = "Погано."

        self.progress_bar.set(1.0)
        
        save_history(
            test_title=self.test_data.get("info", {}).get("title", "Тест"),
            score=score_val,
            max_score=max_score,
            percentage=percents
        )

        # Вивід на екран
        ctk.CTkLabel(self.question_container, text=f"{int(score_val)} / {max_score}", 
                     font=("Arial", 60, "bold"), text_color=result_color).pack(pady=(50, 10))

        ctk.CTkLabel(self.question_container, text=f"Успішність: {percents:.1f}%", font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(self.question_container, text=comment, text_color="gray", font=("Arial", 16, "italic")).pack(pady=20)

        from main_screen import MainFrame
        ctk.CTkButton(self.question_container, text="На головне меню", **BUTTON_STYLE,
                      command=lambda: self.app_manager.switch_frame(MainFrame)).pack(pady=40)

class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color=BG_COLOR)
        self.app_manager = app_manager
        
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        self.back_button = ctk.CTkButton(
            self.header,
            command=lambda: self.app_manager.switch_frame(MainFrame),
            **BACK_BUTTON_STYLE   
        ).place(rely=0.25, relx=0.01, anchor="nw")
        
        # Заголовок сторінки
        self.label = ctk.CTkLabel(self.header, text="Історія тестувань", font=("Arial", 28, "bold"))
        self.label.pack(side="left", padx=50)

        # 1. Створюємо "Шапку" таблиці
        self.create_table_header()

        # 2. Створюємо зону з прокруткою для даних
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Налаштовуємо вагу стовпців для скрол-фрейму, щоб вони збігалися з хедером
        self.scroll_container.grid_columnconfigure(0, weight=3) # Назва (ширша)
        self.scroll_container.grid_columnconfigure(1, weight=1) # Дата
        self.scroll_container.grid_columnconfigure(2, weight=1) # Результат

        self.load_history_data()

    # Метод для створення хедера таблиці
    def create_table_header(self):
        # Фрейм для заголовків стовпців (колір трохи світліший за фон)
        header_frame = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, height=40)
        header_frame.pack(fill="x", padx=20, pady=(10, 0))
        header_frame.pack_propagate(False)

        # Налаштування сітки (grid)
        header_frame.grid_columnconfigure(0, weight=2)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)
        header_frame.grid_columnconfigure(3, weight=1)

        # Самі назви стовпців
        ctk.CTkLabel(header_frame, text="Назва тесту", font=("Arial", 14), text_color="gray").grid(row=0, column=0, sticky="w", padx=20)
        ctk.CTkLabel(header_frame, text="Дата", font=("Arial", 14), text_color="gray").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(header_frame, text="Результат", font=("Arial", 14), text_color="gray").grid(row=0, column=2, sticky="w")
        ctk.CTkLabel(header_frame, text="Відсоток", font=("Arial", 14), text_color="gray").grid(row=0, column=3, sticky="w")

    # Метод для заваниаження історії
    def load_history_data(self):
        if not os.path.exists("files/history.json"):
            ctk.CTkLabel(self.scroll_container, text="Історія порожня").pack(pady=20)
            return

        with open("files/history.json", "r", encoding="utf-8") as f:
            history = json.load(f)

        # Виводимо кожен запис як рядок таблиці
        for i, entry in enumerate(reversed(history)): # Нові результати зверху
            row_color = TABLE_SECONDARY if i % 2 == 0 else "transparent" # Зебра для зручності
            
            row_frame = ctk.CTkFrame(self.scroll_container, fg_color=row_color, height=45, corner_radius=0)
            row_frame.pack(fill="x")
            
            row_frame.grid_columnconfigure(0, weight=2)
            row_frame.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(2, weight=1)
            row_frame.grid_columnconfigure(3, weight=1)

            # Назва
            ctk.CTkLabel(row_frame, text=entry["test"], font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=20)
            # Дата
            ctk.CTkLabel(row_frame, text=entry["date"], font=("Arial", 13), text_color="gray").grid(row=0, column=1, sticky="w")
            # Результат (з виділенням кольором)
            ctk.CTkLabel(row_frame, text=entry["score"], font=("Arial", 14, "bold"), text_color="#3b8ed0").grid(row=0, column=2, sticky="w")
            # Відсоток
            ctk.CTkLabel(row_frame, text=entry["percentage"], font=("Arial", 14), text_color="gray").grid(row=0, column=3, sticky="w")
            
class ConstructorFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color=BG_COLOR)
        self.app_manager = app_manager
        self.questions_list = []

        self.setup_header()
        self.setup_footer()
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.setup_editor_panel()
        self.setup_preview_panel()
        self.update_live_preview()

    # Метод створення хедера
    def setup_header(self):
        self.header = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, height=60)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        self.back_button = ctk.CTkButton(self.header, command=lambda: self.app_manager.switch_frame(MainFrame), **BACK_BUTTON_STYLE)
        self.back_button.place(rely=0.25, relx=0.01)
        
        self.entry_title = ctk.CTkEntry(self.header, placeholder_text="Назва тесту", width=300)
        self.entry_title.pack(side="left", padx=(60, 20))
        
        self.entry_max_score = ctk.CTkEntry(self.header, placeholder_text="Максимальна кількість балів", width=200)
        self.entry_max_score.pack(side="left")
        self.entry_max_score.bind("<KeyRelease>", self.validate_int)

    # Метод створення футера
    def setup_footer(self):
        self.footer = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, height=60)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.save_button = ctk.CTkButton(self.footer, text="Зберегти тест", fg_color="#2ecc71", hover_color="#27ae60", command=self.save_test_to_file, **BUTTON_STYLE_WITHOUT_COLOR)
        self.save_button.pack(side="right", padx=40)

        self.cancel_button = ctk.CTkButton(self.footer, text="Скасувати", fg_color="#e74c3c", hover_color="#c0392b", command=lambda: self.app_manager.switch_frame(MainFrame), **BUTTON_STYLE_WITHOUT_COLOR)
        self.cancel_button.pack(side="right", padx=10)

    # Метод створення панелі зміни
    def setup_editor_panel(self):
        self.editor_panel = ctk.CTkScrollableFrame(self.main_container, fg_color=FRAME_BG_COLOR, corner_radius=10)
        self.editor_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(self.editor_panel, text="Редактор питання", font=("Arial", 20, "bold")).pack(pady=15)

        ctk.CTkLabel(self.editor_panel, text="Текст питання:").pack(anchor="w", padx=20)
        self.entry_q_text = ctk.CTkEntry(self.editor_panel, placeholder_text="Введіть питання...")
        self.entry_q_text.pack(fill="x", padx=20, pady=(0, 5))
        self.entry_q_text.bind("<KeyRelease>", lambda e: self.update_live_preview())

        ctk.CTkLabel(self.editor_panel, text="Тип:").pack(anchor="w", padx=20)
        self.type_var = ctk.StringVar(value="radio")
        self.type_menu = ctk.CTkOptionMenu(self.editor_panel, values=["radio", "checkbox", "text"], variable=self.type_var, command= self.on_type_change)
        self.type_menu.pack(fill="x", padx=20, pady=(0, 5))

        self.label_options = ctk.CTkLabel(self.editor_panel, text="Варіанти (через кому):")
        self.label_options.pack(anchor="w", padx=20)
        self.entry_options = ctk.CTkEntry(self.editor_panel, placeholder_text="Варіант 1, Варіант 2, Варіант 3")
        self.entry_options.pack(fill="x", padx=20, pady=(0, 5))
        self.entry_options.bind("<KeyRelease>", lambda e: self.update_live_preview())

        ctk.CTkLabel(self.editor_panel, text="Правильна відповідь:",).pack(anchor="w", padx=(20))
        self.entry_correct = ctk.CTkEntry(self.editor_panel, placeholder_text="Відповідь")
        self.entry_correct.pack(fill="x", padx=20, pady=(0, 5))

        self.add_btn = ctk.CTkButton(self.editor_panel, text="Додати питання", command=self.add_question_to_list, **BUTTON_STYLE)
        self.add_btn.pack(pady=20)

    # Метод створення прев'ю
    def setup_preview_panel(self):
        self.preview_panel = ctk.CTkFrame(self.main_container, fg_color=FRAME_BG_COLOR, corner_radius=10)
        self.preview_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(self.preview_panel, text="LIVE PREVIEW", font=("Arial", 12), text_color="gray").pack(pady=10)

        self.preview_question_label = ctk.CTkLabel(self.preview_panel, text="", font=("Arial", 22, "bold"), wraplength=400)
        self.preview_question_label.pack(pady=30, padx=20)

        self.preview_options_container = ctk.CTkFrame(self.preview_panel, fg_color="transparent")
        self.preview_options_container.pack(fill="both", expand=True)

    # Метод оновлення прев'ю
    def update_live_preview(self):
        for child in self.preview_options_container.winfo_children():
            child.destroy()

        q_text = self.entry_q_text.get().strip()
        q_type = self.type_var.get()
        raw_opts = self.entry_options.get()
        options = [opt.strip() for opt in raw_opts.split(",")] if raw_opts else []

        if not q_text:
            self.preview_question_label.configure(text="[Текст питання з'явиться тут]")
        else:
            self.preview_question_label.configure(text=q_text)

        if q_type == "radio":
            self.entry_correct.configure(placeholder_text="Відповідь")
            for opt in options:
                ctk.CTkRadioButton(self.preview_options_container, text=opt).pack(pady=5, anchor="w", padx=60)
        elif q_type == "checkbox":
            self.entry_correct.configure(placeholder_text="Відповідь, відповідь...")
            for opt in options:
                ctk.CTkCheckBox(self.preview_options_container, text=opt).pack(pady=5, anchor="w", padx=60)
        elif q_type == "text":
            self.entry_correct.configure(placeholder_text="Відповідь")
            entry = ctk.CTkEntry(self.preview_options_container, width=300, placeholder_text="Поле для відповіді...")
            entry.configure(state="disabled")
            entry.pack(pady=20)

    # Метод додавання питання до списку
    def add_question_to_list(self):
        q_text = self.entry_q_text.get().strip()
        q_type = self.type_var.get()
        correct = self.entry_correct.get().strip()

        if q_type == "checkbox":
            separator = ";" if ";" in correct else ","
            
            list_correct = [
                c.strip().lower().replace(',', '.') 
                for c in correct.split(separator) if c.strip()
            ]
            hashed_answer = get_hash("".join(sorted(list_correct)))
        else:
            normalized_correct = correct.lower().replace(',', '.')
            hashed_answer = get_hash(normalized_correct)

        question_data = {
            "type": q_type,
            "question": q_text,
            "options": [opt.strip() for opt in self.entry_options.get().split(",")],
            "answer": hashed_answer 
        }
        self.questions_list.append(question_data)
    
        # Очищення полів
        self.entry_q_text.delete(0, 'end')
        self.entry_options.delete(0, 'end')
        self.entry_correct.delete(0, 'end')

    # Метод збереження в файл
    def save_test_to_file(self):
        title = self.entry_title.get().strip() or "unnamed_test"
        en_max = self.entry_max_score.get()
        if en_max:
            max_score = int(en_max)
        else:
            max_score = 12
        
        full_data = {
            "info": {
                "title": title,
                "creator": "Ілля Снітко",
                "max_score": max_score
            },
            "questions": self.questions_list
        }

        if not os.path.exists("tests"):
            os.makedirs("tests")

        filename = f"tests/{title.lower().replace(' ', '_')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=4)
        
        self.app_manager.switch_frame(MainFrame)
        
    # Метод валідації цифр для ентрі максимального балу
    def validate_int(self, event):
        current_value = self.entry_max_score.get()

        if current_value=="" or current_value.isdigit():
            self.entry_max_score.configure(border_color=BORDER_COLOR)
        else:
            self.entry_max_score.configure(border_color="red")
            
    # Метод для ховання варіантів коли вибрано "текст"
    def on_type_change(self, choice):
        if choice == "text":
            self.label_options.pack_forget()
            self.entry_options.pack_forget()
        else:
            self.label_options.pack(after=self.type_menu ,anchor="w", padx=20)
            self.entry_options.pack(after=self.label_options, fill="x", padx=20, pady=(0, 5))
        
        self.update_live_preview()
                
class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color=BG_COLOR)
        self.app_manager=app_manager
        
        self.header = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, height=60)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        self.back_button = ctk.CTkButton(self.header, command=lambda: self.app_manager.switch_frame(MainFrame), **BACK_BUTTON_STYLE)
        self.back_button.place(relx=0.01, rely=0.25, anchor="nw")

        self.main_label = ctk.CTkLabel(self.header, text="Налаштування", **MAIN_LABEL_STYLE)
        self.main_label.pack(side="left", padx=60)
        
        self.theme_container = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.theme_container.pack(pady=(40, 5), padx=100)
        
        self.theme_label = ctk.CTkLabel(self.theme_container, font=("Arial", 16), text="Тема")
        self.theme_label.pack(padx=40, side="left")

        self.theme_segment_menu = ctk.CTkSegmentedButton(self.theme_container, values=["System", "Light", "Dark"], command=self.change_theme)
        self.theme_segment_menu.pack(side="right", padx=40)
        self.theme_segment_menu.set(ctk.get_appearance_mode())
        
        self.log_out_button = ctk.CTkButton(self, text="Вийти з акаунта", command=self.log_out, **BUTTON_STYLE)
        self.log_out_button.pack(pady=40)
        
        self.footer = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=FRAME_BG_COLOR)
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        self.footer_label = ctk.CTkLabel(self.footer, text="Курсова робота | Снітко Ілля | Версія 1.0", text_color=TEXT_SECONDARY, font=("Arial", 16))
        self.footer_label.pack(side="left", padx=20)
        
        self.restart_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 24, "bold"))
        self.restart_label.pack(side="bottom", pady=40)
        
    def log_out(self):
        from login_screen import LoginFrame
        self.app_manager.switch_frame(LoginFrame)

        data = get_data("files/settings.json")

        data["isLogged"] = False
        data["userName"] = ""

        with open("files/settings.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

        data= get_data("files/settings.json")
        data["theme"] = new_theme

        with open("files/settings.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)