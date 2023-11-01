import tkinter as tk
from tkinter import _Cursor, _Relief, _ScreenUnits, _TakeFocusValue, Menu, Misc, ttk
import sqlite3
from typing import Any
from typing_extensions import Literal

class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        tollbar = tk.Frame(bg='#d7d8e0',bd = 2)
        tollbar.pack(side=tk.TOP,fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(tollbar,bg='#d7d8e0',bd = 0,image=self.add_img,command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID','name','price'),height=45,show='headings')
        self.tree.column('ID',width=30,anchor=tk.CENTER)
        self.tree.column('name',width=300,anchor=tk.CENTER)
        self.tree.column('price',width=150,anchor=tk.CENTER)
        self.tree.heading('ID',text='ID')
        self.tree.heading('name',text='name')
        self.tree.heading('price',text='price')
        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(tollbar,bg='#d7d8e0',bd=0,image=self.update_img,command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(tollbar, bg='#d7d8e0',bd=0,image=self.delete_img,command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(tollbar,bg='#d7d8e0',bd=0,image=self.search_img,command=self.open_search_dialog )
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='./img/refresh.jpeg')
        btn_refresh = tk.Button(tollbar,bg='#d7d8e0',bd=0,image=self.refresh_img,command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)




    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def records(self,name,price):
        self.db.insert_data(name,price)
        self.view_records()
    
    def view_records(self):
        self.db.c.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row)for row in self.db.c.fetchall()]

        self.db.conn.commit()
        self.view_records()

    def delete_record(self):
        for select_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM db WHERE id=?',self.tree.set(select_item,'#1'))
            self.db.conn.commit()
            self.view_records()
        
    def open_search_dialog(self):
        Search()

    def search_records(self,name):
        name = ('%',+ name + '%')
        self.db.cur.execute('SELECT * FROM db WHERE name LIKE ?',name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row)for row in self.db.cur.fetchall()]
        self.view_records()



    

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    def init_child(self):
        self.title('добавить продукт')
        self.geometry('440x220')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self,text='name')
        label_name.place(x=50,y=50)
        label_price = tk.Label(self,text='price')
        label_price.place(x=50,y=80)
        entry_name = ttk.Entry(self)
        entry_name.place(x=200,y=50)
        entry_price = ttk.Entry(self)
        entry_price.place(x=200,y=80)
        self.btn_cancel = ttk.Button(self,text='close',command=self.destroy)
        self.btn_cancel.place(x=300,y=170)
        self.btn_ok = ttk.Button(self,text='add')
        self.btn_ok.place(x=220,y=170)
        self.btn_ok.bind('<Button-l>',lambda event:
                         self.view.records(entry_name.get(),
                                           entry_price.get()))
        
        self.btn_ok.bind('<Button-l>',lambda event: self.destroy(),add='+')


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('редактировать товар')
        btn_edit = ttk.Button(self,text='редактировать')
        btn_edit.place(x=180,y=170)
        btn_edit.bind('<Button-l>',lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_price.get()))
        
        btn_edit.bind('<Button-l>',lambda event: self.destroy(),add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cur.execute('SELECT * FROM db WHERE id=?,',(self.view.tree.set(self.view.tree.selection() [0],'#1'),))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_price.insert(0,row[2])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_searcg(self):
        self.title('поиск продукта')
        self.geometry('300x100')
        self.resizable(False,False)

        label_search = tk.Label(self,text='название')
        label_search.place(x=50,y=20)
        
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105,y=20,width=150)

        btn_cancel = ttk.Button(self,text='закрыть',command=self.destroy)
        btn_cancel.place(x=185,y=50)

        btn_search = ttk.Button(self,text='поиск')
        btn_search.place(x=105,y=50)
        btn_search.bind('<Button-l>',lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-l>',lambda event:self.destroy(),add='+')

                        
                         


class BD:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS db (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       price TEXT);''')
        self.conn.commit()
        
    def insert_data(self,name,price):
        self.c.execute('INSERT INTO db(name,price) VALUES(?,?,?)',(name,price))
        self.conn.commit()














if __name__ == '__main__':
    root = tk.Tk()
    db = BD()
    app = Main(root)
    app.pack()
    root.title('бытовая техника')
    root.geometry('665x450')
    root.resizable(False,False)
    root.mainloop()