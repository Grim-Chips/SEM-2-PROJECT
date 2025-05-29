import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from typing import Optional

class Units:
    def __init__(self, UnitId, location, size, status, rent, sellingprice, ownerId):
        self.UnitId = UnitId
        self.location = location
        self.size = size
        self.status = status
        self.rent = rent
        self.sellingprice = sellingprice
        self.ownerId = ownerId
    def __str__(self):
        return f"{self.UnitId.title()} | {self.location} | {self.size} | {self.status} | ${self.rent} | ${self.sellingprice} | {self.ownerId}"

class UnitsDatabase:
    def __init__(self, db_name="units.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        # Initialize the database and create the units table if it doesn't exist
        conn = sqlite3.connect(self.db_name)
        pointer = conn.cursor()
        pointer.execute('''
            CREATE TABLE IF NOT EXISTS units (
                UnitId TEXT PRIMARY KEY,
                location TEXT NOT NULL,
                size INTEGER NOT NULL,
                status TEXT NOT NULL,
                rent REAL,
                sellingprice REAL,
                ownerId TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_unit(self, unit: Units):
        # Add a unit to the database
        conn = sqlite3.connect(self.db_name)
        pointer = conn.cursor()
        try:
            pointer.execute('''
                INSERT INTO units (UnitId, location, size, status, rent, sellingprice, ownerId)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (unit.UnitId, unit.location, unit.size, unit.status, unit.rent, unit.sellingprice, unit.ownerId))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_units(self):
        # Retrieve all units from the database
        conn = sqlite3.connect(self.db_name)
        pointer = conn.cursor()
        pointer.execute('SELECT * FROM units')
        rows = pointer.fetchall()
        conn.close()
        
        units = []
        for row in rows:
            unit = Units(*row)
            units.append(unit)
        return units
    
    def update_unit_status(self, unit_id: str, new_status: str):
        # Update the status of a unit
        conn = sqlite3.connect(self.db_name)
        pointer = conn.cursor()
        pointer.execute('UPDATE units SET status = ? WHERE UnitId = ?', (new_status, unit_id))
        conn.commit()
        conn.close()
    
    def delete_unit(self, unit_id: str):
        # Delete a unit from the database
        conn = sqlite3.connect(self.db_name)
        pointer = conn.cursor()
        pointer.execute('DELETE FROM units WHERE UnitId = ?', (unit_id,))
        conn.commit()
        conn.close()

class UnitsGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Units Management System")
        self.window.geometry("900x700")
        
        self.db = UnitsDatabase()
        self.setup_gui()
        self.refresh_units_list()
    
    def setup_gui(self):
        # Main frame
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Unit Information Frame
        self.setup_unit_info_frame(main_frame)
        
        # Units List Frame
        self.setup_units_list_frame(main_frame)
        
        # Buttons Frame
        self.setup_buttons_frame(main_frame)


    #  Setup the unit information input frame
    def setup_unit_info_frame(self, parent):
        user_info_frame = tk.LabelFrame(parent, text="Unit Information", padx=10, pady=10)
        user_info_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Unit ID
        tk.Label(user_info_frame, text="Unit ID:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.unit_id_entry = tk.Entry(user_info_frame, width=20)
        self.unit_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        
        # Location
        tk.Label(user_info_frame, text="Location:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.location_entry = tk.Entry(user_info_frame, width=20)
        self.location_entry.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        
        # Size
        tk.Label(user_info_frame, text="Size (sq ft):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.size_entry = tk.Entry(user_info_frame, width=20)
        self.size_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        # Status
        tk.Label(user_info_frame, text="Status:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(user_info_frame, textvariable=self.status_var, 
                                        values=["Available", "Rented", "Sold"], width=17)
        self.status_combo.grid(row=1, column=3, padx=5, pady=2, sticky="w")
        self.status_combo.set("Available")
        
        # Rent
        tk.Label(user_info_frame, text="Rent ($):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.rent_entry = tk.Entry(user_info_frame, width=20)
        self.rent_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        
        # Selling Price
        tk.Label(user_info_frame, text="Selling Price ($):").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.selling_price_entry = tk.Entry(user_info_frame, width=20)
        self.selling_price_entry.grid(row=2, column=3, padx=5, pady=2, sticky="w")
        
        # Owner ID
        tk.Label(user_info_frame, text="Owner ID:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.owner_id_entry = tk.Entry(user_info_frame, width=20)
        self.owner_id_entry.grid(row=3, column=1, padx=5, pady=2, sticky="w")
    
    def setup_units_list_frame(self, parent):
        # Setup the units list display frame
        list_frame = tk.LabelFrame(parent, text="Units List", padx=10, pady=10)
        list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights for expansion
        parent.grid_rowconfigure(1, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview for units list
        columns = ("UnitID", "Location", "Size", "Status", "Rent", "Price", "OwnerID")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        # Define column headings and widths
        column_widths = {"UnitID": 80, "Location": 120, "Size": 80, "Status": 80, "Rent": 80, "Price": 100, "OwnerID": 80}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_unit_select)
    
    def setup_buttons_frame(self, parent):
        # Setup the buttons frame
        buttons_frame = tk.Frame(parent)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Add Unit button
        tk.Button(buttons_frame, text="Add Unit", command=self.add_unit, 
                 bg="#2e7d32", fg="white", width=12, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Update Status buttons
        tk.Button(buttons_frame, text="Mark as Rented", command=self.mark_as_rented, 
                 bg="#ff9800", fg="white", width=12, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="Mark as Sold", command=self.mark_as_sold, 
                 bg="#f44336", fg="white", width=12, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Delete Unit button
        tk.Button(buttons_frame, text="Delete Unit", command=self.delete_unit, 
                 bg="#d32f2f", fg="white", width=12, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Clear Fields button
        tk.Button(buttons_frame, text="Clear Fields", command=self.clear_fields, 
                 bg="#757575", fg="white", width=12, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        tk.Button(buttons_frame, text="Refresh", command=self.refresh_units_list, 
                 bg="#1976d2", fg="white", width=12, font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)

    def validate_numeric_input(self, value: str, field_name: str, allow_empty: bool = False) -> Optional[float]:
        # Validate and convert numeric input with better error messages
        if not value.strip():
            if allow_empty:
                return None
            else:
                raise ValueError(f"{field_name} cannot be empty!")
        
        try:
            num_value = float(value.strip())
            if field_name == "Size" and num_value <= 0:
                raise ValueError("Size must be greater than 0!")
            if field_name in ["Rent", "Selling Price"] and num_value < 0:
                raise ValueError(f"{field_name} cannot be negative!")
            return num_value
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError(f"{field_name} must be a valid number! You entered: '{value}'")
            raise e

    def add_unit(self):
        # Add a new unit to the database with improved error handling
        try:
            # Get and validate basic string inputs
            unit_id = self.unit_id_entry.get().strip()
            location = self.location_entry.get().strip()
            status = self.status_var.get()
            owner_id = self.owner_id_entry.get().strip()
            
            # Check required fields
            if not unit_id:
                messagebox.showerror("Error", "Unit ID is required!")
                self.unit_id_entry.focus()
                return
            if not location:
                messagebox.showerror("Error", "Location is required!")
                self.location_entry.focus()
                return
            if not owner_id:
                messagebox.showerror("Error", "Owner ID is required!")
                self.owner_id_entry.focus()
                return
            
            # Validate numeric inputs with specific error messages
            size_str = self.size_entry.get().strip()
            rent_str = self.rent_entry.get().strip()
            price_str = self.selling_price_entry.get().strip()
            
            # Size is required and must be an integer
            try:
                size_val = self.validate_numeric_input(size_str, "Size", allow_empty=False)
                if size_val is None:
                    raise ValueError("Size cannot be empty!")
                size = int(size_val)
            except ValueError as e:
                messagebox.showerror("Size Error", str(e))
                self.size_entry.focus()
                return
            
            # Rent and selling price are optional
            try:
                rent = self.validate_numeric_input(rent_str, "Rent", allow_empty=True)
            except ValueError as e:
                messagebox.showerror("Rent Error", str(e))
                self.rent_entry.focus()
                return
            
            try:
                selling_price = self.validate_numeric_input(price_str, "Selling Price", allow_empty=True)
            except ValueError as e:
                messagebox.showerror("Selling Price Error", str(e))
                self.selling_price_entry.focus()
                return
            
            # Create unit object
            unit = Units(unit_id, location, size, status, rent, selling_price, owner_id)
            
            # Add to database
            if self.db.add_unit(unit):
                messagebox.showinfo("Success", f"Unit '{unit_id}' added successfully!")
                self.clear_fields()
                self.refresh_units_list()
            else:
                messagebox.showerror("Error", f"Unit ID '{unit_id}' already exists! Please use a different ID.")
                self.unit_id_entry.focus()
                
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
    
    def mark_as_rented(self):
        # Mark selected unit as rented
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a unit to mark as rented!")
            return
        
        unit_id = self.tree.item(selected_item[0])['values'][0]
        self.db.update_unit_status(unit_id, "Rented")
        messagebox.showinfo("Success", f"Unit {unit_id} marked as rented!")
        self.refresh_units_list()
    
    def mark_as_sold(self):
        # Mark selected unit as sold
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a unit to mark as sold!")
            return
        
        unit_id = self.tree.item(selected_item[0])['values'][0]
        self.db.update_unit_status(unit_id, "Sold")
        messagebox.showinfo("Success", f"Unit {unit_id} marked as sold!")
        self.refresh_units_list()
    
    def delete_unit(self):
        # Delete selected unit
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a unit to delete!")
            return
        
        unit_id = self.tree.item(selected_item[0])['values'][0]
        result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete unit {unit_id}?")
        
        if result:
            self.db.delete_unit(unit_id)
            messagebox.showinfo("Success", f"Unit {unit_id} deleted successfully!")
            self.refresh_units_list()
    
    def clear_fields(self):
        # Clear all input fields
        self.unit_id_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)
        self.status_var.set("Available")
        self.rent_entry.delete(0, tk.END)
        self.selling_price_entry.delete(0, tk.END)
        self.owner_id_entry.delete(0, tk.END)
        # Focus on the first field after clearing
        self.unit_id_entry.focus()
    
    def on_unit_select(self, event):
        # Handle unit selection in the treeview
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            self.unit_id_entry.delete(0, tk.END)
            self.unit_id_entry.insert(0, values[0])
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, values[1])
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, values[2])
            self.status_var.set(values[3])
            self.rent_entry.delete(0, tk.END)
            self.rent_entry.insert(0, values[4] if values[4] != 'None' else '')
            self.selling_price_entry.delete(0, tk.END)
            self.selling_price_entry.insert(0, values[5] if values[5] != 'None' else '')
            self.owner_id_entry.delete(0, tk.END)
            self.owner_id_entry.insert(0, values[6])
    
    def refresh_units_list(self):
        # Refresh the units list display
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all units from database
        units = self.db.get_all_units()
        
        # Insert units into treeview
        for unit in units:
            self.tree.insert("", tk.END, values=(
                unit.UnitId, unit.location, unit.size, unit.status,
                f"${unit.rent:.2f}" if unit.rent is not None else 'N/A',
                f"${unit.sellingprice:.2f}" if unit.sellingprice is not None else 'N/A',
                unit.ownerId
            ))
    
    def run(self):
        # Start the GUI application
        self.window.mainloop()

# Main execution
if __name__ == "__main__":
    app = UnitsGUI()
    app.run()