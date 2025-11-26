import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# File path for storing student data
FILENAME = os.path.join(os.path.dirname(__file__), "studentMarks.txt")

# Marks helper functions
def calc_coursework_total(c1, c2, c3):
    return c1 + c2 + c3

def calc_overall_percentage(cw_total, exam):
    return round(((cw_total + exam) / 160) * 100, 2)

def calc_grade(pct):
    if pct >= 70: return "A"
    if pct >= 60: return "B"
    if pct >= 50: return "C"
    if pct >= 40: return "D"
    return "F"

# File I/O functions
def load_data_from_file():
    students = []
    if not os.path.exists(FILENAME):
        return students
    with open(FILENAME, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    for ln in lines:
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) != 6:
            continue
        code, name = parts[0], parts[1]
        try:
            c1, c2, c3, exam = map(int, parts[2:])
        except ValueError:
            continue
        cw_total = calc_coursework_total(c1, c2, c3)
        pct = calc_overall_percentage(cw_total, exam)
        students.append({
            "code": code, "name": name,
            "c1": c1, "c2": c2, "c3": c3,
            "cw_total": cw_total, "exam": exam,
            "pct": pct, "grade": calc_grade(pct)
        })
    return students

def save_data_to_file(students):
    with open(FILENAME, "w", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

# # Main Application

class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager — Dashboard") # Window title
        self.geometry("1000x600") # Window size
        self.minsize(920, 520)
        self.configure(bg="#111113")
        self.students = load_data_from_file() # Load student data
        self.sort_asc = True # Default sort order

        self.setup_style() # Configure UI styles
        self.create_sidebar() # Left menu buttons
        self.create_main_area() # Main content area
        self.show_home() # Show home view

 # Styles
    def setup_style(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

         # General frames and labels
        self.style.configure("TFrame", background="#111113")
        self.style.configure("TLabel", background="#111113", foreground="#E6D4A6", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#FFD66B", background="#111113")
        self.style.configure("Small.TLabel", font=("Segoe UI", 10), foreground="#E6D4A6", background="#111113")
        
        # Sidebar buttons
        self.style.configure("Sidebar.TButton", background="#141414", foreground="#E6D4A6", relief="flat",
                             font=("Segoe UI", 10), padding=6)
        self.style.map("Sidebar.TButton", background=[("active", "#2A2A2A")])

         # Treeview (table) style
        self.style.configure("Treeview",
                             background="#1C1C1E",
                             foreground="#FFFFFF",
                             fieldbackground="#1C1C1E",
                             rowheight=22,
                             font=("Segoe UI", 10))
        self.style.map("Treeview", background=[("selected", "#3B3A36")])
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#222225",
                             foreground="#E6D4A6")

 # Sidebar buttons
    def create_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#0E0E0F", width=180)
        self.sidebar.pack(side="left", fill="y")

        # Sidebar logo/title
        logo = tk.Label(self.sidebar, text="🎓 EduPortal", bg="#0E0E0F", fg="#FFD66B",
                        font=("Segoe UI", 12, "bold"))
        logo.pack(pady=(12, 8))

 # Buttons and commands
        btn_specs = [
            ("Home", self.show_home),
            ("View All", self.show_view_all),
            ("Search", self.show_search),
            ("Add Student", self.show_add),
            ("Update Student", self.show_update),
            ("Delete Student", self.show_delete),
            ("Sort (Toggle)", self.toggle_sort),
            ("Highest", self.show_highest),
            ("Lowest", self.show_lowest),
            ("Exit", self.quit)
        ]
        for txt, cmd in btn_specs:
            b = ttk.Button(self.sidebar, text=txt, command=cmd, style="Sidebar.TButton")
            b.pack(fill="x", padx=10, pady=6)

# Main content area
    def create_main_area(self):
        self.main = tk.Frame(self, bg="#111113")
        self.main.pack(side="right", fill="both", expand=True)

         # Header label
        self.header = ttk.Label(self.main, text="📊 Student Records", style="Header.TLabel")
        self.header.pack(anchor="nw", padx=18, pady=(12, 6))

         # Content frame for table
        self.content = tk.Frame(self.main, bg="#111113")
        self.content.pack(fill="both", expand=True, padx=12, pady=6)

         # Table columns
        columns = ("code", "name", "c1", "c2", "c3", "cw_total", "exam", "pct", "grade")
        self.tree = ttk.Treeview(self.content, columns=columns, show="headings", selectmode="browse")
        headings = {
            "code": "Code", "name": "Name", "c1": "CW1", "c2": "CW2", "c3": "CW3",
            "cw_total": "CW Total", "exam": "Exam", "pct": "Overall %", "grade": "Grade"
        }
        widths = {"code": 80, "name": 260, "c1": 50, "c2": 50, "c3": 50, "cw_total": 80, "exam": 70, "pct": 90, "grade": 60}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

         # Scrollbars
        vsb = ttk.Scrollbar(self.content, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.content, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.status = ttk.Label(self.main, text="", style="Small.TLabel", anchor="w")
        self.status.pack(fill="x", padx=18, pady=(6, 12))

     # Helper to refresh table
    def refresh_tree(self, students=None):
        if students is None:
            students = self.students
        for r in self.tree.get_children():
            self.tree.delete(r)
        for s in students:
            self.tree.insert("", "end", values=(
                s["code"], s["name"], s["c1"], s["c2"], s["c3"],
                s["cw_total"], s["exam"], s["pct"], s["grade"]
            ))
        self.status.config(text=f"Records: {len(students)}   |   Sort: {'ASC' if self.sort_asc else 'DESC'}")

# View functions
    def show_home(self):
        self.header.config(text="Student Manager — Dashboard")
        total_students = len(self.students)
        avg = round(sum(s["pct"] for s in self.students) / total_students, 2) if total_students else 0.0
        self.status.config(text=f"Students: {total_students}    |    Class Average: {avg}%")
        top = sorted(self.students, key=lambda x: x["pct"], reverse=True)[:12]
        self.refresh_tree(top)

    def show_view_all(self):
        for s in self.students:
            s["cw_total"] = calc_coursework_total(s["c1"], s["c2"], s["c3"])
            s["pct"] = calc_overall_percentage(s["cw_total"], s["exam"])
            s["grade"] = calc_grade(s["pct"])
        self.students.sort(key=lambda x: x["pct"], reverse=not self.sort_asc)
        self.refresh_tree(self.students)

    def show_search(self):
        query = simpledialog.askstring("Search", "Enter student code or name (partial allowed):", parent=self)
        if not query:
            return
        q = query.strip().lower()
        matches = [s for s in self.students if q in s["code"].lower() or q in s["name"].lower()]
        if not matches:
            messagebox.showinfo("No Results", f"No students matching '{query}'")
            return
        self.refresh_tree(matches)
        self.header.config(text=f"Search Results for '{query}'")

    def show_add(self):
        form = StudentForm(self, title="Add Student")
        self.wait_window(form)
        if form.result:
            new_s = form.result
            if any(s["code"] == new_s["code"] for s in self.students):
                messagebox.showerror("Duplicate Code", "A student with that code already exists.")
                return
            new_s["cw_total"] = calc_coursework_total(new_s["c1"], new_s["c2"], new_s["c3"])
            new_s["pct"] = calc_overall_percentage(new_s["cw_total"], new_s["exam"])
            new_s["grade"] = calc_grade(new_s["pct"])
            self.students.append(new_s)
            save_data_to_file(self.students)
            messagebox.showinfo("Added", f"Student {new_s['name']} added.")
            self.show_view_all()

    def show_update(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select the student row in the table to update.")
            return
        vals = self.tree.item(sel[0], "values")
        code = vals[0]
        student = next((s for s in self.students if s["code"] == code), None)
        if not student:
            messagebox.showerror("Error", "Selected student not found.")
            return
        form = StudentForm(self, title="Update Student", data=student)
        self.wait_window(form)
        if form.result:
            updated = form.result
            student.update(updated)
            student["cw_total"] = calc_coursework_total(student["c1"], student["c2"], student["c3"])
            student["pct"] = calc_overall_percentage(student["cw_total"], student["exam"])
            student["grade"] = calc_grade(student["pct"])
            save_data_to_file(self.students)
            messagebox.showinfo("Updated", f"Student {student['name']} updated.")
            self.show_view_all()

    def show_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select the student row in the table to delete.")
            return
        vals = self.tree.item(sel[0], "values")
        code, name = vals[0], vals[1]
        ans = messagebox.askyesno("Confirm Delete", f"Delete {name} ({code})?")
        if not ans:
            return
        self.students = [s for s in self.students if s["code"] != code]
        save_data_to_file(self.students)
        messagebox.showinfo("Deleted", f"Student {name} deleted.")
        self.show_view_all()

    def toggle_sort(self):
        self.sort_asc = not self.sort_asc
        self.show_view_all()

    def show_highest(self):
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        best = max(self.students, key=lambda s: s["pct"])
        self.refresh_tree([best])
        self.header.config(text=f"Highest: {best['name']} ({best['pct']}%)")

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        worst = min(self.students, key=lambda s: s["pct"])
        self.refresh_tree([worst])
        self.header.config(text=f"Lowest: {worst['name']} ({worst['pct']}%)")

# Student Form (Add/Update)
class StudentForm(tk.Toplevel):
    def __init__(self, parent, title="Student Form", data=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg="#131313")
        self.result = None
        self.build_form(data)
        self.transient(parent)
        self.grab_set()
        self.focus_force()

    def build_form(self, data=None):
        pad = {"padx": 10, "pady": 6}
        lbl_style = {"bg": "#131313", "fg": "#E6D4A6"}
        entry_bg = "#1C1C1E"
        entry_fg = "white"

        frame = tk.Frame(self, bg="#131313")
        frame.pack(padx=12, pady=12)

# Labels and entries
        tk.Label(frame, text="Student Code:", **lbl_style).grid(row=0, column=0, sticky="e", **pad)
        self.e_code = tk.Entry(frame, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, relief="flat")
        self.e_code.grid(row=0, column=1, **pad)

        tk.Label(frame, text="Name:", **lbl_style).grid(row=1, column=0, sticky="e", **pad)
        self.e_name = tk.Entry(frame, width=40, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, relief="flat")
        self.e_name.grid(row=1, column=1, **pad)

        tk.Label(frame, text="Coursework 1 (0-20):", **lbl_style).grid(row=2, column=0, sticky="e", **pad)
        self.e_c1 = tk.Entry(frame, width=8, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, relief="flat")
        self.e_c1.grid(row=2, column=1, sticky="w", **pad)

        tk.Label(frame, text="Coursework 2 (0-20):", **lbl_style).grid(row=3, column=0, sticky="e", **pad)
        self.e_c2 = tk.Entry(frame, width=8, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, relief="flat")
        self.e_c2.grid(row=3, column=1, sticky="w", **pad)

        tk.Label(frame, text="Coursework 3 (0-20):", **lbl_style).grid(row=4, column=0, sticky="e", **pad)
        self.e_c3 = tk.Entry(frame, width=8, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, relief="flat")
        self.e_c3.grid(row=4, column=1, sticky="w", **pad)

        tk.Label(frame, text="Exam (0-100):", **lbl_style).grid(row=5, column=0, sticky="e", **pad)
        self.e_exam = tk.Entry(frame, width=8, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, relief="flat")
        self.e_exam.grid(row=5, column=1, sticky="w", **pad)

# Buttons
        btn_frame = tk.Frame(frame, bg="#131313")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(12, 0))
        tk.Button(btn_frame, text="Save", command=self.on_save, bg="#2A2A2A", fg="#E6D4A6", width=12).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancel", command=self.destroy, bg="#2A2A2A", fg="#E6D4A6", width=12).pack(side="left", padx=8)

 # Fill data if updating
        if data:
            self.e_code.insert(0, data["code"])
            self.e_code.config(state="disabled")
            self.e_name.insert(0, data["name"])
            self.e_c1.insert(0, str(data["c1"]))
            self.e_c2.insert(0, str(data["c2"]))
            self.e_c3.insert(0, str(data["c3"]))
            self.e_exam.insert(0, str(data["exam"]))

    def on_save(self):
        code = self.e_code.get().strip()
        name = self.e_name.get().strip()
        try:
            c1, c2, c3 = int(self.e_c1.get().strip()), int(self.e_c2.get().strip()), int(self.e_c3.get().strip())
            exam = int(self.e_exam.get().strip())
        except ValueError:
            messagebox.showerror("Invalid", "Please enter valid integer marks.")
            return
        if not code.isdigit() or not (1000 <= int(code) <= 9999):
            messagebox.showerror("Invalid Code", "Student code must be an integer 1000–9999.")
            return
        if not (0 <= c1 <= 20 and 0 <= c2 <= 20 and 0 <= c3 <= 20):
            messagebox.showerror("Invalid Coursework", "Coursework marks must be 0–20 each.")
            return
        if not (0 <= exam <= 100):
            messagebox.showerror("Invalid Exam", "Exam mark must be 0–100.")
            return
        if not name:
            messagebox.showerror("Invalid", "Please enter the student's name.")
            return
        self.result = {"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam}
        self.destroy()

# Run Application
if __name__ == "__main__":
    app = StudentManagerApp()
    app.mainloop()