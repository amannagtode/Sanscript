import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from anuvada.ShastraAnuvadaYantra import ShastraAnuvadaYantra
import json

class ShastraAnuvadaYantraGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shastra Anuvada Yantra")
        self.create_widgets()
        self.translator = ShastraAnuvadaYantra("src/modules/maya/config.json")
        self.dark_mode = False

    def create_widgets(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save Project", command=self.save_project)
        self.file_menu.add_command(label="Load Project", command=self.load_project)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)

        self.view_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Documentation", command=self.show_documentation)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.sanskrit_text_label = tk.Label(self.root, text="Sanskrit Text")
        self.sanskrit_text_label.pack()

        self.sanskrit_text = tk.Text(self.root, height=10, width=50)
        self.sanskrit_text.pack()

        self.target_language_label = tk.Label(self.root, text="Target Language")
        self.target_language_label.pack()

        self.target_language = tk.StringVar(self.root)
        self.target_language.set("en")
        self.target_language_menu = tk.OptionMenu(self.root, self.target_language, "en", "fr", "de", "es")
        self.target_language_menu.pack()

        self.translation_style_label = tk.Label(self.root, text="Translation Style")
        self.translation_style_label.pack()

        self.translation_style = tk.StringVar(self.root)
        self.translation_style.set("literal")
        self.translation_style_menu = tk.OptionMenu(self.root, self.translation_style, "literal", "interpretive", "devotional")
        self.translation_style_menu.pack()

        self.translate_button = tk.Button(self.root, text="Translate", command=self.translate)
        self.translate_button.pack()

        self.translated_text_label = tk.Label(self.root, text="Translated Text")
        self.translated_text_label.pack()

        self.translated_text = tk.Text(self.root, height=10, width=50)
        self.translated_text.pack()

        self.export_button = tk.Button(self.root, text="Export", command=self.export_translation)
        self.export_button.pack()

        self.synthesize_button = tk.Button(self.root, text="Synthesize Voice", command=self.synthesize_voice)
        self.synthesize_button.pack()

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progress.pack()

    def translate(self):
        sanskrit_text = self.sanskrit_text.get("1.0", tk.END).strip()
        target_language = self.target_language.get()
        translation_style = self.translation_style.get()

        if not sanskrit_text:
            messagebox.showerror("Error", "Please enter Sanskrit text.")
            return

        try:
            self.progress.start()
            translated_text = self.translator.translate_scripture(sanskrit_text, target_language, translation_style)
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert(tk.END, translated_text)
            self.progress.stop()
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", str(e))

    def export_translation(self):
        translated_text = self.translated_text.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showerror("Error", "No translated text to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            try:
                self.translator.export_translation(translated_text, "PDF")
                messagebox.showinfo("Success", f"Translation exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def synthesize_voice(self):
        translated_text = self.translated_text.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showerror("Error", "No translated text to synthesize.")
            return

        try:
            voice_file_path = self.translator.synthesize_voice(translated_text, self.target_language.get())
            messagebox.showinfo("Success", f"Voice synthesized and saved to {voice_file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_project(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            project_data = {
                "sanskrit_text": self.sanskrit_text.get("1.0", tk.END).strip(),
                "translated_text": self.translated_text.get("1.0", tk.END).strip(),
                "target_language": self.target_language.get(),
                "translation_style": self.translation_style.get()
            }
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(project_data, file)
            messagebox.showinfo("Success", f"Project saved to {file_path}")

    def load_project(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                project_data = json.load(file)
                self.sanskrit_text.delete("1.0", tk.END)
                self.sanskrit_text.insert(tk.END, project_data.get("sanskrit_text", ""))
                self.translated_text.delete("1.0", tk.END)
                self.translated_text.insert(tk.END, project_data.get("translated_text", ""))
                self.target_language.set(project_data.get("target_language", "en"))
                self.translation_style.set(project_data.get("translation_style", "literal"))
            messagebox.showinfo("Success", f"Project loaded from {file_path}")

    def undo(self):
        try:
            self.translated_text.edit_undo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def redo(self):
        try:
            self.translated_text.edit_redo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.root.tk.call("ttk::style", "theme", "use", "default")
            self.dark_mode = False
        else:
            self.root.tk.call("ttk::style", "theme", "use", "clam")
            self.dark_mode = True

    def show_documentation(self):
        messagebox.showinfo("Documentation", "This is the documentation for Shastra Anuvada Yantra.")

    def show_about(self):
        messagebox.showinfo("About", "Shastra Anuvada Yantra\nVersion 1.0\nDeveloped by [Your Name]")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShastraAnuvadaYantraGUI()
    app.run()
