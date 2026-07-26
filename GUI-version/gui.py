import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from patient import Patient
from file_handler import load_patients, save_patients

# ---------------------------------------------------------------------------
# Color Palette — Dark clinical theme
# ---------------------------------------------------------------------------
BG        = "#0a1420"
BG_PANEL  = "#101d2c"
BG_FIELD  = "#0c1826"
BORDER    = "#1e3348"
TEAL      = "#2fd6c0"
TEAL_DIM  = "#173d38"
AMBER     = "#e8a944"
RED       = "#e2695f"
TEXT_HI   = "#eaf2f5"
TEXT_MID  = "#9fb4c4"
TEXT_LOW  = "#5f7788"

FONT_BASE   = ("Trebuchet MS", 10)
FONT_MED    = ("Trebuchet MS", 10, "bold")
FONT_HEAD   = ("Georgia", 18, "bold")
FONT_MONO   = ("Consolas", 9)
FONT_STAT   = ("Consolas", 20, "bold")


class HospitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital — Patient Record System")
        self.root.geometry("1180x660")
        self.root.minsize(960, 540)
        self.root.configure(bg=BG)

        # Load from CSV
        self.patients, self.next_id = load_patients()
        self.current_filter = "All"

        self._build_style()
        self._build_layout()
        self.refresh()
        self._tick_clock()

    # ------------------------------------------------------------------
    # Style
    # ------------------------------------------------------------------
    def _build_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                         background=BG_PANEL,
                         fieldbackground=BG_PANEL,
                         foreground=TEXT_HI,
                         rowheight=32,
                         borderwidth=0,
                         font=FONT_BASE)
        style.map("Treeview",
                  background=[("selected", TEAL_DIM)],
                  foreground=[("selected", TEAL)])
        style.configure("Treeview.Heading",
                         background=BG,
                         foreground=TEXT_LOW,
                         borderwidth=0,
                         font=("Trebuchet MS", 9, "bold"))
        style.map("Treeview.Heading", background=[("active", BG)])
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self):
        # ---- Header ----
        header = tk.Frame(self.root, bg=BG_PANEL, highlightbackground=BORDER,
                           highlightthickness=1)
        header.pack(fill="x", padx=18, pady=(18, 12))

        left = tk.Frame(header, bg=BG_PANEL)
        left.pack(side="left", padx=18, pady=14)

        mark = tk.Canvas(left, width=38, height=38, bg=BG_PANEL, highlightthickness=0)
        mark.pack(side="left", padx=(0, 12))
        mark.create_oval(0, 0, 38, 38, fill=TEAL, outline="")
        mark.create_text(19, 19, text="+", fill="#062622", font=("Georgia", 16, "bold"))

        title_box = tk.Frame(left, bg=BG_PANEL)
        title_box.pack(side="left")
        tk.Label(title_box, text="Hospital Patient Records", font=FONT_HEAD, bg=BG_PANEL, fg=TEXT_HI).pack(anchor="w")
        tk.Label(title_box, text="MANAGEMENT SYSTEM", font=("Consolas", 8),
                 bg=BG_PANEL, fg=TEXT_LOW).pack(anchor="w")

        clock_box = tk.Frame(header, bg=BG_PANEL)
        clock_box.pack(side="right", padx=(6, 0), pady=14)
        self.clock_label = tk.Label(clock_box, text="", font=("Consolas", 16, "bold"),
                                     bg=BG_PANEL, fg=TEAL)
        self.clock_label.pack(anchor="e")
        self.date_label = tk.Label(clock_box, text="", font=("Consolas", 8),
                                    bg=BG_PANEL, fg=TEXT_LOW)
        self.date_label.pack(anchor="e")

        stats = tk.Frame(header, bg=BG_PANEL)
        stats.pack(side="right", padx=18, pady=14)
        self.stat_admitted = self._stat_block(stats, "Admitted", TEAL)
        self.stat_discharged = self._stat_block(stats, "Discharged", TEXT_MID)
        self.stat_total = self._stat_block(stats, "Total", TEXT_HI)

        # ---- Toolbar ----
        toolbar = tk.Frame(self.root, bg=BG)
        toolbar.pack(fill="x", padx=18, pady=(0, 10))

        search_wrap = tk.Frame(toolbar, bg=BG_FIELD, highlightbackground=BORDER,
                                highlightthickness=1)
        search_wrap.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(search_wrap, text="🔍", bg=BG_FIELD, fg=TEXT_LOW).pack(side="left", padx=(10, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh())
        search_entry = tk.Entry(search_wrap, textvariable=self.search_var, bg=BG_FIELD,
                                 fg=TEXT_HI, insertbackground=TEXT_HI, relief="flat",
                                 font=FONT_BASE)
        search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self._placeholder(search_entry, "Search by name or patient ID…")

        self._button(toolbar, "＋ Add Patient", self.open_add_dialog, primary=True).pack(side="left")

        # ---- Filter chips ----
        chips = tk.Frame(self.root, bg=BG)
        chips.pack(fill="x", padx=18, pady=(0, 12))
        self.chip_buttons = {}
        for label in ("All", "Admitted", "Discharged"):
            b = tk.Label(chips, text=label.upper(), font=("Consolas", 8, "bold"),
                         bg=BG, fg=TEXT_MID, padx=12, pady=6, cursor="hand2")
            b.pack(side="left", padx=(0, 8))
            b.bind("<Button-1>", lambda e, l=label: self.set_filter(l))
            self.chip_buttons[label] = b
        self._style_chip("All")

        # ---- Table ----
        table_frame = tk.Frame(self.root, bg=BG_PANEL, highlightbackground=BORDER,
                                highlightthickness=1)
        table_frame.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        cols = ("id", "name", "age", "gender", "disease", "doctor", "status", "admitted_at", "discharged_at")
        headers = ("ID", "Name", "Age", "Sex", "Diagnosis", "Doctor", "Status", "Admitted", "Discharged")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
        self.tree.column("id", width=55, anchor="w")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("age", width=45, anchor="center")
        self.tree.column("gender", width=45, anchor="center")
        self.tree.column("disease", width=150, anchor="w")
        self.tree.column("doctor", width=140, anchor="w")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("admitted_at", width=130, anchor="center")
        self.tree.column("discharged_at", width=130, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)

        self.tree.tag_configure("Admitted", foreground=TEAL)
        self.tree.tag_configure("Discharged", foreground=TEXT_LOW)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self.open_edit_dialog())

        # ---- Action bar ----
        actions = tk.Frame(self.root, bg=BG)
        actions.pack(fill="x", padx=18, pady=(0, 18))
        self._button(actions, "Edit", self.open_edit_dialog).pack(side="left", padx=(0, 8))
        self._button(actions, "Discharge", self.discharge_selected, accent=AMBER).pack(side="left", padx=(0, 8))
        self._button(actions, "Delete", self.delete_selected, accent=RED).pack(side="left", padx=(0, 8))
        self._button(actions, "Clear All Records", self.clear_all_records, accent=RED).pack(side="left")

        self.status_label = tk.Label(actions, text="", bg=BG, fg=TEXT_LOW, font=("Consolas", 9))
        self.status_label.pack(side="right")

    def _stat_block(self, parent, label, color):
        box = tk.Frame(parent, bg=BG_PANEL)
        box.pack(side="left", padx=16)
        num = tk.Label(box, text="0", font=FONT_STAT, bg=BG_PANEL, fg=color)
        num.pack(anchor="e")
        tk.Label(box, text=label.upper(), font=("Consolas", 8), bg=BG_PANEL, fg=TEXT_LOW).pack(anchor="e")
        return num

    def _tick_clock(self):
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%I:%M:%S %p"))
        self.date_label.config(text=now.strftime("%a, %d %b %Y").upper())
        self.root.after(1000, self._tick_clock)

    def _placeholder(self, entry, text):
        entry.insert(0, text)
        entry.config(fg=TEXT_LOW)

        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg=TEXT_HI)

        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg=TEXT_LOW)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _button(self, parent, text, command, primary=False, accent=None):
        bg = TEAL if primary else BG_PANEL
        fg = "#062622" if primary else (accent or TEXT_MID)
        b = tk.Label(parent, text=text, bg=bg, fg=fg, font=FONT_MED,
                     padx=16, pady=9, cursor="hand2",
                     highlightbackground=BORDER, highlightthickness=0 if primary else 1)
        b.bind("<Button-1>", lambda e: command())
        hover_bg = TEAL if primary else "#152537"
        b.bind("<Enter>", lambda e: b.config(bg=hover_bg))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    def _style_chip(self, active):
        for label, b in self.chip_buttons.items():
            if label == active:
                b.config(bg=TEAL_DIM, fg=TEAL)
            else:
                b.config(bg=BG, fg=TEXT_MID)

    # ------------------------------------------------------------------
    # Data logic
    # ------------------------------------------------------------------
    def find_by_id(self, pid):
        for p in self.patients:
            if p.id == pid:
                return p
        return None

    def selected_patient(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.find_by_id(int(sel[0]))

    def set_filter(self, label):
        self.current_filter = label
        self._style_chip(label)
        self.refresh()

    def set_status(self, msg):
        self.status_label.config(text=msg)
        self.root.after(3000, lambda: self.status_label.config(text=""))

    # ------------------------------------------------------------------
    # Refresh table + stats
    # ------------------------------------------------------------------
    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        query = self.search_var.get().strip().lower()
        if query == "search by name or patient id…":
            query = ""

        for p in self.patients:
            if self.current_filter != "All" and p.status != self.current_filter:
                continue
            if query and query != str(p.id) and query not in p.name.lower():
                continue
            
            admitted_str = p.admitted_time.strftime("%d %b, %I:%M %p")
            discharged_str = p.discharged_time.strftime("%d %b, %I:%M %p") if p.discharged_time else "—"
            self.tree.insert("", "end", iid=str(p.id),
                              values=(f"{p.id:03d}", p.name, p.age, p.gender,
                                      p.disease, p.doctor, p.status,
                                      admitted_str, discharged_str),
                              tags=(p.status,))

        admitted = sum(1 for p in self.patients if p.status == "Admitted")
        discharged = sum(1 for p in self.patients if p.status == "Discharged")
        self.stat_admitted.config(text=str(admitted))
        self.stat_discharged.config(text=str(discharged))
        self.stat_total.config(text=str(len(self.patients)))

    # ------------------------------------------------------------------
    # Add / Edit dialog
    # ------------------------------------------------------------------
    def open_add_dialog(self):
        self._patient_form_dialog(title="Admit New Patient", patient=None)

    def open_edit_dialog(self):
        p = self.selected_patient()
        if not p:
            messagebox.showinfo("No selection", "Select a patient row first.")
            return
        self._patient_form_dialog(title=f"Edit Record — ID #{p.id:03d}", patient=p)

    def _patient_form_dialog(self, title, patient):
        dlg = tk.Toplevel(self.root)
        dlg.title(title)
        dlg.configure(bg=BG_PANEL)
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text=title, font=FONT_MED, bg=BG_PANEL, fg=TEXT_HI).pack(
            anchor="w", padx=24, pady=(22, 16))

        fields = {}

        def add_field(label, default=""):
            tk.Label(dlg, text=label, font=("Trebuchet MS", 9, "bold"), bg=BG_PANEL,
                      fg=TEXT_MID).pack(anchor="w", padx=24)
            e = tk.Entry(dlg, bg=BG_FIELD, fg=TEXT_HI, insertbackground=TEXT_HI,
                         relief="flat", font=FONT_BASE, highlightbackground=BORDER,
                         highlightthickness=1)
            e.insert(0, default)
            e.pack(fill="x", padx=24, pady=(4, 12), ipady=7)
            fields[label] = e
            return e

        add_field("Full name", patient.name if patient else "")
        add_field("Age", patient.age if patient else "")

        tk.Label(dlg, text="Gender", font=("Trebuchet MS", 9, "bold"), bg=BG_PANEL,
                  fg=TEXT_MID).pack(anchor="w", padx=24)
        gender_var = tk.StringVar(value=patient.gender if patient else "M")
        gender_menu = ttk.Combobox(dlg, textvariable=gender_var, values=["M", "F", "O"],
                                     state="readonly")
        gender_menu.pack(fill="x", padx=24, pady=(4, 12))

        add_field("Diagnosis", patient.disease if patient else "")
        add_field("Assigned doctor", patient.doctor if patient else "")

        btn_row = tk.Frame(dlg, bg=BG_PANEL)
        btn_row.pack(fill="x", padx=24, pady=(6, 20))

        def on_save():
            name = fields["Full name"].get().strip()
            age = fields["Age"].get().strip()
            disease = fields["Diagnosis"].get().strip()
            doctor = fields["Assigned doctor"].get().strip()
            gender = gender_var.get()

            if not (name and age and disease and doctor):
                messagebox.showwarning("Missing fields", "Please fill in every field.")
                return
            if not age.isdigit():
                messagebox.showwarning("Invalid age", "Age must be a number.")
                return

            if patient:
                patient.name = name
                patient.age = age
                patient.gender = gender
                patient.disease = disease
                patient.doctor = doctor
                self.set_status("Patient record updated.")
            else:
                p = Patient(self.next_id, name, age, gender, disease, doctor)
                self.patients.append(p)
                self.next_id += 1
                self.set_status(f"Patient added — ID #{p.id:03d}")

            save_patients(self.patients)
            dlg.destroy()
            self.refresh()

        cancel_btn = tk.Label(btn_row, text="Cancel", bg=BG_PANEL, fg=TEXT_MID,
                               font=FONT_MED, padx=16, pady=9, cursor="hand2",
                               highlightbackground=BORDER, highlightthickness=1)
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))
        cancel_btn.bind("<Button-1>", lambda e: dlg.destroy())

        save_btn = tk.Label(btn_row, text="Save Patient" if not patient else "Update Record",
                             bg=TEAL, fg="#062622", font=FONT_MED, padx=16, pady=9,
                             cursor="hand2")
        save_btn.pack(side="left", expand=True, fill="x", padx=(6, 0))
        save_btn.bind("<Button-1>", lambda e: on_save())

        dlg.update_idletasks()
        w = max(380, dlg.winfo_reqwidth())
        h = dlg.winfo_reqheight()
        x = self.root.winfo_x() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - h) // 2
        dlg.geometry(f"{w}x{h}+{x}+{y}")

        fields["Full name"].focus_set()

    # ------------------------------------------------------------------
    # Discharge / Delete
    # ------------------------------------------------------------------
    def discharge_selected(self):
        p = self.selected_patient()
        if not p:
            messagebox.showinfo("No selection", "Select a patient row first.")
            return
        if p.status == "Discharged":
            messagebox.showinfo("Already discharged", f"{p.name} is already discharged.")
            return
        if messagebox.askyesno("Discharge patient?", f"Mark {p.name} as discharged?"):
            p.status = "Discharged"
            p.discharged_time = datetime.now()
            save_patients(self.patients)
            self.set_status(f"{p.name} has been discharged.")
            self.refresh()

    def delete_selected(self):
        p = self.selected_patient()
        if not p:
            messagebox.showinfo("No selection", "Select a patient row first.")
            return
        if messagebox.askyesno("Delete record?",
                                f"Permanently delete {p.name}'s record? This can't be undone.",
                                icon="warning"):
            self.patients.remove(p)
            save_patients(self.patients)
            self.set_status("Patient record deleted.")
            self.refresh()

    def clear_all_records(self):
        if not self.patients:
            messagebox.showinfo("No records", "There are no records to clear.")
            return
        if messagebox.askyesno(
            "Clear all records?",
            f"This will permanently delete all {len(self.patients)} patient "
            "record(s). This can't be undone.",
            icon="warning"
        ):
            self.patients.clear()
            self.next_id = 1
            save_patients(self.patients)
            self.set_status("All patient records cleared.")
            self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()