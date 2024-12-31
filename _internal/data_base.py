from customtkinter import *
from PIL import Image
import other
from datetime import datetime
from openpyxl import load_workbook, Workbook

class C_dbase(CTkFrame):
    def __init__(self, root, master, **kwargs):
        super().__init__(master, **kwargs)

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=3)
        master.grid_rowconfigure(1, weight=1)

        self.top_level = None
        self.root = root

        self.frm_data = CTkFrame(master, border_width=5, corner_radius = 15)
        self.frm_data.grid(row=0,column=0,columnspan=2,padx=3,pady=(3,7),sticky="news")
        self.frm_data.grid_rowconfigure(0, weight=1)

        self.frm_data.grid_columnconfigure(0, weight=1)
        self.frm_data.grid_columnconfigure(1, weight=1)

        self.sfrm_list = CTkScrollableFrame(self.frm_data)
        self.sfrm_list.grid(row=0,column=0,padx=(10,10),pady=10,ipadx=3,sticky="nws")
        self.sfrm_list.grid_columnconfigure((0,1,2,3,4),weight=1)

        self.show_mbr()

        self.frm_filter = CTkFrame(self.frm_data)
        self.frm_filter.grid(row=0,column=1,padx=(10,10),pady=10)

        self.lbl_filtres = CTkLabel(self.frm_filter, text="Filtres :",font = ("Roboto",20))
        self.lbl_filtres.grid(row=0,column=7,padx=10,pady=10)

        self.ckb_homme = CTkCheckBox(self.frm_filter, onvalue=True, offvalue=False, text="Homme")
        self.ckb_homme.grid(row=1,column=7,padx=10,pady=10)
        self.ckb_homme.select()

        self.ckb_femme = CTkCheckBox(self.frm_filter, onvalue=True, offvalue=False, text="femme")
        self.ckb_femme.grid(row=2,column=7,padx=10,pady=10)
        self.ckb_femme.select()

        self.lbl_tri = CTkLabel(self.frm_filter, text="Tri :",font = ("Roboto",20))
        self.lbl_tri.grid(row=0,column=6,padx=10,pady=10)

        self.cbb_tri = CTkComboBox(self.frm_filter,state="readonly", values=["Alphabétique","Cronologique","Date de modification","Complétion"])
        self.cbb_tri.grid(row=1,column=6,padx=10,pady=10)
        self.cbb_tri.set("Alphabétique")

        self.swt_reverse = CTkSwitch(self.frm_filter, text="Ordre croissant")
        self.swt_reverse.grid(row=2,column=6,padx=10,pady=10)

        self.lbl_recherche = CTkLabel(self.frm_filter, text="Recherche :",font = ("Roboto",20))
        self.lbl_recherche.grid(row=0,column=5,padx=10,pady=10)

        self.cbb_nom = CTkComboBox(self.frm_filter,state="readonly", values=self.root.info[1])
        self.cbb_nom.grid(row=1,column=5,padx=10,pady=10)
        self.cbb_nom.set("Nom")

        self.ntr_prenom = CTkEntry(self.frm_filter, placeholder_text="Prénom")
        self.ntr_prenom.grid(row=2, column=5,padx=10,pady=10)

        self.lbl_blank = CTkLabel(self.frm_filter, fg_color="transparent", text= " ")
        self.lbl_blank.grid(row=3,column=7)

        reset = CTkImage(Image.open(f"{root.directory_path}\\assets\\reset.png"),size=(33,33))
        self.btn_reset = CTkButton(self.frm_filter, text="Réinitialiser", image=reset, fg_color="transparent", text_color=["gray20","white"], command=self.reset_filters)
        self.btn_reset.grid(row=4,column=7,padx=1,pady=1)

        self.btn_new = CTkButton(self.frm_filter, text="Nouveau membre", font=("Roboto",16),height=40,corner_radius=20, command = lambda: self.select_member(True,0,self.root))
        self.btn_new.grid(row=4,column=5,padx=10,pady=10)

        #bottom part
        self.frm_select = CTkFrame(master, border_width=5,corner_radius=15)
        self.frm_select.grid(row=1,column=0,padx=(3,7),pady=(7,3),sticky="news")
        self.frm_select.grid_columnconfigure(0, weight = 1)

        photo = CTkImage(Image.open(f"{root.directory_path}\\assets\\default.jpg"),size=(200,200))
        self.lbl_photo = CTkLabel(self.frm_select, image=photo, text="")
        self.lbl_photo.grid(row=0,column=0,rowspan=4,padx=10,pady=(20,10),sticky="news")

        self.lbl_selected_mb = CTkLabel(self.frm_select, text="Nouveau membre", font=("Roboto",30))
        self.lbl_selected_mb.grid(row=4,column=0,padx=10,pady=(10,0),sticky="news")
        
        self.lbl_last_modif = CTkLabel(self.frm_select, text="Dernière modification :", font = ("Roboto",25))
        self.lbl_last_modif.grid(row=2,column=2,padx=(10,20),pady=(10,5))

        self.lbl_date = CTkLabel(self.frm_select, text = "Le 03/04/2024 à 15:27", font=("Roboto", 17))
        self.lbl_date.grid(row=3,column=2,padx=(10,20),pady=0)

        self.lbl_avancement = CTkLabel(self.frm_select, text="Avancement de la complétion :", font = ("Roboto",25))
        self.lbl_avancement.grid(row=0,column=2,padx=(10,20),pady=(10,5))

        self.pgb_compl = CTkProgressBar(self.frm_select)
        self.pgb_compl.grid(row=1,column=2,padx=(10,20),pady=0)
        self.pgb_compl.set(0.75)

        modif_icon = CTkImage(Image.open(f"{root.directory_path}\\assets\\modification_g.png"),size=(33,33))
        self.btn_modif = CTkButton(self.frm_select,text=" Inspecter\n & modifier",image=modif_icon, font=("Roboto",30), corner_radius=20, command = lambda: self.start_edition(root))
        self.btn_modif.grid(row=0,column=1,rowspan=3,padx=10,pady=0)

        tarsh_icon = CTkImage(Image.open(f"{root.directory_path}\\assets\\trash_icon_r.png"),size=(29,33))
        self.btn_modif = CTkButton(self.frm_select,text="Supprimer",image=tarsh_icon, font=("Roboto",30), corner_radius=20)
        self.btn_modif.grid(row=3,column=1,rowspan=1,padx=10,pady=0)

        master.update_idletasks()
        self.sfrm_list.configure(width=self.sfrm_list.winfo_width())

        #export part
        self.frm_csv = CTkFrame(self.master,border_width=5, corner_radius = 15)
        self.frm_csv.grid(row=1,column=1,padx=(7,3),pady=(7,3),sticky="news")
        self.frm_csv.grid_rowconfigure(0, weight=1)
        self.frm_csv.grid_rowconfigure((1,2,3), weight=1)
        self.frm_csv.grid_rowconfigure(4, weight=1)

        self.btn_export = CTkButton(self.frm_csv, text="Exporter la base \nde donnée", font=("Roboto",20), command= self.exporter)
        self.btn_export.grid(row=1,column=0,padx=20,pady=10,sticky="ew")

        self.btn_import = CTkButton(self.frm_csv, text="Importer une base \nde donnée", font=("Roboto",20), command= lambda: other.message(self,"Importez uniquement une base de donnée conforme !",0,"ok",func=lambda:other.importer(root)))
        self.btn_import.grid(row=2,column=0,padx=20,pady=10,sticky="ew")

        self.btn_reset = CTkButton(self.frm_csv, text="Effacer la base \nde donnée", font=("Roboto",20), command = lambda: other.message(self,"Etes vous sûr de vouloir supprimer la base de données actuelle ?",0,"oui",func=lambda:other.clear_data(root)))
        self.btn_reset.grid(row=3,column=0,padx=20,pady=10,sticky="ew")

        master.bind("<Visibility>", lambda event: self.select_member(True,0,self.root))

    def exporter(self):
        wb = load_workbook(self.root.directory_path + "\\" + "data.xlsx")
        file_path = filedialog.asksaveasfilename(title="Enregistrer sous",initialfile="données",defaultextension=".xlsx",filetypes=[("Tous les fichiers", "*.*"),("Fichiers Excel", "*.xlsx")])
        if file_path != "":
            wb.save(file_path)

    def reset_filters(self):
        self.cbb_tri.set("Alphabétique")
        self.cbb_nom.set("Nom")
        self.ntr_prenom.delete(0, END)
        #self.swt_reverse

    def show_mbr(self): 
        for widget in self.sfrm_list.grid_slaves():
            widget.destroy()

        sorted_mbr = self.root.member_list #plus tard on trie

        lbl_nom = CTkLabel(self.sfrm_list, text="nom", font=("Roboto", 20),fg_color="#2b2b2b")
        lbl_nom.grid(row=0,column=0,padx=0,pady=0,sticky="we")

        lbl_prenom = CTkLabel(self.sfrm_list, text="prenom", font=("Roboto", 20),fg_color="#2b2b2b")
        lbl_prenom.grid(row=0,column=1,padx=0,pady=0,sticky="we")

        lbl_age = CTkLabel(self.sfrm_list, text="naiss.", font=("Roboto", 20),fg_color="#2b2b2b")
        lbl_age.grid(row=0,column=2,padx=0,pady=0,sticky="we")

        lbl_sexe = CTkLabel(self.sfrm_list, text="sexe", font=("Roboto", 20),fg_color="#2b2b2b",width=20)
        lbl_sexe.grid(row=0,column=3,padx=0,pady=0,sticky="we")

        lbl_completion = CTkLabel(self.sfrm_list, text="complé.", font=("Roboto", 20),fg_color="#2b2b2b")
        lbl_completion.grid(row=0,column=4,padx=0,pady=0,sticky="we")

        lbl_date =CTkLabel(self.sfrm_list, text= "modification", font=("Roboto", 20),fg_color="#2b2b2b")
        lbl_date.grid(row=0,column=5,padx=0,pady=0,sticky="we")

        for row,mbr in enumerate(sorted_mbr):

            lbl_nom = CTkLabel(self.sfrm_list, text=mbr.nom, font=("Roboto", 20))
            lbl_nom.grid(row=row+1,column=0,padx=0,pady=0,sticky="we")

            lbl_prenom = CTkLabel(self.sfrm_list, text=mbr.prenom1, font=("Roboto", 20))
            lbl_prenom.grid(row=row+1,column=1,padx=0,pady=0,sticky="we")

            lbl_age = CTkLabel(self.sfrm_list, text=mbr.date_n3, font=("Roboto", 20))
            lbl_age.grid(row=row+1,column=2,padx=0,pady=0,sticky="we")

            sexe = CTkImage(Image.open(f"{self.root.directory_path}\\assets\\{mbr.sexe}.png"))
            lbl_sexe = CTkLabel(self.sfrm_list, text="", image=sexe)
            lbl_sexe.grid(row=row+1,column=3,padx=0,pady=0,sticky="we")

            lbl_completion = CTkLabel(self.sfrm_list, text=str(int(mbr.completion))+"%", font=("Roboto", 20))
            lbl_completion.grid(row=row+1,column=4,padx=0,pady=0,sticky="we")

            if mbr.date == "Jamais modifié":
                lbl_date =CTkLabel(self.sfrm_list, text= mbr.date, font=("Roboto", 20))
            else:
                dt_obj = datetime.strptime(mbr.date, "Le %d/%m/%Y à %H:%M")
                lbl_date =CTkLabel(self.sfrm_list, text= dt_obj.strftime("%d/%m/%y"), font=("Roboto", 20))
            lbl_date.grid(row=row+1,column=5,padx=(2,5),pady=0,sticky="we")

        for child in self.sfrm_list.winfo_children():
            child.bind('<Enter>', self.hover)
            child.bind('<Leave>', self.out_hover)
            child.bind("<Button-1>", self.choose_member)

    def get_row(self,location):
        index = 80
        num = ""
        while index < len(location) and (location[index]).isnumeric():
            num += location[index]
            index += 1  

        if num == "":
            num = 1
        else:
            num = int(num)
        return (num-1)//6

    def hover(self,event):
        widget = event.widget
        row = self.get_row(str(widget))
        if row != 0:
            all_ = [wid for wid in self.sfrm_list.winfo_children()]
            for widg in all_:
                if self.get_row(str(widg)) == row:
                    widg.configure(fg_color = "grey")

    def out_hover(self,event):
        widget = event.widget
        row = self.get_row(str(widget))
        if row != 0:
            all_ = [wid for wid in self.sfrm_list.winfo_children()]
            for widg in all_:
                if self.get_row(str(widg)) == row:
                    widg.configure(fg_color = "#333333")

    def choose_member(self,event):
        widget = event.widget
        row = self.get_row(str(widget))
        self.select_member(False,row-1,self.root)

    def select_member(self,new,index,root):
        if new:
            self.selected_mb = other.create_member(self.root.info[0])

            self.lbl_selected_mb.configure(text="Nouveau membre")
            photo = CTkImage(Image.open(f"{root.directory_path}\\assets\\default.jpg"),size=(200,200))
            self.lbl_photo.configure(image=photo)
            self.pgb_compl.set(0)
            self.lbl_date.configure(text="Jamais modifié")

        else:
            self.selected_mb = self.root.member_list[index]

            self.lbl_selected_mb.configure(text=f'{self.selected_mb.nom} {self.selected_mb.prenom1}')
            if not self.selected_mb.picture is None:
                photo = CTkImage(Image.open(f"{root.directory_path}\\temp\\{self.selected_mb.picture}.png"),size=(200,200))
                
            else:
                photo = CTkImage(Image.open(f"{root.directory_path}\\assets\\default.jpg"),size=(200,200))
            self.lbl_photo.configure(image=photo)
            self.pgb_compl.set(self.selected_mb.completion/100)
            self.lbl_date.configure(text=self.selected_mb.date)
        self.root.opened = False

    def start_edition(self,root):
        root.selected_mb = self.selected_mb
        root.frm_tab.set("Éditeur")


