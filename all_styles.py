BG_COLOR = ("#F0F2F5", "#101010")# Головне вікно (світло-сірий / майже чорний)
FRAME_BG_COLOR = ("#FFFFFF", "#1B1B1B") # Картки та фрейми (чистий білий / темно-сірий)
ACCENT_COLOR = ("#3B8ED0", "#1F6AA5") # Акцентний синій (насичений / приглушений)
TEXT_COLOR = ("#1A1A1A", "#FFFFFF") # Основний текст (майже чорний / білий)
TEXT_SECONDARY = ("#606060", "#AAAAAA") # Другорядний текст (темно-сірий / світло-сірий)
BORDER_COLOR = ("#DBDBDB", "#2B2B2B") # Колір ліній та розділювачів
BACK_BTN_COLOR = ("#E5E5E5", "#333333") # Світлий / Темний фон
BACK_BTN_HOVER = ("#D1D1D1", "#444444") # Колір при наведенні
BACK_BTN_TEXT = ("#1A1A1A", "#FFFFFF") # Чорний / Білий текст
TABLE_SECONDARY = ("#DBDBDB", "#2B2B2B") # Другий колір для таблиці історії

# 
HEADER_STYLE = {
    "font": ("Arial", 32, "bold"),
    "text_color": TEXT_COLOR,
    "anchor": "w"
}

SECTION_LABEL_STYLE = {
    "font": ("Arial", 14, "bold"),
    "text_color": ACCENT_COLOR,
    "anchor": "w"
}

ENTRY_LABEL_STYLE = {
    "width": 300,
    "font": ("CtkFont", 10),
    "anchor": "w"
}

ENTRY_STYLE = {
    "width": 300
}

MAIN_LABEL_STYLE = {
    "font": ("Ctkfont", 32, "bold")
}

BUTTON_STYLE = {
    "width": 160,
    "height": 40,
    "corner_radius": 20,
    "font": ("Arial", 14, "bold"),
    "fg_color": ACCENT_COLOR,
    "hover_color": "#14507A" # Темніший синій при наведенні
}

BACK_BUTTON_STYLE = {
    "width": 30,
    "fg_color": BACK_BTN_COLOR,
    "text_color": BACK_BTN_TEXT,
    "hover_color": BACK_BTN_HOVER,
    "text": "<"
}

BUTTON_STYLE_WITHOUT_COLOR = {
    "width": 160,
    "height": 40,
    "corner_radius": 20,
    "font": ("Arial", 14, "bold"),
}