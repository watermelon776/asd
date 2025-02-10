import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from github import Github

class GitHubUploader:
    def __init__(self, master):
        self.master = master
        self.master.title("Загружатор Инатор 2300")

        self.token = None
        self.github = None
        self.repos = []

        self.auth_button = tk.Button(master, text="Авторизоваться в GitHub", command=self.authenticate)
        self.auth_button.pack(pady=10)

        self.upload_button = tk.Button(master, text="Загрузить файл", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.select_code_button = tk.Button(master, text="Создать файл из выделенного текста", command=self.create_file_from_selection)
        self.select_code_button.pack(pady=10)

        self.repo_button = tk.Button(master, text="Показать доступные репозитории", command=self.show_repositories)
        self.repo_button.pack(pady=10)

    def authenticate(self):
        self.token = simpledialog.askstring("Token", "Введите ваш GitHub токен:")
        if self.token:
            try:
                self.github = Github(self.token)
                self.github.get_user()  # Проверка токена
                self.repos = self.get_repositories()
                messagebox.showinfo("Успех", "Вы успешно авторизовались!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось авторизоваться: {str(e)}")

    def get_repositories(self):
        """Получение списка доступных репозиториев пользователя."""
        user = self.github.get_user()
        return user.get_repos()

    def show_repositories(self):
        """Отображение доступных репозиториев в сообщении."""
        if not self.repos:
            messagebox.showwarning("Предупреждение", "Сначала авторизуйтесь в GitHub!")
            return

        repo_names = [repo.name for repo in self.repos]
        messagebox.showinfo("Доступные репозитории", "\n".join(repo_names))

    def upload_file(self):
        if not self.github:
            messagebox.showerror("Ошибка", "Сначала авторизуйтесь в GitHub!")
            return

        file_path = filedialog.askopenfilename()
        if file_path:
            repo_name = simpledialog.askstring("Репозиторий", "Введите имя репозитория (например, username/repo):")
            if repo_name:
                try:
                    repo = self.github.get_repo(repo_name)
                    with open(file_path, "rb") as file:
                        content = file.read()
                        file_name = file_path.split("/")[-1]
                        repo.create_file(file_name, "Добавление файла", content)
                        messagebox.showinfo("Успех", f"Файл {file_name} успешно загружен в {repo_name}!")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def create_file_from_selection(self):
        if not self.github:
            messagebox.showerror("Ошибка", "Сначала авторизуйтесь в GitHub!")
            return

        text = "Это пример выделенного текста."  # Замените на выделенный текст
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_name:
            repo_name = simpledialog.askstring("Репозиторий", "Введите имя репозитория (например, username/repo):")
            if repo_name:
                try:
                    repo = self.github.get_repo(repo_name)
                    repo.create_file(file_name.split("/")[-1], "Создание файла из выделенного текста", text)
                    messagebox.showinfo("Успех", f"Файл {file_name} успешно загружен в {repo_name}!")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось создать файл: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUploader(root)
    root.mainloop()