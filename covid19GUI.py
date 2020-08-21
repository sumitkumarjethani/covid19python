from tkinter import *
import sqlite3
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Covid19_GUI():
    def __init__(self,root):
        self.conn = sqlite3.connect('covid.sqlite')
        self.cur = self.conn.cursor()
        
        self.root = root
        self.menu_frame = Frame(self.root, width="400", height="100")
        self.graphics_frame = Frame(self.root,width="600",height="400")
        self.selected = IntVar()
        
        #root config
        self.root.title("Aplicación Covid-19 Gráficos")
        
        #menu frame config
        self.menu_frame.pack(fill="x")
        self.lbl_option = Label(self.menu_frame, text="Choose an option", 
                                font=("Times New Roman bold", 12))
        self.lbl_option.grid(row=0,column=0,sticky="w",padx=5,pady=5)
        
        self.rad1 = Radiobutton(self.menu_frame,text='Continent', value=1,
                                font=("Times New Roman bold", 12),variable=self.selected,
                                command=self.show_continent_combobox)
        self.rad1.grid(row=1,column=0,sticky="w",padx=3,pady=3)
    
        self.rad2 = Radiobutton(self.menu_frame,text='Country', value=2,
                                font=("Times New Roman bold", 12),variable=self.selected,
                                command=self.show_country_combobox)
        self.rad2.grid(row=2,column=0,sticky="w",padx = 3,pady=3)
        
        self.accept = Button(self.menu_frame,text="Accept",command=self.accept_button,width=20,
                             font=("Times New Roman bold", 12),bg='#0052cc', fg='#ffffff')
        self.accept.grid(row=0,column=2,sticky="e",padx=5,pady=5)
        
        self.lbl_combobox = Label(self.menu_frame,font=("Times New Roman bold", 12))
        self.combobox = ttk.Combobox(self.menu_frame,width=15)
        
        #graphics frame config
        self.graphics_frame.pack(fill="both",expand="True")
        
        
    def accept_button(self):
        if self.selected.get() == 1:
            self.paint_continent_graphics()
        elif self.selected.get() == 2:
            self.paint_country_graphics()
    
    def paint_continent_graphics(self):
        print('polla')

    def paint_country_graphics(self):
        name_country = self.combobox.get()
        self.cur.execute('''SELECT id FROM Country WHERE name=?''',(name_country,))
        id_country = self.cur.fetchone()[0]
        self.cur.execute('''SELECT day,month,year,cases,deaths FROM Daily_data
                         WHERE id_country=? ORDER BY year ASC, month ASC, day ASC''',(id_country,))
        rows = self.cur.fetchall()
        dates = list()
        cases = list()
        deaths = list()
        for row in rows:
            date = str(row[0]) + "/" + str(row[1]) + "/" + str(row[2])
            dates.append(date)
            cases.append(row[3])
            deaths.append(row[4])
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(dates,cases)
        
        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    
    def fill_combobox(self,num):
        if num == 1:
            self.cur.execute('''SELECT name FROM Continent''')
        else:
            self.cur.execute('''SELECT name FROM Country''')
        names = list()
        rows = self.cur.fetchall()
        for row in rows:
            names.append(row[0])
        self.combobox["values"] = names 
    
    
    def show_continent_combobox(self):
        self.lbl_combobox["text"] = "Continents"
        self.lbl_combobox.grid(row=0,column=1,sticky="e",padx=5,pady=5)
        self.fill_combobox(1)
        self.combobox.current(0)
        self.combobox.grid(row=1,column=1,sticky="e",padx=3,pady=3)

    def show_country_combobox(self):
        self.lbl_combobox["text"] = "Countries"
        self.lbl_combobox.grid(row=0,column=1,sticky="e",padx=5,pady=5)
        self.fill_combobox(2)
        self.combobox.current(0)
        self.combobox.grid(row=1,column=1,padx=3,pady=3)
    

def main():
    root = Tk()
    Covid19_GUI(root)
    root.mainloop()

main()