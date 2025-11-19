
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from db_connection import DatabaseManager


class SmartParkApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("SmartPark - Parking Management System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize database manager
        self.db = DatabaseManager()
        self.setup_ui()
        
    def setup_ui(self):
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header, 
            text="🚗 SmartPark System", 
            font=("Arial", 24, "bold"),
            bg="#2c3e50", 
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        
        # Welcome message
        welcome = tk.Label(
            self.content_frame,
            text="Welcome to SmartPark",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        welcome.pack(pady=30)
        
        # Button container
        button_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        button_frame.pack(expand=True)
        
        # Navigation buttons
        buttons = [
            ("Park Vehicle", self.show_park_vehicle, "#27ae60"),
            ("Unpark Vehicle", self.show_unpark_vehicle, "#e74c3c"),
            ("View Parking Map", self.show_parking_map, "#3498db"),
            ("Check Availability", self.check_availability, "#f39c12"),
            ("View Parking History", self.show_parking_history, "#9b59b6"),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg=color,
                fg="white",
                width=20,
                height=2,
                command=command,
                cursor="hand2",
                relief=tk.RAISED,
                bd=3
            )
            btn.pack(pady=10)
    
    def show_park_vehicle(self):
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Park Vehicle",
            font=("Arial", 18, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Get available spots
        spots = self.db.get_parking_spots()
        available_spots = [spot_id for spot_id, occupied in spots if not occupied]
        
        if not available_spots:
            tk.Label(
                self.content_frame,
                text="No available parking spots!",
                font=("Arial", 14, "bold"),
                bg="#ecf0f1",
                fg="#e74c3c"
            ).pack(pady=20)
            
            tk.Button(
                self.content_frame,
                text="Back",
                font=("Arial", 12, "bold"),
                bg="#95a5a6",
                fg="white",
                width=15,
                command=self.show_dashboard
            ).pack(pady=20)
            return
        
        # Available spots display
        info_label = tk.Label(
            self.content_frame,
            text=f"Available Spots: {len(available_spots)}",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#27ae60"
        )
        info_label.pack(pady=5)
        
        # Form frame
        form_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        form_frame.pack(pady=20)
        
        # Spot ID (Dropdown)
        tk.Label(form_frame, text="Select Spot:", font=("Arial", 12), bg="#ecf0f1").grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )
        spot_var = tk.StringVar()
        spot_dropdown = ttk.Combobox(
            form_frame, 
            textvariable=spot_var,
            values=available_spots,
            font=("Arial", 12),
            width=28,
            state="readonly"
        )
        spot_dropdown.grid(row=0, column=1, padx=10, pady=10)
        if available_spots:
            spot_dropdown.current(0)
        
        # Driver Name
        tk.Label(form_frame, text="Driver Name:", font=("Arial", 12), bg="#ecf0f1").grid(
            row=1, column=0, sticky="w", padx=10, pady=10
        )
        driver_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        driver_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Plate Number
        tk.Label(form_frame, text="Plate Number:", font=("Arial", 12), bg="#ecf0f1").grid(
            row=2, column=0, sticky="w", padx=10, pady=10
        )
        plate_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        plate_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        button_frame.pack(pady=20)
        
        def submit_park():
            spot = spot_var.get().strip()
            driver = driver_entry.get().strip()
            plate = plate_entry.get().strip().upper()
            
            if not spot or not driver or not plate:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                spot_id = int(spot)
            except ValueError:
                messagebox.showerror("Error", "Invalid spot selection!")
                return
            
            success, message = self.db.park_vehicle(spot_id, driver, plate)
            
            if success:
                messagebox.showinfo("Success", f"Vehicle parked successfully!\n\n"
                                              f"Driver: {driver}\n"
                                              f"Plate: {plate}\n"
                                              f"Spot: {spot_id}\n"
                                              f"Time: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            button_frame,
            text="Park Vehicle",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=15,
            command=submit_park
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=15,
            command=self.show_dashboard
        ).pack(side=tk.LEFT, padx=10)
    
    def show_unpark_vehicle(self):
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Unpark Vehicle",
            font=("Arial", 18, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        form_frame.pack(pady=20)
        
        # Plate Number
        tk.Label(
            form_frame, 
            text="Plate Number:", 
            font=("Arial", 12), 
            bg="#ecf0f1"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        plate_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        plate_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        button_frame.pack(pady=20)
        
        def submit_unpark():
            plate = plate_entry.get().strip().upper()
            
            if not plate:
                messagebox.showerror("Error", "Plate number is required!")
                return
            
            success, message, data = self.db.unpark_vehicle(plate)
            
            if success:
                messagebox.showinfo("Success", f"Vehicle unparked successfully!\n\n"
                                              f"Driver: {data['driver']}\n"
                                              f"Plate: {data['plate']}\n"
                                              f"Spot: {data['spot']}\n"
                                              f"Time In: {data['time_in']}\n"
                                              f"Time Out: {data['time_out']}")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            button_frame,
            text="Unpark Vehicle",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            command=submit_unpark
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=15,
            command=self.show_dashboard
        ).pack(side=tk.LEFT, padx=10)
    
    def show_parking_map(self):
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Parking Map",
            font=("Arial", 18, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Get parking spots data
        spots = self.db.get_parking_spots()
        
        if not spots:
            tk.Label(
                self.content_frame,
                text="No parking spots found in database.",
                font=("Arial", 12),
                bg="#ecf0f1",
                fg="#e74c3c"
            ).pack(pady=20)
        else:
            # Create grid for parking spots
            grid_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
            grid_frame.pack(pady=20)
            
            # Display spots in a grid (5 columns)
            cols = 5
            for idx, (spot_id, occupied) in enumerate(spots):
                row = idx // cols
                col = idx % cols
                
                color = "#e74c3c" if occupied else "#27ae60"
                status = "OCCUPIED" if occupied else "AVAILABLE"
                
                spot_frame = tk.Frame(grid_frame, bg=color, relief=tk.RAISED, bd=2)
                spot_frame.grid(row=row, column=col, padx=5, pady=5)
                
                tk.Label(
                    spot_frame,
                    text=f"Spot {spot_id}",
                    font=("Arial", 10, "bold"),
                    bg=color,
                    fg="white",
                    width=12,
                    height=2
                ).pack()
                
                tk.Label(
                    spot_frame,
                    text=status,
                    font=("Arial", 8),
                    bg=color,
                    fg="white"
                ).pack()
            
            # Legend
            legend_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
            legend_frame.pack(pady=20)
            
            tk.Label(
                legend_frame,
                text="● Available",
                font=("Arial", 10),
                bg="#ecf0f1",
                fg="#27ae60"
            ).pack(side=tk.LEFT, padx=20)
            
            tk.Label(
                legend_frame,
                text="● Occupied",
                font=("Arial", 10),
                bg="#ecf0f1",
                fg="#e74c3c"
            ).pack(side=tk.LEFT, padx=20)
        
        # Back button
        tk.Button(
            self.content_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=15,
            command=self.show_dashboard
        ).pack(pady=20)
    
    def check_availability(self):
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Parking Availability",
            font=("Arial", 18, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Get parking spots data
        spots = self.db.get_parking_spots()
        
        if not spots:
            tk.Label(
                self.content_frame,
                text="No parking spots found in database.",
                font=("Arial", 12),
                bg="#ecf0f1",
                fg="#e74c3c"
            ).pack(pady=20)
        else:
            # Create scrollable list
            list_frame = tk.Frame(self.content_frame, bg="white")
            list_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            
            # Create treeview for better display
            tree = ttk.Treeview(
                list_frame,
                columns=("Spot", "Status"),
                show="headings",
                height=15
            )
            
            tree.heading("Spot", text="Spot ID")
            tree.heading("Status", text="Status")
            
            tree.column("Spot", width=200, anchor="center")
            tree.column("Status", width=200, anchor="center")
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            
            # Insert data
            for spot_id, occupied in spots:
                status = "OCCUPIED" if occupied else "AVAILABLE"
                tag = "occupied" if occupied else "available"
                tree.insert("", tk.END, values=(f"Spot {spot_id}", status), tags=(tag,))
            
            # Configure tags for colors
            tree.tag_configure("occupied", background="#ffcccc")
            tree.tag_configure("available", background="#ccffcc")
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Summary
            occupied_count = sum(1 for _, occupied in spots if occupied)
            available_count = len(spots) - occupied_count
            
            summary = tk.Label(
                self.content_frame,
                text=f"Total Spots: {len(spots)} | Available: {available_count} | Occupied: {occupied_count}",
                font=("Arial", 12, "bold"),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            summary.pack(pady=10)
        
        # Back button (always show regardless of spots)
        tk.Button(
            self.content_frame,
            text="Back to Dashboard",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=20,
            command=self.show_dashboard
        ).pack(pady=20)
    
    def show_parking_history(self):
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Parking History",
            font=("Arial", 18, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Get parking history data
        history = self.db.get_parking_history()
        
        if not history:
            tk.Label(
                self.content_frame,
                text="No parking history records found.",
                font=("Arial", 12),
                bg="#ecf0f1",
                fg="#e74c3c"
            ).pack(pady=20)
        else:
            # Create scrollable frame for history
            list_frame = tk.Frame(self.content_frame, bg="white")
            list_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            
            # Create treeview for better display
            columns = ("ID", "Spot", "Driver", "Plate", "Time In", "Time Out")
            tree = ttk.Treeview(
                list_frame,
                columns=columns,
                show="headings",
                height=15
            )
            
            # Define headings
            tree.heading("ID", text="Record ID")
            tree.heading("Spot", text="Spot ID")
            tree.heading("Driver", text="Driver Name")
            tree.heading("Plate", text="Plate Number")
            tree.heading("Time In", text="Time In")
            tree.heading("Time Out", text="Time Out")
            
            # Define column widths
            tree.column("ID", width=80, anchor="center")
            tree.column("Spot", width=80, anchor="center")
            tree.column("Driver", width=150, anchor="w")
            tree.column("Plate", width=120, anchor="center")
            tree.column("Time In", width=150, anchor="center")
            tree.column("Time Out", width=150, anchor="center")
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            
            # Insert data
            for record in history:
                time_in = record['time_in'].strftime('%Y-%m-%d %I:%M %p') if record['time_in'] else 'N/A'
                time_out = record['time_out'].strftime('%Y-%m-%d %I:%M %p') if record['time_out'] else 'N/A'
                
                tree.insert("", tk.END, values=(
                    record['id'],
                    record['spot_id'],
                    record['driver_name'],
                    record['plate_number'],
                    time_in,
                    time_out
                ))
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Summary
            summary = tk.Label(
                self.content_frame,
                text=f"Total Records: {len(history)} (showing last 50)",
                font=("Arial", 12, "bold"),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            summary.pack(pady=10)
        
        # Back button (always show regardless of spots)
        tk.Button(
            self.content_frame,
            text="Back to Dashboard",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=20,
            command=self.show_dashboard
        ).pack(pady=20)
    
    def show_parking_history(self):
        self.clear_content()
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Parking History",
            font=("Arial", 18, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Get parking history data
        history = self.db.get_parking_history()
        
        if not history:
            tk.Label(
                self.content_frame,
                text="No parking history records found.",
                font=("Arial", 12),
                bg="#ecf0f1",
                fg="#e74c3c"
            ).pack(pady=20)
        else:
            # Create scrollable frame for history
            list_frame = tk.Frame(self.content_frame, bg="white")
            list_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            
            # Create treeview for better display
            columns = ("ID", "Spot", "Driver", "Plate", "Time In", "Time Out")
            tree = ttk.Treeview(
                list_frame,
                columns=columns,
                show="headings",
                height=15
            )
            
            # Define headings
            tree.heading("ID", text="Record ID")
            tree.heading("Spot", text="Spot ID")
            tree.heading("Driver", text="Driver Name")
            tree.heading("Plate", text="Plate Number")
            tree.heading("Time In", text="Time In")
            tree.heading("Time Out", text="Time Out")
            
            # Define column widths
            tree.column("ID", width=80, anchor="center")
            tree.column("Spot", width=80, anchor="center")
            tree.column("Driver", width=150, anchor="w")
            tree.column("Plate", width=120, anchor="center")
            tree.column("Time In", width=150, anchor="center")
            tree.column("Time Out", width=150, anchor="center")
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            
            # Insert data
            for record in history:
                time_in = record['time_in'].strftime('%Y-%m-%d %I:%M %p') if record['time_in'] else 'N/A'
                time_out = record['time_out'].strftime('%Y-%m-%d %I:%M %p') if record['time_out'] else 'N/A'
                
                tree.insert("", tk.END, values=(
                    record['id'],
                    record['spot_id'],
                    record['driver_name'],
                    record['plate_number'],
                    time_in,
                    time_out
                ))
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Summary
            summary = tk.Label(
                self.content_frame,
                text=f"Total Records: {len(history)} (showing last 50)",
                font=("Arial", 12, "bold"),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            summary.pack(pady=10)
        
        # Back button
        tk.Button(
            self.content_frame,
            text="Back to Dashboard",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=20,
            command=self.show_dashboard
        ).pack(pady=20)
    
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = SmartParkApp(root)
    app.run()


if __name__ == "__main__":
    main()
