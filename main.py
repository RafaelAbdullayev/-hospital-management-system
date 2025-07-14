import tkinter as tk
from tkinter import ttk, messagebox

# Patient structure: dictionary with keys: name, age, condition
patients = []
deleted_patients = []

current_search_results = []

class SHMS:
    def __init__(self, root):
        self.root = root
        self.root.title("SHMS - Sumqayit Hospital Management System")
        self.root.geometry("800x600")

        self.create_main_screen()

    def create_main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="SHMS - Main Menu", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Patient List", width=20, command=self.show_patient_list).pack(pady=10)
        tk.Button(self.root, text="Deleted Patients", width=20, command=self.show_deleted_patients).pack(pady=10)
        tk.Button(self.root, text="Complaints", width=20, command=self.show_complaint_screen).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_patient_list(self):
        self.clear_screen()
        tk.Label(self.root, text="Patient List", font=("Arial", 16)).pack(pady=10)

        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT)
        tk.Button(search_frame, text="Search", command=lambda: self.search_patients(search_entry.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Back", command=self.create_main_screen).pack(side=tk.LEFT)

        self.patient_table = ttk.Treeview(self.root, columns=("Name", "Age", "Condition"), show="headings")
        for col in ("Name", "Age", "Condition"):
            self.patient_table.heading(col, text=col)
        self.patient_table.pack(pady=10)

        tk.Button(self.root, text="Add Patient", command=self.add_patient_screen).pack(pady=5)
        tk.Button(self.root, text="Edit Selected", command=self.edit_selected_patient).pack(pady=5)
        tk.Button(self.root, text="Delete Selected", command=self.delete_selected_patient).pack(pady=5)

        self.refresh_patient_table()

    def refresh_patient_table(self):
        for row in self.patient_table.get_children():
            self.patient_table.delete(row)

        global current_search_results
        current_search_results = list(enumerate(patients))
        for idx, patient in current_search_results:
            self.patient_table.insert("", "end", iid=idx, values=(patient['name'], patient['age'], patient['condition']))

    def search_patients(self, query):
        for row in self.patient_table.get_children():
            self.patient_table.delete(row)

        global current_search_results
        current_search_results = [(i, p) for i, p in enumerate(patients) if query.lower() in p['name'].lower()]
        for idx, patient in current_search_results:
            self.patient_table.insert("", "end", iid=idx, values=(patient['name'], patient['age'], patient['condition']))

    def add_patient_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add New Patient", font=("Arial", 16)).pack(pady=10)

        name_entry = tk.Entry(self.root)
        age_entry = tk.Entry(self.root)
        condition_entry = tk.Entry(self.root)

        name_entry.pack(pady=5)
        age_entry.pack(pady=5)
        condition_entry.pack(pady=5)

        tk.Button(self.root, text="Save", command=lambda: self.save_new_patient(name_entry.get(), age_entry.get(), condition_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_patient_list).pack()

    def save_new_patient(self, name, age, condition):
        if name and age and condition:
            patients.append({"name": name, "age": age, "condition": condition})
            self.show_patient_list()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def edit_selected_patient(self):
        selected = self.patient_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to edit.")
            return

        index = int(selected)
        self.show_edit_patient_screen(index)

    def show_edit_patient_screen(self, index):
        self.clear_screen()
        patient = patients[index]

        tk.Label(self.root, text="Edit Patient", font=("Arial", 16)).pack(pady=10)

        name_entry = tk.Entry(self.root)
        name_entry.insert(0, patient['name'])
        age_entry = tk.Entry(self.root)
        age_entry.insert(0, patient['age'])
        condition_entry = tk.Entry(self.root)
        condition_entry.insert(0, patient['condition'])

        name_entry.pack(pady=5)
        age_entry.pack(pady=5)
        condition_entry.pack(pady=5)

        tk.Button(self.root, text="Save Changes", command=lambda: self.save_edited_patient(index, name_entry.get(), age_entry.get(), condition_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_patient_list).pack()

    def save_edited_patient(self, index, name, age, condition):
        if name and age and condition:
            patients[index] = {"name": name, "age": age, "condition": condition}
            self.show_patient_list()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_selected_patient(self):
        selected = self.patient_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to delete.")
            return

        index = int(selected)
        deleted_patients.append(patients.pop(index))
        self.refresh_patient_table()

    def show_deleted_patients(self):
        self.clear_screen()
        tk.Label(self.root, text="Deleted Patients", font=("Arial", 16)).pack(pady=10)

        self.deleted_table = ttk.Treeview(self.root, columns=("Name", "Age", "Condition"), show="headings")
        for col in ("Name", "Age", "Condition"):
            self.deleted_table.heading(col, text=col)
        self.deleted_table.pack(pady=10)

        for idx, patient in enumerate(deleted_patients):
            self.deleted_table.insert("", "end", iid=idx, values=(patient['name'], patient['age'], patient['condition']))

        tk.Button(self.root, text="Restore Selected", command=self.restore_deleted_patient).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_screen).pack()

    def restore_deleted_patient(self):
        selected = self.deleted_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to restore.")
            return

        index = int(selected)
        patients.append(deleted_patients.pop(index))
        self.show_deleted_patients()

    def show_complaint_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Patient Complaint", font=("Arial", 16)).pack(pady=10)

        complaint_entry = tk.Text(self.root, height=10, width=60)
        complaint_entry.pack(pady=10)

        tk.Button(self.root, text="Submit", command=lambda: self.submit_complaint(complaint_entry.get("1.0", tk.END))).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_screen).pack()

    def submit_complaint(self, complaint):
        if complaint.strip():
            messagebox.showinfo("Submitted", "Complaint submitted successfully.")
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Complaint cannot be empty.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SHMS(root)
    root.mainloop()
