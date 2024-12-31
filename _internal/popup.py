from customtkinter import *
import other

class C_popup(CTkToplevel):
    def __init__(self,master,message,title_,oui,func, **kwargs):
        super().__init__(master, **kwargs)
        self.title(title_)
        self.geometry("600x200")
        self.resizable(False,False)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        self.WasTopmost = False

        def validate():
            func()
            self.destroy()

        def get_dimensions():
            self.update_idletasks()
            row1= 0
            for widget in self.grid_slaves(row=1):
                row1 += widget.winfo_reqwidth()
            
            clmn0= 0
            for widget in self.grid_slaves(column=0):
                clmn0 += widget.winfo_reqheight()

            return max(self.lbl_mess.winfo_reqwidth(),row1),max(200,clmn0)
        

        self.lbl_mess = CTkLabel(self, text=message, font=("Roboto",16))
        self.lbl_mess.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        if oui == "oui":
            self.btn_oui = CTkButton(self,text="oui", font=("Roboto",16),command= validate)
            self.btn_oui.grid(row=1,column=0,padx=10,pady=10)

            self.btn_non = CTkButton(self,text="non", font=("Roboto",16), command= lambda: self.end(master))
            self.btn_non.grid(row=1,column=1,padx=10,pady=10)

        else:
            if func is None:
                self.btn_ok = CTkButton(self,text="ok", font=("Roboto",16), command= lambda: self.end(master))

            else:
                self.btn_ok = CTkButton(self,text="ok", font=("Roboto",16), command= validate)
            self.btn_ok.grid(row=1,column=0,columnspan=2,padx=10,pady=10)

        
        width,heigth = get_dimensions()
        self.geometry(f"{width}x{heigth}")  
        try:
            if master.wm_state():  
                master.wm_attributes("-topmost",False)
                self.WasTopmost = True
        except AttributeError:
            pass

        self.wm_attributes("-topmost",True)

    def end(self,master):
        self.destroy()
        if self.WasTopmost:
            master.wm_attributes("-topmost",True)
        
