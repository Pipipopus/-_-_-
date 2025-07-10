import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import subprocess


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Распознавание текста")
        self.root.geometry("700x500")

        self.tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if not os.path.exists(self.tesseract_path):
            messagebox.showerror("Ошибка", "Tesseract OCR не установлен!")
            self.root.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        # Выбор файла
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Изображение:").pack(side=tk.LEFT)
        self.file_entry = tk.Entry(frame, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="Обзор", command=self.browse_file).pack(side=tk.LEFT)

        # Кнопка распознавания
        tk.Button(self.root, text="Распознать текст", command=self.run_ocr).pack(pady=5)

        # Вывод результата
        self.output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.output.pack(pady=10, padx=10)

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if filepath:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filepath)

    def run_ocr(self):
        image_path = self.file_entry.get()
        if not image_path:
            messagebox.showerror("Ошибка", "Выберите файл изображения!")
            return

        if not os.path.exists(image_path):
            messagebox.showerror("Ошибка", "Файл не существует!")
            return

        try:
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "Идёт распознавание...")
            self.root.update()

            # Используем subprocess для вызова tesseract
            result = subprocess.run(
                [self.tesseract_path, image_path, 'stdout', '-l', 'rus+eng'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                self.output.delete(1.0, tk.END)
                self.output.insert(tk.END, result.stdout)
            else:
                messagebox.showerror("Ошибка", result.stderr)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()