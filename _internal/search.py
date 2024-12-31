from customtkinter import *
from PIL import Image
import difflib

class C_top_search(CTkToplevel):
    def __init__(self,master,directory_path,scale,index, liste, title_, **kwargs):
        super().__init__(master, **kwargs)
        self.title(title_)
        self.geometry(f"{600*scale}x{295*scale}")
        self.resizable(False,False)
        self.scale = scale
        if title_ in ("Département de naissance","Département de mariage","Département de décès"):
            self.liste = [ num + " " +depart for num,depart in liste.items()]
            self.origin_btn = (master.btn_dn,master.btn_dm,master.btn_dd)

        else:
            self.liste = [f"{member.nom}|{member.prenom1}|{member.date_n3}" for member in liste]
            self.origin_btn = (master.btn_pere,master.btn_mere,master.btn_conjoint)
        self.origin_btn = self.origin_btn[index]

        def validate(val):
            if title_ not in ("Département de naissance","Département de mariage","Département de décès"):
                master.link_members(val,index)
            self.origin_btn.configure(text=val)
            master.check_completion()
            self.destroy()

        self.ntr_search = CTkEntry(self, placeholder_text="Rechercher")
        self.ntr_search.grid(row=0,column=0,padx=10,pady=(10,5),sticky="ew")
        self.ntr_search.bind("<Return>", lambda event: self.update_button())

        loupe = CTkImage(Image.open(f"{directory_path}\\assets\\loupe.png"))
        self.btn_loupe = CTkButton(self, text="", image=loupe, width=50, command= self.update_button)
        self.btn_loupe.grid(row=0,column=1,padx=10,pady=(10,5))

        self.sfrm_list = CTkScrollableFrame(self,width=210,border_width=5)
        self.sfrm_list.grid(row=1,column=0,columnspan=2,rowspan=3,padx=10,pady=(5,10))

        self.ntr_autre = CTkEntry(self, placeholder_text="Autre")
        self.ntr_autre.grid(row=0,column=2,padx=(30,10),pady=(10,5), sticky="ew")
        self.ntr_autre.bind("<Return>", lambda event: self.select(self.ntr_autre))

        verify = CTkImage(Image.open(f"{directory_path}\\assets\\verify.png"))
        self.btn_verify = CTkButton(self,text="", image=verify, width=30, fg_color="transparent",command = lambda btn=self.ntr_autre: self.select(btn))
        self.btn_verify.grid(row=0,column=3,padx=10,pady=10, sticky="w")

        self.lbl_depn = CTkLabel(self, text=title_+" :", font=("Roboto", 20))
        self.lbl_depn.grid(row=1,column=2,columnspan=2,padx=10,pady=10)

        self.lbl_selected = CTkLabel(self, text=self.origin_btn.cget("text"), font=("Roboto", 30))
        self.lbl_selected.grid(row=2,column=2,columnspan=2,padx=10,pady=10)

        self.btn_valider = CTkButton(self, text="Valider", font=("Roboto", 16),corner_radius=20, command = lambda *args: validate(self.lbl_selected.cget("text")))
        self.btn_valider.grid(row=3,column=2,padx=10,pady=10)

        self.btn_annuler = CTkButton(self, text="Annuler", font=("Roboto", 16),corner_radius=20, command = self.destroy)
        self.btn_annuler.grid(row=3,column=3,padx=10,pady=10)

        self.update_button()
        self.update_idletasks()
        self.get_grid_width()
        self.wm_attributes("-topmost",True)

    def get_grid_width(self):
        self.width = self.lbl_selected.winfo_reqwidth() + (250*self.scale)
                
        self.geometry(f"{max(self.width,600*self.scale)}x{295*self.scale}")

    def update_button(self):
        for widget in self.sfrm_list.pack_slaves():
            widget.destroy()

        for d in self.trier_par_proximite(self.liste, self.ntr_search.get()):
            button = CTkButton(self.sfrm_list,text_color=["gray14", "gray84"],text=d,width=200,anchor="w")
            button.configure(command= lambda btn=button: self.select(btn))
            button.pack()

    def select(self,btn):
        text_ = btn.cget("text") if isinstance(btn, CTkButton) else btn.get()
        if text_ != "":
            self.lbl_selected.configure(text=text_) 
        self.after(100, self.get_grid_width)

    def trier_par_proximite(self,liste, chaine_entree):
        # Utiliser difflib pour obtenir les ratios de similarité
        ratios = [(chaine, difflib.SequenceMatcher(None, chaine, chaine_entree).ratio()) for chaine in liste]
        # Trier la liste en fonction des ratios de similarité
        ratios_tries = sorted(ratios, key=lambda x: x[1], reverse=True)
        # Extraire les chaînes triées
        liste_trie = [chaine for chaine, ratio in ratios_tries]
        return liste_trie