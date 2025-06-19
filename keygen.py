#It has no comments because even I don’t understand how this managed to work.
#No tiene comentarios porque ni yo entiendo como esto logró funcionar.

import tkinter as tk
from tkinter import messagebox
import random, string, json, os, sys
import pyperclip
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

DATA_FILE = 'password_data.json'
PREFS_FILE = 'preferences.json'
MAX_NAME_LENGTH = 20

with open('languages.json', 'r', encoding='utf-8') as f:
    LANGUAGES = json.load(f)

preferences = {}
current_lang = 'en'
current_theme = 'light'
current_use_special_chars = False

def load_preferences():
    global preferences, current_lang, current_theme, current_use_special_chars
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, 'r', encoding='utf-8') as f:
                preferences = json.load(f)
            current_lang = preferences.get('language', 'en')
            current_theme = preferences.get('theme', 'light')
            current_use_special_chars = preferences.get('use_special_chars', False)
        except Exception:
            preferences = {}
    else:
        preferences = {}

def save_preferences():
    global preferences
    try:
        with open(PREFS_FILE, 'w', encoding='utf-8') as f:
            json.dump(preferences, f)
    except Exception:
        pass

load_preferences()

def set_icon(window):
    try:
        window.iconbitmap('images/key_icon.ico')
    except Exception:
        pass

def get_theme_colors(theme):
    if theme == 'dark':
        return '#1e1e1e', '#ffffff'
    else:
        return '#f0f2f5', '#000000'

class LoginDialog:
    def __init__(self, master, username=None, first_time=False):
        global current_lang, current_theme
        self.dialog = tk.Toplevel(master)
        self.username = username
        self.first_time = first_time
        self.result = None

        self.bg_color, self.fg_color = get_theme_colors(current_theme)

        self.dialog.title(LANGUAGES[current_lang]['config_title'] if first_time else LANGUAGES[current_lang]['login_title'])
        self.dialog.geometry("300x160")
        self.dialog.resizable(False, False)
        set_icon(self.dialog)
        self.dialog.configure(bg=self.bg_color)
        self.dialog.bind('<Return>', lambda event: self.submit())

        frame = tk.Frame(self.dialog, padx=10, pady=10, bg=self.bg_color)
        frame.pack(fill='both', expand=True)

        if first_time:
            tk.Label(frame, text=LANGUAGES[current_lang]['login_user_label'], bg=self.bg_color, fg=self.fg_color).pack(anchor='w')
            self.user_entry = tk.Entry(frame)
            self.user_entry.pack(fill='x', pady=5)
        else:
            tk.Label(frame, text=f"{LANGUAGES[current_lang]['login_user_label']}: {username}", bg=self.bg_color, fg=self.fg_color).pack(anchor='center', pady=10)
            self.user_entry = None

        tk.Label(frame, text=LANGUAGES[current_lang]['login_pass_label'], bg=self.bg_color, fg=self.fg_color).pack(anchor='w')
        self.password_entry = tk.Entry(frame, show='*')
        self.password_entry.pack(fill='x', pady=5)

        action_text = LANGUAGES[current_lang]['create_account_btn'] if first_time else LANGUAGES[current_lang]['login_btn']
        btn = tk.Button(frame, text=action_text, command=self.submit, bg=self.bg_color, fg=self.fg_color)
        btn.pack(pady=10)

        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        self.dialog.grab_set()
        self.dialog.wait_window()

    def submit(self):
        user = self.user_entry.get().strip() if self.first_time else self.username
        password = self.password_entry.get()
        if self.first_time and not user:
            messagebox.showwarning(LANGUAGES[current_lang]['error'], LANGUAGES[current_lang]['user_required'], parent=self.dialog)
            return
        if not password:
            messagebox.showwarning(LANGUAGES[current_lang]['error'], LANGUAGES[current_lang]['pass_required'], parent=self.dialog)
            return
        self.result = (user, password)
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()
        sys.exit()

