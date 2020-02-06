import tkinter.filedialog
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import re
import random

class Application:
    def __init__(self, master=None):
        self.master = master
        self.master.title('Advanced Password Generator')
        window.geometry("800x300")
        ttk.Style().theme_use("xpnative")
        
        # Adding Menu Bar at the top of the window
        self.menubar = tk.Menu(self.master)
        self.menu_bar()
        self.master.config(menu=self.menubar)
        
        tab_parent = ttk.Notebook()
        self.tab1 = ttk.Frame(tab_parent)
        self.tab2 = ttk.Frame(tab_parent)
        self.tab3 = ttk.Frame(tab_parent)
        
        self.left_section = tk.Frame(self.tab1, borderwidth=0)
        self.left_section.pack(expand=1, padx=0, pady=0, side=tk.LEFT, fill=tk.BOTH)
        
        self.right_section = tk.Frame(self.tab1, borderwidth=0)
        self.right_section.pack(expand=1, padx=0, pady=0, side=tk.RIGHT, fill=tk.BOTH)
        
        tab_parent.add(self.tab1, text="Brute Force")
        tab_parent.add(self.tab2, text="Random")
        tab_parent.add(self.tab3, text="Passwords")
        tab_parent.pack(expand=1, fill='both')
        
        self.random_tap()
        
        self.statusbar = tk.Label(self.left_section, text="Ready", bd=1, padx=5, pady=5, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.current_password = ''
        self.rules_values = tk.Variable()
        
        self.add_new()
        self.control_rules()
        self.copy_export()
        self.Generated_passwords()
    
    def random_tap(self):
        tab2_number_rules_label = ttk.Label(self.tab2, text='Number of Rules:')
        tab2_number_rules_label.grid(row=0, column=0)
        self.tab2_number_rules_entry = ttk.Entry(self.tab2)
        self.tab2_number_rules_entry.grid(row=0, column=1)
        
        self.tab2_special_digits_label = ttk.Label(self.tab2, text='Special Digits:')
        self.tab2_special_digits_label.grid(row=1, column=0)
        self.tab2_special_digits_entry = ttk.Entry(self.tab2)
        self.tab2_special_digits_entry.grid(row=1, column=1)
        
        
        self.tab2_alpha_value = tk.BooleanVar()
        self.tab2_alpha_checkbox = tk.Checkbutton(self.tab2, text="A:Z", variable=self.tab2_alpha_value)
        self.tab2_alpha_checkbox.grid(row=2, column=0)
        
        self.tab2_alpha_small_value = tk.BooleanVar()
        self.tab2_alpha_small_checkbox = tk.Checkbutton(self.tab2, text="a:z", variable=self.tab2_alpha_small_value)
        self.tab2_alpha_small_checkbox.grid(row=2, column=1)
        
        self.tab2_numbers_value = tk.BooleanVar()
        self.tab2_numbers_checkbox = tk.Checkbutton(self.tab2, text="0:9", variable=self.tab2_numbers_value)
        self.tab2_numbers_checkbox.grid(row=2, column=2)
        
        tab2_add_btn = ttk.Button(self.tab2, text='Generate', command=self.tab2_Generate)
        tab2_add_btn.grid(row=3, column=0, columnspan=3, sticky='wesn')
        self.tab2_Generated_passwords()
    
    def restart(self):
        self.clear_rules_list()
        self.password_list.delete(0, 'end')
    
    def menu_bar(self):
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.restart)
        filemenu.add_command(label="Open Rules", command=quit)
        filemenu.add_command(label="Open Passwords", command=quit)
        filemenu.add_separator()
        filemenu.add_command(label="Save Rules as...", command=self.save_rules)
        filemenu.add_command(label="Export Passwords", command=self.export_btn)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = tk.Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Documentation", command=quit)
        helpmenu.add_command(label="Check for Updates...", command=quit)
        helpmenu.add_command(label="About", command=self.restart)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
  
    def add_new(self):
        add_rules= ttk.LabelFrame(self.left_section, text='Add New Digit')
        add_rules.pack(padx=20, pady=20, fill=tk.BOTH)
        
        add_digit_label = ttk.Label(add_rules, text='Add Digit:')
        add_digit_label.pack(padx=5, pady=20, fill=tk.BOTH, side=tk.LEFT)
        
        self.add_digit_entry = ttk.Entry(add_rules)
        self.add_digit_entry.pack(expand=1, padx=5, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        
        self.alpha_value = tk.BooleanVar()
        self.alpha_checkbox = tk.Checkbutton(add_rules, text="A:Z", variable=self.alpha_value)
        # self.alpha_checkbox.deselect()
        self.alpha_checkbox.pack(expand=1, padx=0, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        self.alpha_small_value = tk.BooleanVar()
        self.alpha_small_checkbox = tk.Checkbutton(add_rules, text="a:z", variable=self.alpha_small_value)
        # self.alpha_small_checkbox.deselect()
        self.alpha_small_checkbox.pack(expand=1, padx=0, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        self.numbers_value = tk.BooleanVar()
        self.numbers_checkbox = tk.Checkbutton(add_rules, text="0:9", variable=self.numbers_value)
        # self.numbers_checkbox.select()
        self.numbers_checkbox.pack(expand=1, padx=0, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        add_btn = ttk.Button(add_rules, text='Add', command=self.insert_rule)
        add_btn.pack(expand=1, padx=5, pady=20, side=tk.LEFT, fill=tk.BOTH)

    def insert_rule(self):
        text = self.add_digit_entry.get()
        if self.alpha_value.get():
            text += 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z'
        if self.alpha_small_value.get():
            text += 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'
        if self.numbers_value.get():
            text += '0,1,2,3,4,5,6,7,8,9'
        if text.strip():
            self.rules_list.insert(tk.END, text)
            self.add_digit_entry.delete(0,"end")

    def control_rules(self):
        all_sides = ttk.LabelFrame(self.left_section, text='Control Rules')
        all_sides.pack(expand=1, padx=20, pady=10, fill=tk.BOTH)
        
        right = tk.LabelFrame(all_sides, borderwidth=0)
        right.pack(expand=1, padx=20, pady=10, side=tk.LEFT, fill=tk.BOTH)
        
        left = tk.LabelFrame(all_sides, borderwidth=0)
        left.pack(expand=0, padx=20, pady=30, side=tk.RIGHT, fill=tk.BOTH)
        
        rules= tk.Frame(right, borderwidth=0)
        rules.pack(expand=1, padx=0, pady=0, side=tk.LEFT, fill=tk.BOTH)

        self.rules_list = tk.Listbox(rules, borderwidth=0, listvariable=self.rules_values)
        self.rules_list.pack(expand=1, padx=0, pady=0, side=tk.LEFT, fill=tk.BOTH)
        sc = tk.Scrollbar(self.rules_list, orient="vertical")
        sc.pack(side=tk.RIGHT, fill=tk.Y)
        self.rules_list.config(yscrollcommand=sc.set)
        sc.config(command=self.rules_list.yview)
        
        for line in range(4):
            self.rules_list.insert(tk.END, "0,1 , 2,3" + str(line))
        
        up_btn = ttk.Button(left, text='Up', command=self.up_btn)
        up_btn.pack(padx=0, pady=10,side=tk.TOP, expand=1, fill=tk.X)
        
        down_btn = ttk.Button(left, text='Down', command=self.down_btn)
        down_btn.pack(padx=0, pady=10,side=tk.TOP, expand=1, fill=tk.X)
        
        remove_btn = ttk.Button(left, text='Remove', command=self.remove_btn)
        remove_btn.pack(padx=0, pady=10,side=tk.TOP, expand=1, fill=tk.X)
        
        clear_all_btn = ttk.Button(left, text='Clear All', command=self.clear_rules_list)
        clear_all_btn.pack(padx=0, pady=10,side=tk.TOP, expand=1, fill=tk.X)

    def copy_next_btn(self):
        self.password_list.clipboard_clear()
        print(self.password_list.size())
        try:
            if self.password_list.curselection():
                self.current_password = self.password_list.curselection()
            else:
                if self.current_password[0] < self.password_list.size()-1:
                    self.current_password = self.current_password[0]+1
                else:
                    self.current_password = self.password_list.size()-1
                self.password_list.selection_set(self.current_password)
                print('not selected', self.current_password)
            print(self.current_password)
        
        except tk._tkinter.TclError:
            pass
            
        try:
            self.idxs = self.password_list.curselection()
            if not self.idxs:
                return
            for pos in self.idxs:
                # Are we at the bottom of the list?
                if pos == self.password_list.size()-1:
                    return
                text = self.password_list.get(pos)
                self.password_list.selection_set(pos + 1)
                self.password_list.selection_clear(pos)                
        except:
            pass

    def copy_prev_btn(self):
        self.password_list.clipboard_clear()
        try:
            if self.password_list.curselection():
                self.current_password = self.password_list.curselection()
            else:
                if self.current_password[0]>0:
                    self.current_password = self.current_password[0]-1 
                else:
                    self.current_password = 0
                self.password_list.selection_set(self.current_password)
                print('not selected', self.current_password)
            text = self.password_list.get(self.current_password)
        
        except tk._tkinter.TclError:
            text = self.current_password

        self.password_list.clipboard_append(text)
            
        try:
            self.idxs = self.password_list.curselection()
            if not self.idxs:
                return
            for pos in self.idxs:
                # Are we at the bottom of the list?
                if pos == self.password_list.size()-1:
                    return
                text = self.password_list.get(pos)
                self.password_list.selection_set(pos - 1)
                self.password_list.selection_clear(pos)                
        except:
            pass

    def export_btn(self):
        f = tk.filedialog.asksaveasfile(defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*") ))
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text = self.password_list.get(0, 'end')
        for i in text:
            f.write(i)
            f.write('\n')
        f.close()

    def save_rules(self):
        f = tk.filedialog.asksaveasfile(defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*") ))
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text = self.rules_list.get(0, 'end')
        for i in text:
            f.write(i)
            f.write('\n')
        f.close()

    def remove_btn(self):
        try:
            selection = self.rules_list.curselection()
            self.rules_list.delete(selection[0])
        except:
            self.rules_list.delete('end')
    
    def up_btn(self):
        try:
            self.idxs = self.rules_list.curselection()
            if not self.idxs:
                return
            for pos in self.idxs:
                if pos == 0:
                    continue
                text = self.rules_list.get(pos)
                self.rules_list.delete(pos)
                self.rules_list.insert(pos-1, text)
                self.rules_list.selection_set(pos-1)
        except:
            pass
    
    def down_btn(self):
        try:
            self.idxs = self.rules_list.curselection()
            if not self.idxs:
                return
            for pos in self.idxs:
                # Are we at the bottom of the list?
                if pos == self.rules_list.size()-1:
                    continue
                text = self.rules_list.get(pos)
                self.rules_list.delete(pos)
                self.rules_list.insert(pos+1, text)
                self.rules_list.selection_set(pos + 1)
        except:
            pass
        
    def clear_rules_list(self):
        self.rules_list.delete(0, 'end')
    
    def copy_export(self):
        copy_and_export= ttk.LabelFrame(self.left_section, text='Save, Export and Copy')
        copy_and_export.pack(padx=20, pady=20, fill=tk.BOTH)
        
        self.reverse_value = tk.BooleanVar()
        self.reverse_checkbox = tk.Checkbutton(copy_and_export, text="Reverse", variable=self.reverse_value)
        # self.reverse_checkbox.deselect()
        self.reverse_checkbox.pack(expand=1, padx=0, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        generte_btn = ttk.Button(copy_and_export, text='Generte', command=self.Generate)
        generte_btn.pack(expand=1, padx=20, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        export_btn = ttk.Button(copy_and_export, text='Export', command=self.export_btn)
        export_btn.pack(expand=1, padx=20, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        copy_prev_btn = ttk.Button(copy_and_export, text='Copy Previous',command=self.copy_prev_btn)
        copy_prev_btn.pack(expand=1, padx=20, pady=20, side=tk.LEFT, fill=tk.BOTH)
        
        copy_next_btn = ttk.Button(copy_and_export, text='Copy Next', command=self.copy_next_btn)
        copy_next_btn.pack(expand=1, padx=20, pady=20, side=tk.LEFT, fill=tk.BOTH)

    def Generated_passwords(self):
        paswords = ttk.LabelFrame(self.right_section, text='Generated Passwords')
        paswords.pack(expand=1, padx=20, pady=20, side=tk.LEFT, fill='both')
        
        self.password_list = tk.Listbox(paswords, selectmode='single', borderwidth=0)
        self.password_list.pack(expand=1, padx=10, pady=20, side=tk.RIGHT, fill=tk.BOTH)
        
        sc = tk.Scrollbar(self.password_list, orient="vertical")
        sc.pack(side=tk.RIGHT, fill=tk.Y)
        self.password_list.config(yscrollcommand=sc.set)
        sc.config(command=self.password_list.yview)

    def tab2_Generated_passwords(self):
        tab2_paswords = ttk.LabelFrame(self.tab2, text='Generated Passwords')
        tab2_paswords.grid(row=0, column=4)
        
        self.tab2_password_list = tk.Listbox(tab2_paswords, selectmode='single', borderwidth=0)
        self.tab2_password_list.grid(row=0, column=0, columnspan=3)
        
        # sc = tk.Scrollbar(self.tab2_password_list, orient="vertical")
        # sc.grid(row=0, column=1)
        # self.tab2_password_list.config(yscrollcommand=sc.set)
        # sc.config(command=self.tab2_password_list.yview)

    def grouper(self, lst, lst2):
        '''Group items from two lists to pairs
        '''
        appended_lst = []
        for i in lst:
            for m in lst2:
                appended_lst.append(i + m)
        return appended_lst

    def Generate(self):
        rules = self.rules_values.get()
        inp = []
        for rule in rules:
            item = []
            for key in re.split(r'(?<!\\),', rule):
                if key.replace('\\', '').strip() == '':
                    continue
                item.append(key.replace('\\', '').strip())
            inp.append(item)
        
        
        counter = 1
        for i in rules:
            all_lists = list(dict.fromkeys(i.split(',')))
            counter *= len(all_lists)
        m = messagebox.askyesno(title="Number of passwords", message='Do you want to generate ' + str(counter) + ' passwords')
        if not m:
            return
        
        self.statusbar.config(text='Generating Passwords...')
        all_lists = inp[0]
        for lst_num in range(len(inp)-1):
            all_lists = self.grouper(all_lists, inp[lst_num+1])
        
        # Remove duplicated Characters
        all_lists = list(dict.fromkeys(all_lists))
        
        # Reverd the generated passwords
        if self.reverse_value.get():
            all_lists = sorted(all_lists, reverse=True)
        
        self.statusbar.config(text='Displaying Passwords...')

        self.password_list.delete(0,'end')
        counter = 1
        for passwd in all_lists:
            self.password_list.insert(tk.END, passwd)
            counter += 1
        self.password_list.selection_set(0)
        self.statusbar.config(text=str(counter-1) + ' passwords are generated successfully')
        
    def tab2_Generate(self):
        number_rules = self.tab2_number_rules_entry.get()
        try:
            number_rules = int(number_rules)
        except:
            if type(number_rules) is not int:
                messagebox.showerror(title="Wrong Rules Numbers", message='Please, Enter an integer!')
                return
        inp = []
        if self.tab2_special_digits_entry.get():
            item = []
            for key in re.split(r'(?<!\\),', self.tab2_special_digits_entry.get()):
                if key.replace('\\', '').strip() == '':
                    continue
                item.append(key.replace('\\', '').strip())
            inp.append(item)
            
        if self.tab2_alpha_value.get():
            inp += ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        if self.tab2_alpha_small_value.get():
            inp += ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        if self.tab2_numbers_value.get():
            inp += ['0','1','2','3','4','5','6','7','8','9']
        self.statusbar.config(text='Generating Password...')
        
        print(inp)
        password = ''
        for i in range(number_rules):
            password += random.choice(inp)
        
        self.statusbar.config(text='Displaying Passwords...')
        
        self.tab2_password_list.clipboard_clear()
        self.tab2_password_list.clipboard_append(password)
       
        self.tab2_password_list.insert(tk.END, password)

        self.statusbar.config(text='password generated successfully')
        
    
window = tk.Tk()
Application(master=window)
window.mainloop()