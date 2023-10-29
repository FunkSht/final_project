import tkinter as tk
from tkinter import ttk
import sqlite3




#создание " окна "
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Метод для хранения и инициализации об. граф. интерфейса
    def init_main(self):
        # создание " тулбар "
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        # Кнопка " добавления ""
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img, command=self.open_dialog)
        # упаковка, выравнивание
        btn_open_dialog.pack(side=tk.LEFT)

        # Кнопка " изменения данных "
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                    image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка для " удаления записи'ей "
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Поиск
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Обновление
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Добавление " Treeview "
        self.tree = ttk.Treeview(self, columns=('name', 'id', 'phone', 'email', 'salary'),
                                 height=45, show='headings')
        
        # добавление параметров
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("id", width=30, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        # подписи колонок с параметрами
        self.tree.heading("name", text='ФИО')
        self.tree.heading("id", text='id')
        self.tree.heading("phone", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("salary", text='Зарплата')

        # упаковка
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # добавление данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # изменение данных
    def update_record(self, name, phone, email, salary):
        self.db.c.execute('''UPDATE db SET name=?, phone=?, email=?, salary=? WHERE id=?''',
                          (name, phone, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Вывод ( в виджет таблицы )
    def view_records(self):
        # Выбираем инфу из бд
        self.db.c.execute('''SELECT * FROM db''')
        # удаление всего из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Добавление инфы из бд, в виджет таблицу
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]
        
    # удаление записей
    def delete_records(self):
        # цикл по выделенным записям
        for selection_item in self.tree.selection():
            # удаление из БД
            self.db.c.execute('''DELETE FROM db WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        # сохранение изменений в БД
        self.db.conn.commit()
        # обновление виджета таблицы
        self.view_records()

    # поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    # вызов дочернего окна
    def open_dialog(self):
        Child()

    # вызов окна для изменения данных
    def open_update_dialog(self):
        Update()

    # вызов окна для поиска
    def open_search_dialog(self):
        Search()

# класс дочерних окон
# Toplevel - окно верхнего уровня
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # заголовок окна
        self.title('Добавить')
        # размер окна
        self.geometry('400x220')
        # ограничение по изменению размера окна 
        self.resizable(False, False)

        # перехват всех событий, которые происходят в приложении
        self.grab_set()
        # захватывание фокуса
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_pay = tk.Label(self, text='Зарплата')
        label_pay.place(x=50, y=140)

        # строка ввода для наименования
        self.entry_name = ttk.Entry(self)
        # координаты объекта
        self.entry_name.place(x=200, y=50)

        # строка ввода для e - mail
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        # строка ввода для телефона
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # строка ввода для зарплаты
        self.entry_wage = ttk.Entry(self)
        self.entry_wage.place(x=200, y=140)

        # кнопка для закрытия дочернего окна
        self.btn_cancel = ttk.Button(
            self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # кнопка для добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        # срабатывание по лкм
        # при нажатии кнопки вызывается метод records, ему передаются значения из строк
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_tel.get(),
                                                                       self.entry_wage.get()))
    

# класс окна для обновления, наследуемый от класса дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Изменить позицию')
        btn_edit = ttk.Button(self, text='Изменить')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_tel.get(),
                                                                          self.entry_wage.get()))

        # закрытие окна " редактирования "
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
       
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_wage.insert(0, row[4])


# класс, для поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')


# класс БД
class DB:
    def __init__(self):
        # соединение с БД
        self.conn = sqlite3.connect('db.db')
        # создание объекта класса cursor, используемый для взаимодействия с БД
        self.c = self.conn.cursor()
        # запрос к БД
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS db (id integer primary key, name text, tel text, email text, salary text)''')
        # сохранение изменений БД
        self.conn.commit()

    # метод добавления в БД
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''INSERT INTO db (name, tel, e-mail, salary) VALUES (?, ?, ?, ?)''',
                       (name, tel, email,salary))
        self.conn.commit()




if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    # заголовок 
    root.title('Список сотрудников')
    # размер окна
    root.geometry('800x600')
    root.resizable(False, False)
    root.mainloop()