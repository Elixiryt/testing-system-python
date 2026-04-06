BG_COLOR = "#101010"          # Найтемніший фон (головне вікно)
FRAME_BG_COLOR = "#1B1B1B"   # Трохи світліший фон для карток/фреймів
ACCENT_COLOR = "#1F6AA5"     # Основний синій колір для кнопок
TEXT_COLOR = "#FFFFFF"       # Білий текст
TEXT_SECONDARY = "#AAAAAA"   # Cірий текст для довідкової інформації

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
    "fg_color": "transparent",
    "text": "<"
}