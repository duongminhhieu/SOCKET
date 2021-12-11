import re
import socket
import threading
import tkinter as tk
import time
import os
from PIL import ImageTk, Image
from Constants import *


"""Lấy ảnh của chương trình"""
class AddImage:
    def __init__(self):
        return
    
    def get(name):
        if name in IMG_LIST:
            if IMG_LIST[name][1] is None:
                
                IMG_LIST[name][1] = ImageTk.PhotoImage(file=IMG_LIST[name][0])
                return IMG_LIST[name][1]
            else:
                return IMG_LIST[name][1]
        return None



"""Hàm căn giữa màn hình"""
def center(master,app_width,app_height):
    SCREEN_HEIGHT = master.winfo_screenheight()
    SCREEN_WIDTH = master.winfo_screenwidth()
    
    x = (SCREEN_WIDTH/2) - (app_width/2)  
    y = (SCREEN_HEIGHT/2) - (app_height/2)
    
    master.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")   

"""Thanh tiến trình"""
class LoadingScreen():
    def __init__(self,master,*args,**kwargs):
        if "time_line" in kwargs:
            self.time_line = kwargs.get("time_line")
        else:
            self.time_line = 5
        self.root = tk.Toplevel(master)
        self.master = master
        self.master.withdraw()
        self.app_width = 350
        self.app_height = 80
        self.root.resizable(False, False)
        
        """Căn thanh loading giữa màn hình"""
        center(self.root,self.app_width,self.app_height)
        self.root.wm_attributes("-transparentcolor",self.root["bg"])
        self.root.overrideredirect(1)
        
        self.frame = tk.Frame(self.root,width = 200,height = 28)
        self.frame.place(x = 100,y = 35 )
        tk.Label(self.frame,text= "Shutting down...",fg = "#528B8B",font= "Helvetica").place(x = 0,y=0)
        for i in range(16):
            tk.Label(self.root,bg ="#000",width = 2, height = 1).place(x =(i)*22,y = 10)

        self.root.update()
        self.thread = threading.Thread(target =self.play_animation)
        self.thread.setDaemon(True)
        self.thread.start()
        self.root.after(20, self.check_thread)
  
    def play_animation(self): 
        for i in range(self.time_line):
            if i != self.time_line - 1:   
                for j in range(16):
                    tk.Label(self.root,bg ="#F7E815",width = 2, height = 1).place(x =(j)*22,y = 10)
                    time.sleep(0.02)
                    self.root.update_idletasks() # update lại thanh
                    tk.Label(self.root,bg ="#000",width = 2, height = 1).place(x =(j)*22,y = 10)
            else:
                for j in range(16):
                    tk.Label(self.root,bg ="#F7E815",width = 2, height = 1).place(x =(j)*22,y = 10)
                    time.sleep(0.02)
                    self.root.update_idletasks()
                
    def check_thread(self):
        if self.thread.is_alive():
            self.root.after(20, self.check_thread)
        else:
            self.root.destroy() 
            self.master_exit()
            
    def master_exit(self):
        self.master.destroy()
        os._exit(1)



"""Trang chính của chương trình"""    

class MainPage:
    def __init__(self,master):
        self.root = master
        self.root.title("HOSTING SERVER")
        self.root.iconbitmap(f"{ICON}")
        self.disconnect_flag = False
        
        """Kích thước của app"""
        self.app_height = 400
        self.app_width = 621

        center(self.root,self.app_width,self.app_height)

        self.messages_frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.status_list = tk.Listbox(self.messages_frame,width = 100,height = 22,yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.status_list.pack()

        self.messages_frame.pack()
       
        self.quit_but = tk.Button(self.root,text = "Quit",width = 30,command = self.on_closing)
        #img = AddImage.get("BUTTON_QUIT")
        #self.quit_but.config(image=img)
        self.quit_but.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    """Set cờ khi server muốn dừng kết nối"""
    def set_disconnect_flag(self,bool):
        self.disconnect_flag = bool
    
    """Hàm để lấy cái cờ ngắt kết nối ra khỏi đối tượng"""
    def get_disconnect_flag(self):
        return self.disconnect_flag
    
    """Hàm nhập vào ô text box hiện thông tin"""
    def insert_to_text_box(self,msg):
        self.status_list.insert(tk.END,msg)
    
    """Hàm khi tắt server"""
    def on_closing(self):
        self.set_disconnect_flag(True)  
        """Giao diện tắt server"""
        self.loading = LoadingScreen(self.root,time_line = 5)
  