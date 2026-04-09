import customtkinter as ctk
import os, json
from all_styles import MAIN_LABEL_STYLE, SECTION_LABEL_STYLE, FRAME_BG_COLOR, BACK_BUTTON_STYLE, BUTTON_STYLE, HEADER_STYLE
from login import get_data
from main import get_test_files, get_test_metadata, save_history

settings_data = get_data("files/settings.json")

# Це буде фрейм для гловного екрану
class MainFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent")
        
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
            self.btn_click,
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
            self.btn_click,
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
        super().__init__(master, fg_color="transparent")
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
            list_chunk = ctk.CTkFrame(self.container, height=80, corner_radius=20, fg_color="#1c1c1c")
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
        super().__init__(master, fg_color="transparent")
        self.app_manager = app_manager
        self.test_file = test_file
        
        # 1. Створюємо словник для відповідей (КРИТИЧНО)
        self.user_answers = {}
        
        self.test_data = self.load_test_data()
        self.questions = self.test_data.get("questions", [])
        self.current_question_index = 0
        
        # 2. Запускаємо UI та Навігацію
        self.setup_ui()
        self.setup_navigation()
        self.display_question()
    
    def load_test_data(self):
        path = os.path.join("tests", self.test_file)
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

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
        
    def next_question(self):
        self.save_current_answer()
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_question()
        else:
            self.show_results()

    def previous_question(self):
        if self.current_question_index > 0:
            self.save_current_answer()
            self.current_question_index -= 1
            self.display_question()

    def calculate_score(self):
        total_score = 0
        for i, q in enumerate(self.questions):
            user_value = self.user_answers.get(i)
            correct_value = q.get("answer")

            if user_value is None: continue

            if q["type"] == "checkbox":
                if isinstance(user_value, list) and sorted(user_value) == sorted(correct_value):
                    total_score += 1
            elif str(user_value).strip().lower() == str(correct_value).strip().lower():
                total_score += 1
        return total_score
    
    def show_results(self):
        # 1. Повне очищення
        for child in self.question_container.winfo_children():
            child.destroy()
        if hasattr(self, "footer"):
            self.footer.destroy()

        total = len(self.questions)
        if total == 0: return

        final_score = self.calculate_score()
        info = self.test_data.get("info", {})
        max_score = info.get("max_score", 12)
        
        # 2. Математика результату
        score_val = (final_score / total) * max_score
        percents = (final_score / total) * 100
        
        if percents >= 90:
            result_color = "#2ecc71"; comment = "Відмінно! Справжній Arch-майстер."
        elif percents >= 60:
            result_color = "#3498db"; comment = "Гарний результат"
        else:
            result_color = "#e74c3c"; comment = "Погано. Треба більше практики."

        self.progress_bar.set(1.0)
        
        save_history(
            test_title=self.test_data.get("info", {}).get("title", "Тест"),
            score=score_val,
            max_score=max_score,
            percentage=percents
        )

        # 3. Вивід на екран
        ctk.CTkLabel(self.question_container, text=f"{int(score_val)} / {max_score}", 
                     font=("Arial", 60, "bold"), text_color=result_color).pack(pady=(50, 10))

        ctk.CTkLabel(self.question_container, text=f"Успішність: {percents:.1f}%", font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(self.question_container, text=comment, text_color="gray", font=("Arial", 16, "italic")).pack(pady=20)

        from main_screen import MainFrame
        ctk.CTkButton(self.question_container, text="На головне меню", **BUTTON_STYLE,
                      command=lambda: self.app_manager.switch_frame(MainFrame)).pack(pady=40)

class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color="transparent")
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

    def create_table_header(self):
        # Фрейм для заголовків стовпців (колір трохи світліший за фон)
        header_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", height=40)
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

    def load_history_data(self):
        if not os.path.exists("files/history.json"):
            ctk.CTkLabel(self.scroll_container, text="Історія порожня").pack(pady=20)
            return

        with open("files/history.json", "r", encoding="utf-8") as f:
            history = json.load(f)

        # Виводимо кожен запис як рядок таблиці
        for i, entry in enumerate(reversed(history)): # Нові результати зверху
            row_color = "#1c1c1c" if i % 2 == 0 else "transparent" # Зебра для зручності
            
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