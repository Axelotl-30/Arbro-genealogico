from customtkinter import *
from PIL import Image
import search
import other
import subprocess
import tempfile
import popup
import shutil


class C_editor(CTkFrame):
    def __init__(self,root, master, **kwargs):
        super().__init__(master, **kwargs)
        master.grid_columnconfigure((0,2), weight=1)
        master.grid_columnconfigure(1, weight=3)
        master.grid_rowconfigure((0,1,2),weight=1)

        self.root = root
        self.top_level = None
        #juste pour initialiser
        self.selected_mb = self.root.selected_mb
        self.files_list = []
        self.photo_location = self.root.directory_path + "\\assets\\default.jpg"
        self.modifications = 0

        def tool_bar(event):
            root.swt_edit = CTkSwitch(root, text="Éditer", command= lambda: self.edit_action())
            root.swt_edit.place(x=20,y=22, anchor="w")
            root.swt_edit.select()

            self.update_idletasks()
            offset = root.swt_edit.winfo_width()

            save = CTkImage(Image.open(f"{self.root.directory_path}\\assets\\save.png"), size=(28,28))
            root.btn_save = CTkButton(root, image=save,width=28, text="", fg_color="transparent", text_color=["gray20","white"],hover=False, command = lambda: other.save(self))
            root.btn_save.place(x = offset, y=22, anchor="w")

            self.update_idletasks() 
            offset += root.btn_save.winfo_width()

            dot = CTkImage(Image.open(f"{self.root.directory_path}\\assets\\dot {self.modifications}.png"), size=(28,28))
            root.lbl_dot = CTkLabel(root, image=dot, text="", fg_color="transparent")
            root.lbl_dot.place(x = offset, y=22, anchor="w")

        master.bind("<Visibility>", lambda event: other.open_member(self, event)) 
        master.bind("<Visibility>", tool_bar)

        #etat civil
        self.frm_civil = CTkFrame(master, border_width=5, corner_radius = 15)
        self.frm_civil.grid(row=0,column=1,columnspan=2,padx=(7,3),pady=(3,7),sticky="news")

        self.lbl_prenom = CTkLabel(self.frm_civil, text="Prénoms",font=("Roboto",20))
        self.lbl_prenom.grid(row=0,column=1,padx=10,pady=10)

        self.lbl_nom = CTkLabel(self.frm_civil, text="Nom",font=("Roboto",20))
        self.lbl_nom.grid(row=0,column=0,padx=10,pady=10)

        self.lbl_metier = CTkLabel(self.frm_civil, text="Métier", font=("Roboto",20))
        self.lbl_metier.grid(row=0,column=2,padx=10,pady=10)

        self.lbl_sexe = CTkLabel(self.frm_civil, text="Sexe", font=("Roboto",20))
        self.lbl_sexe.grid(row=0,column=3,padx=10,pady=10)

        self.ntr_prenom1 = CTkEntry(self.frm_civil, placeholder_text="Inconnu")
        self.ntr_prenom1.grid(row=1,column=1,padx=10,pady=5)

        self.ntr_prenom2 = CTkEntry(self.frm_civil, placeholder_text="Inconnu")
        self.ntr_prenom2.grid(row=2,column=1,padx=10,pady=5)

        self.ntr_prenom3 = CTkEntry(self.frm_civil, placeholder_text="Inconnu")
        self.ntr_prenom3.grid(row=3,column=1,padx=10,pady=(5,10))

        self.cbb_nom = CTkComboBox(self.frm_civil, values=self.root.info[1])
        self.cbb_nom.grid(row=1,column=0,padx=10,pady=5)
        self.cbb_nom.set(self.selected_mb.nom)

        self.lbl_nom_usage = CTkLabel(self.frm_civil, text="Nom d'usage")
        self.lbl_nom_usage.grid(row=2,column=0,padx=10,pady=5)

        self.cbb_nom_usage = CTkComboBox(self.frm_civil, values=self.root.info[1])
        self.cbb_nom_usage.grid(row=3,column=0,padx=10,pady=(5,10))
        self.cbb_nom.set(self.selected_mb.nom_usage)

        self.ntr_metier = CTkEntry(self.frm_civil, placeholder_text="Inconnu")
        self.ntr_metier.grid(row=1,column=2,padx=10,pady=5)

        self.sexe_var = StringVar(value="homme")
        self.rbtn_homme = CTkRadioButton(self.frm_civil,text="Homme", variable= self.sexe_var, value = "homme")
        self.rbtn_homme.grid(row=1,column=3,padx=10,pady=5)

        self.rbtn_femme = CTkRadioButton(self.frm_civil,text="Femme", variable= self.sexe_var, value = "femme")
        self.rbtn_femme.grid(row=2,column=3,padx=10,pady=5)

        self.rbtn_homme.select() #pourquoi pas 

        #photo
        self.frm_photo = CTkFrame(master, border_width=5, corner_radius = 15)
        self.frm_photo.grid(row=0,column=0,padx=(3,7),pady=(3,7),sticky="news")

        photo = self.resize_photo(self.photo_location)
        self.btn_photo = CTkButton(self.frm_photo, image=photo, text="",border_width=0,fg_color="transparent",hover=False, command= lambda:self.select_photo())
        self.btn_photo.grid(row=0,column=0,rowspan=4,padx=10,pady=10,sticky="news")

        self.lbl_comple = CTkLabel(self.frm_photo, text="Complétion", font=("Roboto",20))
        self.lbl_comple.grid(row=0,column=2,padx=10,pady=10)

        red_cross = CTkImage(Image.open(f"{self.root.directory_path}\\assets\\cross.png"))
        self.btn_supp_photo = CTkButton(self.frm_photo,image = red_cross, text="",border_width=0,fg_color="transparent",hover=False, command= lambda: self.select_photo(f"{self.root.directory_path}\\data\\assets\\default.jpg"), width=20)
        self.btn_supp_photo.grid(row=0,column=1,padx=(0,20))

        self.pbar_comple = CTkProgressBar(self.frm_photo)
        self.pbar_comple.grid(row=1,column=2,padx=10,pady=5)
        self.pbar_comple.set(0)

        self.lbl_percent = CTkLabel(self.frm_photo, text="0%", font=("Roboto",20))
        self.lbl_percent.grid(row=2,column=2,padx=10,pady=5)

        #filiation
        self.frm_filiation = CTkFrame(master, border_width=5, corner_radius = 15)
        self.frm_filiation.grid(row=1,column=2,rowspan=2,padx=(7,3),pady=(7,3),sticky="news")

        self.lbl_pere = CTkLabel (self.frm_filiation, text="Père", font=("Roboto",20))
        self.lbl_pere.grid(row=0,column=0,padx=10,pady=10)

        self.lbl_mere = CTkLabel (self.frm_filiation, text="Mère", font=("Roboto",20))
        self.lbl_mere.grid(row=0,column=1,padx=10,pady=10)

        self.ckb_conjoint = CTkCheckBox(self.frm_filiation, text="Conjoint", font=("Roboto",20), command = lambda: self.checkbox_action(0))
        self.ckb_conjoint.grid(row=2,column=1,padx=10,pady=10)
        self.ckb_conjoint.select()

        self.lbl_enfant = CTkLabel(self.frm_filiation, text="Enfant", font=("Roboto",20))
        self.lbl_enfant.grid(row=2,column=0,padx=10,pady=10)

        self.btn_pere = CTkButton(self.frm_filiation, text=self.selected_mb.pere, command= lambda: self.open_toplevel(0,self.root.member_list,"Père"))
        self.btn_pere.grid(row=1,column=0,padx=10,pady=10)

        self.btn_mere = CTkButton(self.frm_filiation, text=self.selected_mb.mere, command= lambda:self.open_toplevel(1,self.root.member_list,"Mère"))
        self.btn_mere.grid(row=1,column=1,padx=10,pady=10)

        self.btn_conjoint = CTkButton(self.frm_filiation, text=self.selected_mb.conjoint if self.selected_mb.conjoint != "disabled" else "", command= lambda:self.open_toplevel(2,self.root.member_list,"Conjoint"))
        self.btn_conjoint.grid(row=3,column=1,padx=10,pady=10)

        self.lbl_enfant = CTkLabel(self.frm_filiation, text="Enfant", font=("Roboto",20))
        self.lbl_enfant.grid(row=2,column=0,padx=10,pady=10)

        self.btn_pere = CTkButton(self.frm_filiation, text=self.selected_mb.pere, command= lambda: self.open_toplevel(0,self.root.member_list,"Père"))
        self.btn_pere.grid(row=1,column=0,padx=10,pady=10)

        self.btn_mere = CTkButton(self.frm_filiation, text=self.selected_mb.mere, command= lambda:self.open_toplevel(1,self.root.member_list,"Mère"))
        self.btn_mere.grid(row=1,column=1,padx=10,pady=10)

        self.btn_conjoint = CTkButton(self.frm_filiation, text=self.selected_mb.conjoint if self.selected_mb.conjoint != "disabled" else "", command= lambda:self.open_toplevel(2,self.root.member_list,"Conjoint"))
        self.btn_conjoint.grid(row=3,column=1,padx=10,pady=10)

        self.btn_add_child = CTkButton(self.frm_filiation, text="Ajouter")
        self.btn_add_child.grid(row=3,column=0,padx=10,pady=10)

        #dates et lieux
        self.frm_date_lieu = CTkFrame(master, border_width=5, corner_radius = 15)
        self.frm_date_lieu.grid(row=1,column=0,columnspan=2,padx=(3,7),pady=7,sticky="news")

        self.lbl_date = CTkLabel(self.frm_date_lieu, text="Date", font=("Roboto",20))
        self.lbl_date.grid(row=0,column=1,columnspan=3,padx=10,pady=10)

        self.lbl_departement = CTkLabel(self.frm_date_lieu, text="Département", font=("Roboto",20))
        self.lbl_departement.grid(row=0,column=4,padx=10,pady=10)

        self.lbl_commune = CTkLabel(self.frm_date_lieu, text="Commune", font=("Roboto",20))
        self.lbl_commune.grid(row=0,column=5,padx=10,pady=10)

        self.lbl_naissance = CTkLabel(self.frm_date_lieu, text="Naissance", font=("Roboto",20))
        self.lbl_naissance.grid(row=1,column=0,padx=10,pady=10)

        self.ckb_mariage = CTkCheckBox(self.frm_date_lieu, text="Mariage", font=("Roboto",20), command = lambda: self.checkbox_action(1))
        self.ckb_mariage.grid(row=2,column=0,padx=10,pady=10)
        self.ckb_mariage.select()

        self.ckb_deces = CTkCheckBox(self.frm_date_lieu, text="Décès", font=("Roboto",20), command = lambda:self.checkbox_action(2))
        self.ckb_deces.grid(row=3,column=0,padx=10,pady=10)
        self.ckb_deces.select()

        self.ntr_dn1 = CTkEntry(self.frm_date_lieu, placeholder_text="??",width=30)
        self.ntr_dn1.grid(row=1,column=1,padx=(10,1),pady=10)
        self.ntr_dn1.bind('<KeyRelease>',lambda event: self.focus_date(event))

        self.ntr_dn2 = CTkEntry(self.frm_date_lieu, placeholder_text="??",width=30)
        self.ntr_dn2.grid(row=1,column=2,pady=10)
        self.ntr_dn2.bind('<KeyRelease>',lambda event:self.focus_date(event))
        self.ntr_dn2.bind('<BackSpace>',lambda event:self.back_focus_date(event))

        self.ntr_dn3 = CTkEntry(self.frm_date_lieu, placeholder_text="???",width=45)
        self.ntr_dn3.grid(row=1,column=3,padx=(1,10),pady=10)
        self.ntr_dn3.bind('<BackSpace>',lambda event:self.back_focus_date(event))
        self.ntr_dn3.bind('<KeyRelease>',lambda event:self.block_year_len(event))

        self.btn_dn = CTkButton(self.frm_date_lieu, text=self.selected_mb.departement_n, command= lambda:self.open_toplevel(0,self.root.depart_list,"Département de naissance"))
        self.btn_dn.grid(row=1,column=4,padx=10,pady=10)

        self.ntr_cn = CTkEntry(self.frm_date_lieu, placeholder_text="Inconnu")
        self.ntr_cn.grid(row=1,column=5,padx=10,pady=10)

        self.ntr_dm1 = CTkEntry(self.frm_date_lieu, placeholder_text="??",width=30)
        self.ntr_dm1.grid(row=2,column=1,padx=(10,1),pady=10)
        self.ntr_dm1.bind('<KeyRelease>',lambda event:self.focus_date(event))

        self.ntr_dm2 = CTkEntry(self.frm_date_lieu, placeholder_text="??",width=30)
        self.ntr_dm2.grid(row=2,column=2,pady=10)
        self.ntr_dm2.bind('<KeyRelease>',lambda event:self.focus_date(event))
        self.ntr_dm2.bind('<BackSpace>',lambda event:self.back_focus_date(event))

        self.ntr_dm3 = CTkEntry(self.frm_date_lieu, placeholder_text="????",width=45)
        self.ntr_dm3.grid(row=2,column=3,padx=(1,10),pady=10)
        self.ntr_dm3.bind('<BackSpace>',lambda event:self.back_focus_date(event))
        self.ntr_dm3.bind('<KeyRelease>',lambda event:self.block_year_len(event))

        self.btn_dm = CTkButton(self.frm_date_lieu, text=self.selected_mb.departement_m, command= lambda:self.open_toplevel(1,self.root.depart_list,"Département de mariage"))
        self.btn_dm.grid(row=2,column=4,padx=10,pady=10)

        self.ntr_cm = CTkEntry(self.frm_date_lieu, placeholder_text="Inconnu")
        self.ntr_cm.grid(row=2,column=5,padx=10,pady=10)

        self.ntr_dd1 = CTkEntry(self.frm_date_lieu, placeholder_text="??",width=30)
        self.ntr_dd1.grid(row=3,column=1,padx=(10,1),pady=10)
        self.ntr_dd1.bind('<KeyRelease>',lambda event:self.focus_date(event))

        self.ntr_dd2 = CTkEntry(self.frm_date_lieu, placeholder_text="??",width=30)
        self.ntr_dd2.grid(row=3,column=2,pady=10)
        self.ntr_dd2.bind('<KeyRelease>',lambda event:self.focus_date(event))
        self.ntr_dd2.bind('<BackSpace>',lambda event:self.back_focus_date(event))

        self.ntr_dd3 = CTkEntry(self.frm_date_lieu, placeholder_text="????",width=45)
        self.ntr_dd3.grid(row=3,column=3,padx=(1,10),pady=10)
        self.ntr_dd3.bind('<BackSpace>',lambda event:self.back_focus_date(event))
        self.ntr_dd3.bind('<KeyRelease>',lambda event:self.block_year_len(event))

        self.btn_dd = CTkButton(self.frm_date_lieu, text=self.selected_mb.departement_d, command= lambda:self.open_toplevel(2,self.root.depart_list,"Département de décès"))
        self.btn_dd.grid(row=3,column=4,padx=10,pady=10)

        self.ntr_cd = CTkEntry(self.frm_date_lieu, placeholder_text="Inconnu")
        self.ntr_cd.grid(row=3,column=5,padx=10,pady=10)

        #file manager
        self.frm_file_manager = CTkFrame(master, border_width=5, corner_radius = 15)
        self.frm_file_manager.grid(row=2,column=0,columnspan=2,padx=(3,7),pady=(7,3),sticky="news")

        self.sfrm_file = CTkScrollableFrame(self.frm_file_manager,width=300)
        self.sfrm_file.grid(row=0,column=0,rowspan=3,padx=10,pady=10,sticky="news")
        self.sfrm_file.grid_columnconfigure((0,1),weight=1)

        self.frm_read = CTkFrame(self.frm_file_manager)
        self.frm_read.grid(row=2,column=1)

        self.btn_read = CTkButton(self.frm_read, text="Voir", command = self.read_file)
        self.btn_read.grid(row=2,column=1,padx=10,pady=10)

        self.btn_supp = CTkButton(self.frm_read, text="Supprimer", command = self.delete_file)
        self.btn_supp.grid(row=2,column=2,padx=10,pady=10)

        self.frm_add = CTkFrame(self.frm_file_manager)
        self.frm_add.grid(row=0,column=1)

        self.btn_enr_all = CTkButton(self.frm_add, text="Enregistrer tout", command = self.select_repertory)
        self.btn_enr_all.grid(row=1,column=1,padx=10,pady=10)

        self.btn_add_file = CTkButton(self.frm_add, text="Ajouter un fichier", command= self.addup_file)
        self.btn_add_file.grid(row=0,column=0,padx=10,pady=10)

        for widget in (self.cbb_nom, self.cbb_nom_usage, self.ntr_dd1, self.ntr_dd2, self.ntr_dd3, self.ntr_dm1, self.ntr_dm2, self.ntr_dm3, self.ntr_dn1, self.ntr_dn2, self.ntr_dn3, self.ntr_prenom1, self.ntr_prenom2, self.ntr_prenom3, self.ntr_cn, self.ntr_cm, self.ntr_cd, self.ntr_metier):
            widget.bind("<FocusOut>", lambda event:self.check_completion(event))

    def id_to_text(self,origin_btn,id_):
        linked_member = None
        for member in self.root.member_list:
            if member.column == id_:
                linked_member = member
        
        if linked_member is not None:
            origin_btn.configure(text=f"{linked_member.nom}|{linked_member.prenom1}|{linked_member.date_n3}")

        else:
            origin_btn.configure(text="Inconnu")

    def link_members(self,val,index):
        vals = val.split("|")
        id_list = [self.id_pere, self.id_mere, self.id_conjoint]
        for member in self.root.member_list:
            if [member.nom, member.prenom1, member.date_n3] == vals:
                id_list[index] = member.column
                print("oui:",id_list[index],self.id_pere)

    def check_completion(self,event=None):
        data = vars(self.selected_mb)
        total = 0
        n = 0
        for key,val in other.get_dict(self).items():
            if val != "disabled" and key not in ("completion", "date","column","notes_l","photo_l"):

                if key[:4] == "date":
                    total += 0.333 
                    if val != "Inconnu":
                        n += 0.333  

                elif key == "picture":
                    total += 1
                    if val != None:
                        n += 1
                
                else:
                    total += 1 
                    if val != "Inconnu":
                        n += 1

                if val != data[key]:
                    #print(val,key)
                    if self.modifications == 0:
                        self.modifications = 1
                        if self.root.lbl_dot.winfo_exists():
                            self.change_dot()                

        value = n/total
        self.pbar_comple.set(value)
        self.lbl_percent.configure(text=str(int(value*100))+"%")

    def change_dot(self):
        dot = CTkImage(Image.open(f"{self.root.directory_path}\\assets\\dot {self.modifications}.png"), size=(28,28))
        self.root.lbl_dot.configure(image=dot)

    def select_repertory(self):
        return
        d_path = filedialog.askdirectory(title="Enregistrer les fichier")
        if d_path != "":
            for photo in self.selected_mb.photo_l:
                img = Image.open(self.root.directory_path+"\\temp\\"+photo)

    def addup_file(self):
        return
        file_path = filedialog.askopenfilename(title="Ouvrir une fichier")
        if file_path != "":
            self.files_add.append(file_path)
            other.show_files(self)
            self.file_modif()

    def read_file(self):
        return
        if "photo" in self.sld_file:
            index = int(self.sld_file[5:]) - (0 if not self.selected_mb.picture is None else 1)

            img = Image.open(f"{self.root.directory_path}\\temp\\{self.photo_l[index]}")
            img.show()

        else: #note
            index = int(self.sld_file[4:])-1

            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                temp_file.write((self.notes_l[index]).encode('utf-8'))
                temp_file_path = temp_file.name

            subprocess.run(['notepad.exe', temp_file_path])

    def delete_file(self):
        return
        if "photo" in self.sld_file:
            index = self.selected_mb.photo_l.index(self.sld_file[5:])

        else: #note
            index = self.selected_mb.notes_l.index(self.sld_file)
        
    def choose_file(self):
        return

    def focus_date(self,event):
        widget = event.widget 
        date = widget.get() 

        if len(date) > 2 and event.keysym != "BackSpace":
            nextwidget = widget.winfo_parent()
            nextwidget = (nextwidget[:-1] + str(int(nextwidget[-1])+1)) if nextwidget[-1] != "y" else nextwidget+"2"
            nextwidget = self.master.nametowidget(nextwidget)
            widget.delete(2,END)
            if event.keysym in ("1","2","3","4","5","6","7","8","9","0"):
                len_next = len(nextwidget.get())
                if len_next < 2:
                    nextwidget.insert(len_next,event.keysym)
            nextwidget.focus_set()
                    
        elif event.keysym not in ("1","2","3","4","5","6","7","8","9","0","Shift", "Control", "Alt", "Caps_Lock", "Tab", "BackSpace", "Return", "Enter", "Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Left", "Up", "Right", "Down", "Home", "End", "Page_Up", "Page_Down", "Insert", "Delete", "Pause", "Break", "Print", "Scroll_Lock", "Num_Lock"):
            widget.delete(len(date)-1,len(date))

    def back_focus_date(self,event):
        widget = event.widget 
        date = widget.get() 

        if len(date) == 0 and event.keysym == "BackSpace":
            nextwidget = widget.winfo_parent()
            nextwidget = (nextwidget[:-1] + str(int(nextwidget[-1])-1)) if nextwidget[-1] != "2" else nextwidget[:-1]
            nextwidget = self.master.nametowidget(nextwidget)
            nextwidget.focus_set()

    def block_year_len(self,event):
        widget = event.widget 
        date = widget.get() 

        if len(date) > 4 and event.keysym != "BackSpace":
            widget.delete(4,END)

        elif event.keysym not in ("1","2","3","4","5","6","7","8","9","0","Shift", "Control", "Alt", "Caps_Lock", "Tab", "BackSpace", "Return", "Enter", "Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Left", "Up", "Right", "Down", "Home", "End", "Page_Up", "Page_Down", "Insert", "Delete", "Pause", "Break", "Print", "Scroll_Lock", "Num_Lock"):
            widget.delete(len(date)-1,len(date))
    
    def open_toplevel(self,index,liste,title):
        if self.top_level is None or not self.top_level.winfo_exists():
            self.top_level = search.C_top_search(self,self.root.directory_path,self.root.scale,index,liste,title)

        else:
            self.top_level.focus()

    def checkbox_action(self,checkbox_i):
        ckb = (self.ckb_conjoint, self.ckb_mariage, self.ckb_deces)[checkbox_i]

        widgets = ([self.btn_conjoint],[self.btn_dm, self.ntr_dm1, self.ntr_dm2, self.ntr_dm3, self.ntr_cm],[self.btn_dd, self.ntr_dd1, self.ntr_dd2, self.ntr_dd3, self.ntr_cd])[checkbox_i]

        if ckb.get():
            self.enable(widgets)
                
        else:
            self.disable(widgets) 

    def enable(self,widget_list):
        for widget in widget_list:
            widget.configure(state="normal")

    def disable(self,widget_list):
        self.rbtn_homme.focus()
        self.update_idletasks()
        for widget in widget_list:
            if isinstance(widget, (CTkEntry, CTkComboBox)):
                widget.configure(state="readonly") 

            elif isinstance(widget, (CTkButton, CTkCheckBox)):
                widget.configure(state="disabled") 

    def resize_photo(self,path):
        photo = Image.open(path)
        largeur, hauteur = photo.size
        nouvelle_largeur = 150
        nouvelle_hauteur = 150

        if largeur > hauteur:
            nouvelle_hauteur = int(hauteur * nouvelle_largeur / largeur)
        elif largeur < hauteur:
            nouvelle_largeur = int(largeur * nouvelle_hauteur / hauteur)

        return CTkImage(photo,size=(nouvelle_largeur,nouvelle_hauteur))
    
    def select_photo(self, path=None):
        if path is None:
            file_path = filedialog.askopenfilename(title="Ouvrir une image", filetypes=[("Images", ("*.png"," *.jpg","*.jpeg","*.ico","*.gif","*.bmp","*.svg"))])
        else:
            file_path = path

        if file_path != "":
            self.photo_location = file_path
            photo = self.resize_photo(file_path)
            self.btn_photo.configure(image=photo)