

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from expense_tracker import ExpenseManager, Expense


class ExpenseTrackerGUI:
    
    
    def __init__(self):
        self.manager = ExpenseManager()
        self.root = tk.Tk()
        self.root.title("Personal Expense Tracker")
        self.root.geometry("800x600")
        
        self.setup_ui()
        self.refresh_expense_list()
    
    def setup_ui(self):
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Personal Expense Tracker", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Buttons
        ttk.Button(buttons_frame, text="Add Expense", 
                  command=self.add_expense_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Update Expense", 
                  command=self.update_expense_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Delete Expense", 
                  command=self.delete_expense_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Summary Report", 
                  command=self.show_summary_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Download Report", 
                  command=self.download_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Filter", 
                  command=self.filter_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", 
                  command=self.refresh_expense_list).pack(side=tk.LEFT, padx=(5, 0))
        
        # Expenses list frame
        list_frame = ttk.LabelFrame(main_frame, text="Expenses", padding="5")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for expenses
        columns = ("ID", "Date", "Category", "Amount", "Note")
        self.expense_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.expense_tree.heading("ID", text="ID")
        self.expense_tree.heading("Date", text="Date")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Note", text="Note")
        
        self.expense_tree.column("ID", width=60)
        self.expense_tree.column("Date", width=100)
        self.expense_tree.column("Category", width=100)
        self.expense_tree.column("Amount", width=100)
        self.expense_tree.column("Note", width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)
        
        self.expense_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def refresh_expense_list(self):
        """Refresh the expense list display"""
        # Clear existing items
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        # Add expenses to tree
        for expense in self.manager.expenses:
            self.expense_tree.insert("", tk.END, values=(
                expense.id,
                expense.date,
                expense.category,
                f"Rs.{expense.amount:.2f}",
                expense.note
            ))
        
        # Update status
        total_expenses = sum(exp.amount for exp in self.manager.expenses)
        self.status_var.set(f"Total Expenses: Rs.{total_expenses:.2f} | Count: {len(self.manager.expenses)}")
    
    def add_expense_dialog(self):
        
        dialog = ExpenseDialog(self.root, self.manager.categories, "Add New Expense")
        if dialog.result:
            amount, category, note, date = dialog.result
            if self.manager.add_expense(amount, category, note):
                self.refresh_expense_list()
                messagebox.showinfo("Success", "Expense added successfully!")
    
    def update_expense_dialog(self):
        
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to update.")
            return
        
        item = self.expense_tree.item(selected_item[0])
        expense_id = int(item['values'][0])
        
        expense = self.manager.get_expense_by_id(expense_id)
        if not expense:
            messagebox.showerror("Error", "Expense not found.")
            return
        
        dialog = ExpenseDialog(self.root, self.manager.categories, "Update Expense", 
                              expense.amount, expense.category, expense.note, expense.date)
        if dialog.result:
            amount, category, note, date = dialog.result
            if self.manager.update_expense(expense_id, amount, category, note, date):
                self.refresh_expense_list()
                messagebox.showinfo("Success", "Expense updated successfully!")
    
    def delete_expense_dialog(self):
        
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to delete.")
            return
        
        item = self.expense_tree.item(selected_item[0])
        expense_id = int(item['values'][0])
        
        result = messagebox.askyesno("Confirm Delete", 
                                   "Are you sure you want to delete this expense?")
        if result:
            if self.manager.delete_expense(expense_id):
                self.refresh_expense_list()
                messagebox.showinfo("Success", "Expense deleted successfully!")
    
    def show_summary_report(self):
        
        if not self.manager.expenses:
            messagebox.showinfo("Info", "No expenses found.")
            return
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Expense Summary Report")
        report_window.geometry("500x400")
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(report_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate report text
        total_spent = sum(expense.amount for expense in self.manager.expenses)
        
        # Group by category
        category_totals = {}
        for expense in self.manager.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        
        # Group by month
        month_totals = {}
        for expense in self.manager.expenses:
            month = expense.date[:7]  # YYYY-MM
            month_totals[month] = month_totals.get(month, 0) + expense.amount
        
        report_text = f"""EXPENSE SUMMARY REPORT
{'='*50}
Total Expenses: Rs.{total_spent:.2f}
Total Transactions: {len(self.manager.expenses)}

By Category:
"""
        for category, total in sorted(category_totals.items()):
            percentage = (total / total_spent) * 100 if total_spent > 0 else 0
            report_text += f"  {category}: Rs.{total:.2f} ({percentage:.1f}%)\n"
        
        report_text += "\nBy Month:\n"
        for month, total in sorted(month_totals.items()):
            report_text += f"  {month}: Rs.{total:.2f}\n"
        
        text_widget.insert(tk.END, report_text)
        text_widget.config(state=tk.DISABLED)
    
    def download_report(self):
        """Download summary report as text file"""
        if not self.manager.expenses:
            messagebox.showinfo("Info", "No expenses found.")
            return
        
        # Generate and save the report
        self.manager.get_summary_report(save_to_file=True)
        messagebox.showinfo("Success", "Summary report has been saved as a text file!")
    
    def filter_dialog(self):
        """Show filter dialog"""
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Expenses")
        filter_window.geometry("300x200")
        
        frame = ttk.Frame(filter_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Category filter
        ttk.Label(frame, text="Category:").grid(row=0, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(frame, textvariable=category_var, 
                                     values=[""] + self.manager.categories)
        category_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Date filter
        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        date_var = tk.StringVar()
        date_entry = ttk.Entry(frame, textvariable=date_var)
        date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        frame.columnconfigure(1, weight=1)
        
        def apply_filter():
            category = category_var.get().strip()
            date = date_var.get().strip()
            
            # Clear existing items
            for item in self.expense_tree.get_children():
                self.expense_tree.delete(item)
            
            # Apply filter and add filtered expenses
            filtered_expenses = self.manager.expenses.copy()
            
            if category:
                filtered_expenses = [exp for exp in filtered_expenses 
                                   if exp.category.lower() == category.lower()]
            
            if date:
                filtered_expenses = [exp for exp in filtered_expenses if exp.date == date]
            
            for expense in filtered_expenses:
                self.expense_tree.insert("", tk.END, values=(
                    expense.id,
                    expense.date,
                    expense.category,
                    f"Rs.{expense.amount:.2f}",
                    expense.note
                ))
            
            filter_window.destroy()
        
        def clear_filter():
            self.refresh_expense_list()
            filter_window.destroy()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Apply Filter", command=apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Filter", command=clear_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=filter_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def run(self):
        
        self.root.mainloop()


class ExpenseDialog:
    
    
    def __init__(self, parent, categories, title, amount=0.0, category="", note="", date=""):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        frame = ttk.Frame(self.dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Amount
        ttk.Label(frame, text="Amount (Rs.):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar(value=str(amount))
        ttk.Entry(frame, textvariable=self.amount_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Category
        ttk.Label(frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value=category)
        category_combo = ttk.Combobox(frame, textvariable=self.category_var, values=categories)
        category_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Date
        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=date or datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(frame, textvariable=self.date_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Note
        ttk.Label(frame, text="Note:").grid(row=3, column=0, sticky=tk.W, pady=5)
        note_frame = ttk.Frame(frame)
        note_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        self.note_text = tk.Text(note_frame, height=4, width=30)
        self.note_text.pack(fill=tk.BOTH, expand=True)
        self.note_text.insert(tk.END, note)
        
        frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def ok_clicked(self):
        
        try:
            amount = float(self.amount_var.get())
            category = self.category_var.get().strip()
            note = self.note_text.get("1.0", tk.END).strip()
            date = self.date_var.get().strip()
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
            
            if not category:
                messagebox.showerror("Error", "Please select a category.")
                return
            
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
            
            self.result = (amount, category, note, date)
            self.dialog.destroy()
            
        except ValueError as e:
            if "time data" in str(e):
                messagebox.showerror("Error", "Please enter date in YYYY-MM-DD format.")
            else:
                messagebox.showerror("Error", "Please enter a valid amount.")


if __name__ == "__main__":
    app = ExpenseTrackerGUI()
    app.run()
