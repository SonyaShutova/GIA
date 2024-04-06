import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация")
        self.root.geometry("300x200")
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)
        self.table = None

        self.frame.pack(expand=True)

        self.label_username = tk.Label(self.frame, text="Имя пользователя", font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.label_username.pack()
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack()

        self.label_password = tk.Label(self.frame, text="Пароль", font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.label_password.pack()
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.pack()

        self.login_button = tk.Button(self.frame, text="Войти", command=self.authenticate_user, width=10, height=2, font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.login_button.pack()

        self.frame.place(relx=0.5, rely=0.5, anchor="center")


    def authenticate_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            role = user[5]
            if role == "Официант":
                self.root.withdraw()
                waiter_window = WaiterWindow(tk.Toplevel(self.root), role)
            elif role == "Повар":
                self.root.withdraw()
                cook_window = CookWindow(tk.Toplevel(self.root), role)
            else:
                self.root.withdraw()
                admin_panel = AdminPanel(tk.Toplevel(self.root), role)
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль")

class AddEmployeeWindow:
    def __init__(self, root, table):
        self.root = root
        self.root.title("Добавить сотрудника")
        self.root.geometry("500x400")

        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        self.label_firstname = tk.Label(self.frame, text="Имя", font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.label_firstname.grid(row=0, column=0)
        self.entry_firstname = tk.Entry(self.frame)
        self.entry_firstname.grid(row=0, column=1)

        self.label_lastname = tk.Label(self.frame, text="Фамилия", font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.label_lastname.grid(row=1, column=0)
        self.entry_lastname = tk.Entry(self.frame)
        self.entry_lastname.grid(row=1, column=1)

        self.label_username = tk.Label(self.frame, text="Учетная запись", font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.label_username.grid(row=2, column=0)
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=2, column=1)

        self.label_password = tk.Label(self.frame, text="Пароль", font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.label_password.grid(row=3, column=0)
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=3, column=1)

        self.label_role = tk.Label(self.frame, text="Роль", font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.label_role.grid(row=4, column=0)
        self.role_var = tk.StringVar()
        self.role_var.set("Администратор")
        self.role_option = tk.OptionMenu(self.frame, self.role_var, "Администратор", "Официант", "Повар")
        self.role_option.grid(row=4, column=1)

        self.save_button = tk.Button(self.frame, text="Сохранить", command=self.save_employee, width=10, height=2, font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.save_button.grid(row=5, columnspan=2, pady=10)

        self.table = table

    def save_employee(self):
        first_name = self.entry_firstname.get()
        last_name = self.entry_lastname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        role = self.role_var.get()
        self.table.insert('', 'end', text="1", values=(first_name, last_name, username, role))

        self.save_employee_to_db(first_name, last_name, username, password, role)

    def save_employee_to_db(self, first_name, last_name, username, password, role):
        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        password TEXT,
        role TEXT)''')

        c.execute("INSERT INTO employees (first_name, last_name, username, password, role) VALUES (?, ?, ?, ?, ?)",
                  (first_name, last_name, username, password, role))
        conn.commit()
        conn.close()

class AdminPanel:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        if self.role == "Официант":
            self.waiter_window = WaiterWindow(self.root, self.role)
        elif self.role == "Повар":
            self.cook_window = CookWindow(self.root, self.role)
        else:
            self.show_admin_window()

    def show_admin_window(self):
        label = tk.Label(self.root, text="Роль сотрудника: " + self.role)
        label.pack()
        self.create_employees_table()
        self.root = tk.Tk()
        self.root.title("Панель администратора")
        self.root.geometry("600x400")
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        self.employees_button = tk.Button(
            self.frame, text="Сотрудники", command=self.show_employees_window, width=15, height=3,
            font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.employees_button.pack(pady=10)
        self.orders_button = tk.Button(self.frame, text="Заказы", command=self.show_orders_window, width=15,
                                       height=3, font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.orders_button.pack(pady=10)
        self.schedule_button = tk.Button(self.frame, text="График смен", command=self.show_schedule_window, width=15,
                                         height=3, font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        self.schedule_button.pack(pady=10)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.root.mainloop()
        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            password TEXT,
            role TEXT)''')

        conn.commit()
        conn.close()

    def show_waiter_window(self):
        self.root.title("Окно официанта")
        self.root.geometry("400x300")
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)
        self.waiter_window = WaiterWindow(self.root, self.role)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_chef_window(self):
        self.cook_window = tk.Toplevel(self.root)
        self.cook_window.title("Окно повара")
        self.cook_window.geometry("400x300")
        self.cook_frame = tk.Frame(self.cook_window)
        self.cook_frame.pack(expand=True)
        self.orders_button = tk.Button(self.cook_frame, text="Заказы", command=self.show_orders_window, width=15, height=3)
        self.orders_button.pack(pady=10)
        self.cook_window = CookWindow(self.cook_window, self.role)

    def create_employees_table(self):
        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            password TEXT,
            role TEXT)''')
        conn.commit()
        conn.close()

    def show_employees_window(self):
        self.employees_window = tk.Toplevel(self.root)
        self.employees_window.title("Сотрудники")
        self.employees_window.geometry("400x300")

        self.employees_list = ttk.Treeview(self.employees_window, columns=("ID", "Name", "Role"))
        self.employees_list.heading("#0", text="ID")
        self.employees_list.column("#0", minwidth=0, width=50, stretch=tk.NO)
        self.employees_list.heading("ID", text="Имя")
        self.employees_list.heading("Name", text="Фамилия")
        self.employees_list.heading("Role", text="Роль")
        self.employees_list.pack()

        connection = sqlite3.connect("C:/Users/Сергей/Desktop/4/ГИА/basa.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        for employee in employees:
            self.employees_list.insert("", "end", text=employee[0], values=(employee[1], employee[2], employee[5]))

        connection.close()

        add_employee_button = tk.Button(self.employees_window, text="Добавить", command=self.open_add_employee_window, font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        add_employee_button.pack(pady=10)

    def open_add_employee_window(self):
        add_employee_window = tk.Toplevel(self.employees_window)
        add_employee_window.title("Добавить сотрудника")
        add_employee_window.geometry("300x200")

        add_employee_view = AddEmployeeWindow(add_employee_window, self.employees_list)

    def show_orders_window(self):
        orders_window = tk.Toplevel(self.root)
        orders_window.title("Заказы")
        orders_window.geometry("800x400")

        self.orders_table = ttk.Treeview(orders_window,
                                         columns=("Table", "Status", "Payment Status", "Completed", "Dishes"))
        self.orders_table.heading("#0", text="ID")
        self.orders_table.heading("Table", text="Столик")
        self.orders_table.heading("Status", text="Статус")
        self.orders_table.heading("Payment Status", text="Статус оплаты")
        self.orders_table.heading("Completed", text="Выполнен")
        self.orders_table.heading("Dishes", text="Блюда в заказе")
        self.orders_table.pack()

        delete_order_button = tk.Button(orders_window, text="Удалить заказ", command=self.delete_order, font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        delete_order_button.pack(pady=10)

        add_order_button = tk.Button(orders_window, text="Добавить заказ", command=self.open_add_order_window, font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        add_order_button.pack(pady=10)

        self.load_orders_from_db()

    def load_orders_from_db(self):
        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM orders")
            orders = c.fetchall()

            for order in orders:
                id, table, status, payment_status, completed, dishes = order
                self.orders_table.insert('', 'end', values=(dishes,  table, status, payment_status, completed))

    def open_add_order_window(self):
        add_order_window = tk.Toplevel(self.root)
        add_order_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(add_order_window))
        add_order_window.title("Добавить заказ")
        add_order_window.geometry("400x400")

        self.table_label = tk.Label(add_order_window, text="Столик")
        self.table_label.pack()
        self.table_entry = tk.Entry(add_order_window)
        self.table_entry.pack()

        self.dishes_label = tk.Label(add_order_window, text="Блюда (разделяйте запятой)")
        self.dishes_label.pack()
        self.dishes_entry = tk.Entry(add_order_window)
        self.dishes_entry.pack()

        self.status_label = tk.Label(add_order_window, text="Статус")
        self.status_label.pack()
        self.status_combobox = ttk.Combobox(add_order_window, values=["Готов", "Готовится"])
        self.status_combobox.pack()

        self.payment_status_label = tk.Label(add_order_window, text="Статус оплаты")
        self.payment_status_label.pack()
        self.payment_status_combobox = ttk.Combobox(add_order_window, values=["Принят", "Оплачен"])
        self.payment_status_combobox.pack()

        self.completed_label = tk.Label(add_order_window, text="Выполнен (Да/Нет)")
        self.completed_label.pack()
        self.completed_entry = tk.Entry(add_order_window)
        self.completed_entry.pack()

        save_button = tk.Button(add_order_window, text="Сохранить", command=lambda: self.save_order(add_order_window), font=("Comic_Sans_MS", 14), fg="black", bg='#76e383')
        save_button.pack()

    def save_employee_to_db(self, first_name, last_name, username, password, role):
        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            password TEXT,
            role TEXT)''')

        c.execute("INSERT INTO employees (first_name, last_name, username, password, role) VALUES (?, ?, ?, ?, ?)",
                  (first_name, last_name, username, password, role))
        conn.commit()
        conn.close()
    def save_order(self, add_order_window):
        table = str(self.table_entry.get())
        status = self.status_combobox.get()
        payment_status = self.payment_status_combobox.get()
        completed = self.completed_entry.get()

        selected_dishes = [dish.strip() for dish in self.dishes_entry.get().split(',') if dish.strip()]
        dish_list = ", ".join(selected_dishes)

        self.orders_table.insert('', 'end', text="1", values=(table, status, payment_status, completed, dish_list))

        save_order_to_db(table, status, payment_status, completed,
                         selected_dishes)
        self.orders_table.delete(*self.orders_table.get_children())
        self.load_orders_from_db()

        add_order_window.destroy()

    def delete_order(self):
        selected_item = self.orders_table.selection()
        if selected_item:
            self.orders_table.delete(selected_item)
            self.delete_order_from_db(selected_item[0])
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите заказ для удаления")

    def delete_order_from_db(self, order_id):
        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        c = conn.cursor()
        c.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
        conn.close()

    def show_schedule_window(self):
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("График смен")
        schedule_window.geometry("400x300")

    def on_window_close(self, window):
        window.destroy()

def save_order_to_db(table_number, status, payment_status, completed, selected_dishes):
    conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER,
    status TEXT,
    payment_status TEXT,
    completed TEXT,
    dishes TEXT)''')

    c.execute("INSERT INTO orders (table_number, status, payment_status, completed, dishes) VALUES (?, ?, ?, ?, ?)",
              (int(table_number) if table_number else None, status, payment_status, completed, ", ".join(selected_dishes)))
    conn.commit()
    conn.close()

class WaiterWindow:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        self.show_waiter_window()

    def show_waiter_window(self):
        self.root.title("Окно официанта")
        self.root.geometry("400x300")
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        self.orders_button = tk.Button(self.frame, text="Заказы", command=self.show_orders_window_waiter, width=15, height=3)
        self.orders_button.pack(pady=10)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_orders_window_waiter(self):
        orders_window = tk.Toplevel(self.root)
        orders_window.title("Список всех заказов")
        orders_window.geometry("800x400")
        orders_table = ttk.Treeview(orders_window, columns=("Table", "Status", "Payment Status", "Completed", "Dishes"))
        orders_table.heading("#0", text="ID")
        orders_table.heading("Table", text="Столик")
        orders_table.heading("Status", text="Статус")
        orders_table.heading("Payment Status", text="Статус оплаты")
        orders_table.heading("Completed", text="Выполнен")
        orders_table.heading("Dishes", text="Блюда в заказе")
        orders_table.pack()

        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM orders")
            orders = c.fetchall()
            for order in orders:
                orders_table.insert('', 'end', values=order)

class CookWindow:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        self.show_cook_window()

    def show_cook_window(self):
        self.root.title("Окно повара")
        self.root.geometry("400x300")
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)
        self.orders_button = tk.Button(self.frame, text="Заказы", command=self.show_orders_window_cook, width=15, height=3)
        self.orders_button.pack(pady=10)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_orders_window_cook(self):
        orders_window = tk.Toplevel(self.root)
        orders_window.title("Список заказов")
        orders_window.geometry("800x400")
        orders_table = ttk.Treeview(orders_window, columns=("Table", "Status", "Payment Status", "Completed", "Dishes"))
        orders_table.heading("#0", text="ID")
        orders_table.heading("Table", text="Столик")
        orders_table.heading("Status", text="Статус")
        orders_table.heading("Payment Status", text="Статус оплаты")
        orders_table.heading("Completed", text="Выполнен")
        orders_table.heading("Dishes", text="Блюда в заказе")
        orders_table.pack()

        conn = sqlite3.connect('C:/Users/Сергей/Desktop/4/ГИА/basa.db')
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM orders")
            orders = c.fetchall()
            for order in orders:
                orders_table.insert('', 'end', values=order)

def run():
    root = tk.Tk()
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()