import tkinter as tk
from algorithm import *

class Filter():
    def get(self):
        '''Return a list of lists, containing the data in the table'''
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(self._entry[index].get())
            result.append(current_row)
        return result

    def _validate(self, P):
        '''Perform input validation.

        Allow only an empty value, or a value that can be converted to a float
        '''
        if P.strip() == "":
            return True

        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True

class SizeInput(tk.Frame, Filter):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.n = tk.IntVar()
        self.n.set(5)
        vcmd = (self.register(self._validate), "%P")
        self.name_label = tk.Label(text="Введите количество вершин:")
        self.name_label.pack()
        self.name_entry = tk.Entry(textvariable=self.n, validate="key", validatecommand=vcmd, width=5)
        self.name_entry.pack()
        self.inp = tk.Button(text="Ввод", command=self.event)
        self.inp.pack()
        self.table = SimpleTableInput(self, self.n.get(), self.n.get())
        self.submit = tk.Button(self, text="Ввод", command=self.on_submit)
        self.table.pack(side="top", fill="both", expand=True)
        self.submit.pack()
        self.ans = tk.Text(root, height=5, width=52)
        self.ans.pack(side="bottom")

    def event(self):
        n = self.n.get()
        self.table.destroy()
        self.submit.destroy()
        self.table = SimpleTableInput(self, self.n.get(), self.n.get())
        self.table.pack(side="top", fill="both", expand=True)
        self.submit = tk.Button(self, text="Ввод", command=self.on_submit)
        self.submit.pack(side="bottom")


    def on_submit(self):
        t = self.table.get()
        t = [list( map(int,i) ) for i in t]
        for i in range(self.n.get()):
            t[i][i] = 1
        solve = main(t, self.n.get())
        self.ans.delete('1.0', tk.END)
        solve = solve.split(" <= ")[1].replace(" + ", "\n")
        self.ans.insert(tk.END, solve)


class SimpleTableInput(tk.Frame, Filter):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        vcmd = (self.register(self._validate), "%P")

        self._entry = {}
        self.rows = rows
        self.columns = columns

        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, validate="key", validatecommand=vcmd, width=5)
                e.insert(0, "0")
                e.grid(row=row, column=column, stick="nsew")
                self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)


class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.input = SizeInput(self)
        self.input.pack(side="bottom")

root = tk.Tk()
root.title("Минимальные внешне устойчивые подмножества графа")
root.geometry("500x300")
root.resizable(False, True)
Example(root).pack(side="top", fill="both", expand=True)
root.mainloop()