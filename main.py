import subprocess
import tkinter.filedialog
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import re
import random
from threading import Thread
import time
from itertools import product

class Application:
    def __init__(self, master=None):
        self.counter=1
        self.master = master
        self.master.title('Advanced Password Generator')
        window.geometry("1000x700")
        ttk.Style().theme_use("xpnative")
        
        # Adding Menu Bar at the top of the window
        self.menubar = tk.Menu(self.master)
        self.menu_bar()
        self.master.config(menu=self.menubar)

        
        self.left_section = tk.Frame(self.master, borderwidth=0)
        self.left_section.pack(expand=1, padx=0, pady=0, side=tk.LEFT, fill=tk.BOTH)
        
        self.right_section = tk.Frame(self.master, borderwidth=0)
        self.right_section.pack(expand=1, padx=0, pady=0, side=tk.RIGHT, fill=tk.BOTH)
        
        self.statusbar = tk.Label(self.left_section, text="Ready", bd=1, padx=5, pady=5, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.current_password = 0
        self.rules_values = tk.Variable()
        
        self.add_new()
        self.control_rules()
        self.copy_export()
        self.Generated_passwords()
   
    def restart(self):
        self.clear_rules_list()
        self.password_list.delete(0, 'end')
    
    def menu_bar(self):
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.restart)
        filemenu.add_command(label="Open Rules", command=self.open_rules)
        filemenu.add_command(label="Open Passwords", command=self.open_passwords)
        filemenu.add_separator()
        filemenu.add_command(label="Save Rules", command=self.save_rules)
        filemenu.add_command(label="Save Passwords", command=self.save_passwords)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = tk.Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Documentation", command=self.documentation)
        helpmenu.add_command(label="Check for Updates...", command=quit)
        helpmenu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

    def about(self):
        tkinter.messagebox.showinfo(title='About', message='Created By Sameh Elalfi\nFor More Info: sameh.elalfi.mail@gmail.com')
    
    def documentation(self):
        subprocess.Popen('documentation.pdf',shell=True)
        
    def open_passwords(self):
        ftypes = [("text file", "*.txt"), ('All files', '*')]
        f = filedialog.askopenfilename(filetypes = ftypes)
        if f is '':
            return
        f = open(f, 'r', encoding='utf-8')
        passwords = f.readlines()
        self.password_list.delete(0, 'end')
        for password in passwords:
            self.password_list.insert(tk.END, password.strip())
    
    def open_rules(self):
        ftypes = [("text file", "*.txt"), ('All files', '*')]
        f = filedialog.askopenfilename(filetypes = ftypes)
        if f is '':
            return
        f = open(f, 'r', encoding='utf-8')
        rules = f.readlines()
        self.clear_rules_list()
        for rule in rules:
            self.rules_list.insert(tk.END, rule)

    def save_passwords(self):
        passwords = self.password_list.get(0, END)
        f = tk.filedialog.asksaveasfile(defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*") ))
        # asksaveasfile return `None` if dialog closed with "cancel".
        if f is None:
            return
        for password in passwords:
            f.write(password)
            f.write('\n')
        f.close()
        
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
        if len(text) > 0 and not text.endswith(','):
            text += ','
        if self.alpha_value.get():
            text += 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,'
        if self.alpha_small_value.get():
            text += 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,'
        if self.numbers_value.get():
            text += '0,1,2,3,4,5,6,7,8,9,'
        if text.strip():
            self.rules_list.insert(tk.END, text)
            self.add_digit_entry.delete(0,"end")
            
        # self.save_passwords()

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
        
        # for i in range(5):
        #     self.rules_list.insert(tk.END, 'sameh, ashraf, farouk,')
        
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
        try:
            if self.password_list.curselection():
                self.current_password = self.password_list.curselection()
            else:
                if type(self.current_password) == int:
                    text = self.password_list.get([self.current_password,])
                    
                elif type(self.current_password) != int:
                    if self.current_password[0] < self.password_list.size()-1:
                        self.current_password = self.current_password[0]+1
                
                self.password_list.selection_set(self.current_password)        
        
        except tk._tkinter.TclError:
            pass
        
        text = self.password_list.get(self.current_password)
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
                if type(self.current_password) == int:
                    text = self.password_list.get([self.current_password,])
                    
                elif type(self.current_password) != int:
                    if self.current_password[0]>0:
                        self.current_password = self.current_password[0]-1 
                self.password_list.selection_set(self.current_password)
        
        except tk._tkinter.TclError:
            pass

        text = self.password_list.get(self.current_password)
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
        rules = self.rules_values.get()
        
        # Split rules into lists
        inp = []
        for rule in rules:
            item = []
            for key in re.split(r'(?<!\\),', rule):
                if key.replace('\\', '').strip() == '':
                    continue
                item.append(key.replace('\\', '').strip())
            inp.append(item)
        
        # Remove duplicated Characters
        inp_temp = []
        for i in inp:
            inp_i = []
            for m in i:
                # all_lists = list(dict.fromkeys(i.split(',')))
                if m not in inp_i:
                    inp_i.append(m)
            inp_temp.append(inp_i)
        inp = inp_temp
        
        # Display a message box
        counter = 1
        for i in inp:
            # all_lists = list(dict.fromkeys(i.split(',')))
            counter *= len(i)
        m = messagebox.askyesno(title="Number of passwords", message='Do you want to save ' + str(counter) + ' passwords')
        if not m:
            return
        
        # Reverd the generated passwords
        if self.reverse_value.get():
            inp = sorted(inp, reverse=True)
            
        f = tk.filedialog.asksaveasfile(defaultextension=".txt", filetypes=(("text file", "*.txt"),("All Files", "*.*") ))
        # asksaveasfile return `None` if dialog closed with "cancel".
        if f is None:
            return
        self.thread2 = Thread(target=self.export_generator, args=(inp, f, '', len(inp)), daemon=True)
        self.thread2.start()

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
        
        copy_next_btn = ttk.Button(copy_and_export, text='Random', command=self.random)
        copy_next_btn.pack(expand=1, padx=20, pady=20, side=tk.LEFT, fill=tk.BOTH)

    def random(self):
        rules = self.rules_values.get()
        self.password_list.clipboard_clear()
        
        # Split rules into lists
        inp = []
        for rule in rules:
            item = []
            for key in re.split(r'(?<!\\),', rule):
                if key.replace('\\', '').strip() == '':
                    continue
                item.append(key.replace('\\', '').strip())
            inp.append(item)
        
        # Remove duplicated Characters
        inp_temp = []
        for i in inp:
            inp_i = []
            for m in i:
                if m not in inp_i:
                    inp_i.append(m)
            inp_temp.append(inp_i)
        inp = inp_temp
        password = ''
        for i in inp:
            password += random.choice(i)

        self.password_list.selection_clear(END)                
        self.password_list.insert(tk.END, password)
        self.password_list.clipboard_append(password)
        self.password_list.selection_set(self.password_list.size()-1)
        
    def Generated_passwords(self):
        paswords = ttk.LabelFrame(self.right_section, text='Generated Passwords')
        paswords.pack(expand=1, padx=20, pady=20, side=tk.LEFT, fill='both')
        
        self.password_list = tk.Listbox(paswords, selectmode='single', borderwidth=0)
        self.password_list.pack(expand=1, padx=10, pady=20, side=tk.RIGHT, fill=tk.BOTH)
        
        sc = tk.Scrollbar(self.password_list, orient="vertical")
        sc.pack(side=tk.RIGHT, fill=tk.Y)
        self.password_list.config(yscrollcommand=sc.set)
        sc.config(command=self.password_list.yview)
    
    def generator(self, inp):
        counter = 0
        for element in product(*inp):
            self.password_list.insert(tk.END, ''.join(element))
            counter+=1
            self.statusbar.config(text=str(counter) + ' passwords are generated successfully')
            
        # # empty lis
        # if len(ins) == 0:
        #     return

        # # list of one list
        # if type(ins[0]) is list and len(ins[0]) == 1:
        #     return

        # # For every item in the first list
        # for item in ins[0]:
            
        #     # if the length of final number is like we want
        #     if len(num+item) == length:
        #         # Do something
        #         self.password_list.insert(tk.END, num+item)
                
        #         self.counter += 1

        #     # Do the same to every list
        #     self.generator(ins[1:], num+item, length=length)
        # self.statusbar.config(text=str(self.counter-1) + ' passwords are generated successfully')
    
    def export_generator(self, ins, f, num='', length=''):
        # empty lis
        if len(ins) == 0:
            return

        # list of one list
        if type(ins[0]) is list and len(ins[0]) == 1:
            return

        # For every item in the first list
        for item in ins[0]:
            
            # if the length of final number is like we want
            if len(num+item) == length:
                # Do something
                f.write(num+item)
                f.write('\n')

            # Do the same to every list
            self.export_generator(ins[1:], f=f, num=num+item, length=length)
        self.statusbar.config(text=str(self.counter-1) + ' passwords are generated successfully')
        # f.close()
           
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
        
        # Split rules into lists
        inp = []
        for rule in rules:
            item = []
            for key in re.split(r'(?<!\\),', rule):
                if key.replace('\\', '').strip() == '':
                    continue
                item.append(key.replace('\\', '').strip())
            inp.append(item)
        
        # Remove duplicated Characters
        inp_temp = []
        for i in inp:
            inp_i = []
            for m in i:
                # all_lists = list(dict.fromkeys(i.split(',')))
                if m not in inp_i:
                    inp_i.append(m)
            inp_temp.append(inp_i)
        inp = inp_temp
        
        # Display a message box
        counter = 1
        for i in inp:
            # all_lists = list(dict.fromkeys(i.split(',')))
            counter *= len(i)
        m = messagebox.askyesno(title="Number of passwords", message='Do you want to generate ' + str(counter) + ' passwords')
        if not m:
            return
        
        # Reverd the generated passwords
        if self.reverse_value.get():
            inp2 = []
            for i in inp[::-1]:
                inp2.append(i)
            inp = inp2
            # the next function sometimes does not work
            # inp = sorted(inp, reverse=True)
        self.statusbar.config(text='Generating Passwords...')
        self.thread = Thread(target=self.generator, args=(inp,), daemon=True)
        self.thread.start()
        
window = tk.Tk()
Application(master=window)
window.mainloop()