class PasswordManagerApp:
    def __init__(self, root, fernet, username):
        global current_lang, current_theme, current_use_special_chars, preferences

        self.root = root
        self.fernet = fernet
        self.username = username
        self.language = current_lang
        self.theme = current_theme
        self.use_special_chars = current_use_special_chars

        self.bg_color, self.fg_color = get_theme_colors(self.theme)
        self.root.title(f"{LANGUAGES[self.language]['app_title']} - {username}")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        set_icon(self.root)
        self.root.configure(bg=self.bg_color)

        self.current_password = tk.StringVar()
        self.saved_passwords = []

        self.load_passwords()
        self.build_interface()
        self.generate_password()

    def build_interface(self):
        global current_lang, current_theme, current_use_special_chars

        self.bg_color, self.fg_color = get_theme_colors(self.theme)
        self.root.configure(bg=self.bg_color)

        topbar = tk.Frame(self.root, bg=self.bg_color)
        topbar.pack(fill='x', anchor='n', pady=(5, 0))

        self.lang_btn = tk.Menubutton(topbar, text=LANGUAGES[self.language]['language_button'], relief='raised', bg=self.bg_color, fg=self.fg_color)
        self.lang_menu = tk.Menu(self.lang_btn, tearoff=0)
        self.lang_btn.config(menu=self.lang_menu)
        self.lang_btn.pack(side='left', padx=10)

        language_names = LANGUAGES[self.language]['language_names']
        for code, name in language_names.items():
            self.lang_menu.add_command(label=name, command=lambda c=code: self.change_language(c))

        tk.Button(topbar, text=LANGUAGES[self.language]['toggle_theme_btn'], command=self.toggle_theme,
                  bg=self.bg_color, fg=self.fg_color).pack(side='right', padx=10)

        special_btn_text = LANGUAGES[self.language]['special_chars_off'] if self.use_special_chars else LANGUAGES[self.language]['special_chars_on']
        self.special_chars_btn = tk.Button(topbar, text=special_btn_text, command=self.toggle_special_chars,
                                           bg=self.bg_color, fg=self.fg_color)
        self.special_chars_btn.pack(side='right')

        title = tk.Label(self.root, text=LANGUAGES[self.language]['app_main_title'], font=('Arial', 20, 'bold'),
                         bg=self.bg_color, fg=self.fg_color)
        title.pack(pady=10)

        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(pady=5, fill='x')

        center_top = tk.Frame(top_frame, bg=self.bg_color)
        center_top.pack(anchor='center')

        tk.Label(center_top, text=LANGUAGES[self.language]['generated_password_label'], bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, columnspan=3, sticky='n', pady=(0, 5))
        self.pass_entry = tk.Entry(center_top, textvariable=self.current_password, state='readonly', width=40,
                                   justify='center', font=('Arial', 12))
        self.pass_entry.grid(row=1, column=0, padx=5)
        tk.Button(center_top, text=LANGUAGES[self.language]['generate_btn'], command=self.generate_password,
                  bg=self.bg_color, fg=self.fg_color).grid(row=1, column=1, padx=5)
        tk.Button(center_top, text=LANGUAGES[self.language]['copy_btn'], command=self.copy_current,
                  bg=self.bg_color, fg=self.fg_color).grid(row=1, column=2)

        save_frame = tk.Frame(self.root, bg=self.bg_color)
        save_frame.pack(pady=10, fill='x')

        center_save = tk.Frame(save_frame, bg=self.bg_color)
        center_save.pack(anchor='center')

        tk.Label(center_save, text=LANGUAGES[self.language]['save_name_label'], bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.name_entry = tk.Entry(center_save, width=30, justify='center', font=('Arial', 12))
        self.name_entry.grid(row=1, column=0, padx=5)
        tk.Button(center_save, text=LANGUAGES[self.language]['save_btn'], command=self.save_password,
                  bg=self.bg_color, fg=self.fg_color).grid(row=1, column=1)

        tk.Label(self.root, text=LANGUAGES[self.language]['saved_passwords_label'], font=('Arial', 16, 'bold'),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(fill='both', expand=True, padx=20)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Consolas', 12),
                                  bg=self.bg_color, fg=self.fg_color, selectbackground='#6a99f9' if self.theme == 'light' else '#4a6fff')
        self.listbox.pack(side='left', fill='both', expand=True, padx=(10, 0))
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<Button-3>', self.show_context_menu)

        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=10, fill='x', padx=20)
        tk.Button(btn_frame, text=LANGUAGES[self.language]['delete_selected_btn'], command=self.delete_selected,
                  bg=self.bg_color, fg=self.fg_color).pack(side='left', padx=5)
        tk.Button(btn_frame, text=LANGUAGES[self.language]['copy_selected_btn'], command=self.copy_selected,
                  bg=self.bg_color, fg=self.fg_color).pack(side='left', padx=5)
        tk.Button(btn_frame, text=LANGUAGES[self.language]['delete_account_btn'], command=self.delete_account,
                  bg=self.bg_color, fg=self.fg_color).pack(side='right', padx=5)

        self.name_entry.bind('<Return>', lambda e: self.save_password())
        self.pass_entry.bind('<Return>', lambda e: self.generate_password())

        self.refresh_list()

    def change_language(self, new_lang):
        global current_lang, preferences
        current_lang = new_lang
        preferences['language'] = new_lang
        save_preferences()
        self.language = new_lang
        self.clear_ui()
        self.build_interface()

    def toggle_theme(self):
        global current_theme, preferences
        current_theme = 'dark' if current_theme == 'light' else 'light'
        preferences['theme'] = current_theme
        save_preferences()
        self.theme = current_theme
        self.clear_ui()
        self.build_interface()

    def toggle_special_chars(self):
        global current_use_special_chars, preferences
        current_use_special_chars = not current_use_special_chars
        preferences['use_special_chars'] = current_use_special_chars
        save_preferences()
        self.use_special_chars = current_use_special_chars
        if self.use_special_chars:
            self.special_chars_btn.config(text=LANGUAGES[self.language]['special_chars_off'])
        else:
            self.special_chars_btn.config(text=LANGUAGES[self.language]['special_chars_on'])
        self.generate_password()

    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_password(self):
        base_chars = string.ascii_letters + string.digits
        special_chars = '#@!?%&-_'
        length = 16

        if self.use_special_chars:
            pwd_chars = [random.choice(special_chars) for _ in range(random.randint(1, 4))]
            pwd_chars += [random.choice(base_chars + special_chars) for _ in range(length - len(pwd_chars))]
            random.shuffle(pwd_chars)
            password = ''.join(pwd_chars)
        else:
            password = ''.join(random.choice(base_chars) for _ in range(length))

        self.current_password.set(password)

    def copy_current(self):
        pyperclip.copy(self.current_password.get())
        messagebox.showinfo(LANGUAGES[self.language]['copied_title'], LANGUAGES[self.language]['copied_message'])

    def save_password(self):
        name = self.name_entry.get().strip()
        password = self.current_password.get()
        if not name:
            return messagebox.showwarning(LANGUAGES[self.language]['error'], LANGUAGES[self.language]['name_required'])
        if len(name) > MAX_NAME_LENGTH:
            return messagebox.showwarning(LANGUAGES[self.language]['error'], LANGUAGES[self.language]['name_too_long'].format(MAX_NAME_LENGTH))
        self.saved_passwords.append((name, password))
        self.name_entry.delete(0, 'end')
        self.refresh_list()
        self.save_to_file()
        messagebox.showinfo(LANGUAGES[self.language]['saved_title'], LANGUAGES[self.language]['saved_message'])

    def delete_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            return messagebox.showwarning(LANGUAGES[self.language]['error'], LANGUAGES[self.language]['select_to_delete'])
        del self.saved_passwords[selected[0]]
        self.refresh_list()
        self.save_to_file()
        messagebox.showinfo(LANGUAGES[self.language]['deleted_title'], LANGUAGES[self.language]['deleted_message'])

    def copy_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            return messagebox.showwarning(LANGUAGES[self.language]['error'], LANGUAGES[self.language]['select_to_copy'])
        content = self.listbox.get(selected[0]).split(': ', 1)[1]
        pyperclip.copy(content)
        messagebox.showinfo(LANGUAGES[self.language]['copied_title'], LANGUAGES[self.language]['copied_message'])

    def show_context_menu(self, event):
        index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(index)
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=LANGUAGES[self.language]['copy_btn'], command=self.copy_selected)
        menu.add_command(label=LANGUAGES[self.language]['delete_selected_btn'], command=self.delete_selected)
        menu.tk_popup(event.x_root, event.y_root)
        menu.grab_release()

    def refresh_list(self):
        self.listbox.delete(0, 'end')
        for name, password in self.saved_passwords:
            self.listbox.insert('end', f"  {name}: {password}")

    def delete_account(self):
        if messagebox.askyesno(LANGUAGES[self.language]['confirm'], LANGUAGES[self.language]['delete_account_confirm']):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            if os.path.exists(PREFS_FILE):
                os.remove(PREFS_FILE)
            messagebox.showinfo(LANGUAGES[self.language]['deleted_title'], LANGUAGES[self.language]['account_deleted'])
            self.root.destroy()
            sys.exit()

    def save_to_file(self):
        data = {'username': self.username, 'salt': self.salt.hex(), 'passwords': []}
        for name, password in self.saved_passwords:
            token = self.fernet.encrypt(password.encode()).decode()
            data['passwords'].append({'name': name, 'pwd': token})
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)

    def load_passwords(self):
        if not os.path.exists(DATA_FILE):
            self.salt = os.urandom(16)
            return
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        self.salt = bytes.fromhex(data['salt'])
        for entry in data.get('passwords', []):
            password = self.fernet.decrypt(entry['pwd'].encode()).decode()
            self.saved_passwords.append((entry['name'], password))


def get_fernet(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    if not os.path.exists(DATA_FILE):
        login = LoginDialog(root, first_time=True)
        if login.result is None:
            sys.exit()
        username, password = login.result
        salt = os.urandom(16)
        fernet = get_fernet(password, salt)
        with open(DATA_FILE, 'w') as f:
            json.dump({'username': username, 'salt': salt.hex(), 'passwords': []}, f)
    else:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        username = data['username']
        salt = bytes.fromhex(data['salt'])

        login = LoginDialog(root, username=username)
        if login.result is None:
            sys.exit()
        _, password = login.result

        fernet = get_fernet(password, salt)
        try:
            if data.get('passwords'):
                fernet.decrypt(data['passwords'][0]['pwd'].encode())
        except Exception:
            messagebox.showerror(LANGUAGES[current_lang]['error'], LANGUAGES[current_lang]['wrong_password'])
            sys.exit()

    root.deiconify()
    PasswordManagerApp(root, fernet, username)
    root.mainloop()
