import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ------------------- ОКНО -------------------

win = ctk.CTk()
win.title("Умные заметки")
win.geometry("900x600")

notes = {}
current_note = None

# ------------------- ЛЕВАЯ ЧАСТЬ (ТЕКСТ) -------------------

text_field = ctk.CTkTextbox(win, width=500)
text_field.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# ------------------- ПРАВАЯ ЧАСТЬ -------------------

right_frame = ctk.CTkFrame(win, width=300)
right_frame.pack(side="right", fill="y", padx=10, pady=10)

label_notes = ctk.CTkLabel(right_frame, text="Список заметок")
label_notes.pack(pady=(10, 5))

notes_list_frame = ctk.CTkScrollableFrame(right_frame, width=250, height=400)
notes_list_frame.pack(fill="both", expand=True)

note_buttons = {}

# ------------------- ФУНКЦИИ -------------------

def refresh_notes_list():
    """Обновление списка заметок на панели."""
    for widget in notes_list_frame.winfo_children():
        widget.destroy()

    note_buttons.clear()

    for name in notes.keys():
        btn = ctk.CTkButton(
            notes_list_frame,
            text=name,
            anchor="w",
            command=lambda n=name: show_note(n)
        )
        btn.pack(fill="x", pady=2)
        note_buttons[name] = btn

def vspliv(text, rod):
    app1 = ctk.CTkToplevel(rod)
    app1.geometry('300x150')
    app1.title('ошибка!')
    app1.transient(win)     # Привязка к родителю
    app1.lift()             # Поднимаем наверх
    app1.focus_force()
    label = ctk.CTkLabel(master=app1, text=text)
    btn = ctk.CTkButton(master=app1, text='OK', command=lambda: app1.destroy())
    label.pack(pady=10)
    btn.pack(pady=15)

def add_note():
    """Создать новую заметку."""
    global notes
    app1 = ctk.CTkToplevel(win)
    app1.geometry('300x150')
    app1.title('Создать заметку')
    app1.transient(win)     # Привязка к родителю
    app1.lift()             # Поднимаем наверх
    app1.focus_force()      # Передаём фокус
    entry1 = ctk.CTkEntry(master=app1, width=280, height=30, placeholder_text='введите название...')
    btn = ctk.CTkButton(master=app1, text='создать', command=lambda: dat(entry1, app1))
    entry1.pack(pady=10)
    btn.pack(pady=10)

def dat(entry1, app):
    name = entry1.get()
    if name != '':
        notes[name] = {"текст": "", "теги": []}
        refresh_notes_list()
        app.destroy()
    else:
        vspliv('Введите название!', app)


def show_note(name):
    """Показать выбранную заметку."""
    global current_note
    current_note = name

    text_field.delete("0.0", "end")
    text_field.insert("0.0", notes[name]["текст"])


def save_note():
    """Сохранить содержимое заметки."""
    if not current_note:
        vspliv("Выберите заметку!", win)
        return

    notes[current_note]["текст"] = text_field.get("0.0", "end").strip()

    with open("notes_data.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)


def del_note():
    """Удалить заметку."""
    global current_note

    if not current_note:
        vspliv("Выберите заметку!", win)
        return

    del notes[current_note]
    current_note = None

    text_field.delete("0.0", "end")
    refresh_notes_list()

    with open("notes_data.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)


# ------------------- КНОПКИ -------------------

buttons_frame = ctk.CTkFrame(right_frame)
buttons_frame.pack(fill="x", pady=10)

btn_add = ctk.CTkButton(buttons_frame, text="Создать заметку", command=add_note)
btn_add.pack(fill="x", pady=3)

btn_del = ctk.CTkButton(buttons_frame, text="Удалить заметку", command=del_note)
btn_del.pack(fill="x", pady=3)

btn_save = ctk.CTkButton(buttons_frame, text="Сохранить заметку", command=save_note)
btn_save.pack(fill="x", pady=3)

# ------------------- ЗАГРУЗКА ДАННЫХ -------------------

if os.path.exists("notes_data.json"):
    with open("notes_data.json", "r", encoding="utf-8") as f:
        notes = json.load(f)

refresh_notes_list()

# ------------------- ЗАПУСК -------------------

win.mainloop()
