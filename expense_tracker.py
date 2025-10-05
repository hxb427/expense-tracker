

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Expense:
    
    
    def __init__(self, amount: float, category: str, note: str = "", date: str = None, expense_id: int = None):
        self.amount = amount
        self.category = category
        self.note = note
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.id = expense_id or int(datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "note": self.note,
            "date": self.date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        
        expense = cls(data["amount"], data["category"], data["note"], data["date"], data["id"])
        return expense
    
    def __str__(self) -> str:
        return f"ID: {self.id} | Date: {self.date} | Category: {self.category} | Amount: Rs.{self.amount:.2f} | Note: {self.note}"


class ExpenseManager:
    
    
    def __init__(self, data_file: str = "expenses.json"):
        self.data_file = data_file
        self.expenses: List[Expense] = []
        self.categories = ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Health", "Other"]
        self.next_id = 1  # Counter for unique IDs
        self.load_expenses()
    
    def load_expenses(self) -> None:
        """Load expenses from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.expenses = [Expense.from_dict(expense_data) for expense_data in data]
                    # Set next_id to be higher than the highest existing ID
                    if self.expenses:
                        max_id = max(expense.id for expense in self.expenses)
                        self.next_id = max_id + 1
            except (json.JSONDecodeError, FileNotFoundError):
                self.expenses = []
    
    def save_expenses(self) -> None:
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump([expense.to_dict() for expense in self.expenses], f, indent=2)
        except Exception as e:
            print(f"Error saving expenses: {e}")
    
    def add_expense(self, amount: float, category: str, note: str = "") -> bool:
        
        try:
            if amount <= 0:
                print("Amount must be greater than 0")
                return False
            
            if category not in self.categories:
                print(f"Invalid category. Available categories: {', '.join(self.categories)}")
                return False
            
            expense = Expense(amount, category, note, expense_id=self.next_id)
            self.next_id += 1  # Increment for next expense
            self.expenses.append(expense)
            self.save_expenses()
            print(f"Expense added successfully: {expense}")
            return True
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def view_expenses(self, filter_category: str = None, filter_date: str = None) -> None:
        
        filtered_expenses = self.expenses.copy()
        
        if filter_category:
            filtered_expenses = [exp for exp in filtered_expenses if exp.category.lower() == filter_category.lower()]
        
        if filter_date:
            filtered_expenses = [exp for exp in filtered_expenses if exp.date == filter_date]
        
        if not filtered_expenses:
            print("No expenses found matching the criteria.")
            return
        
        print("\n" + "="*80)
        print("EXPENSE LIST")
        print("="*80)
        for expense in filtered_expenses:
            print(expense)
        print("="*80)
    
    def update_expense(self, expense_id: int, amount: float = None, category: str = None, note: str = None, date: str = None) -> bool:
        
        try:
            expense = self.get_expense_by_id(expense_id)
            if not expense:
                print(f"Expense with ID {expense_id} not found")
                return False
            
            if amount is not None:
                if amount <= 0:
                    print("Amount must be greater than 0")
                    return False
                expense.amount = amount
            
            if category is not None:
                if category not in self.categories:
                    print(f"Invalid category. Available categories: {', '.join(self.categories)}")
                    return False
                expense.category = category
            
            if note is not None:
                expense.note = note
            
            if date is not None:
                expense.date = date
            
            self.save_expenses()
            print(f"Expense updated successfully: {expense}")
            return True
        except Exception as e:
            print(f"Error updating expense: {e}")
            return False
    
    def delete_expense(self, expense_id: int) -> bool:
        
        try:
            expense = self.get_expense_by_id(expense_id)
            if not expense:
                print(f"Expense with ID {expense_id} not found")
                return False
            
            self.expenses.remove(expense)
            self.save_expenses()
            print(f"Expense deleted successfully: {expense}")
            return True
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False
    
    def get_expense_by_id(self, expense_id: int) -> Optional[Expense]:
        
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None
    
    def get_summary_report(self, save_to_file: bool = False) -> None:
        
        if not self.expenses:
            print("No expenses found.")
            return
        
        total_spent = sum(expense.amount for expense in self.expenses)
        
        # Group by category
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        
        # Group by month
        month_totals = {}
        for expense in self.expenses:
            month = expense.date[:7]  # YYYY-MM
            month_totals[month] = month_totals.get(month, 0) + expense.amount
        
        # Generate report text
        report_lines = []
        report_lines.append("="*60)
        report_lines.append("EXPENSE SUMMARY REPORT")
        report_lines.append("="*60)
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total Expenses: Rs.{total_spent:.2f}")
        report_lines.append(f"Total Transactions: {len(self.expenses)}")
        
        report_lines.append("\nBy Category:")
        for category, total in sorted(category_totals.items()):
            percentage = (total / total_spent) * 100 if total_spent > 0 else 0
            report_lines.append(f"  {category}: Rs.{total:.2f} ({percentage:.1f}%)")
        
        report_lines.append("\nBy Month:")
        for month, total in sorted(month_totals.items()):
            report_lines.append(f"  {month}: Rs.{total:.2f}")
        
        report_lines.append("="*60)
        
        # Display report
        for line in report_lines:
            print(line)
        
        # Save to file if requested
        if save_to_file:
            self.save_summary_to_file(report_lines)
    
    def save_summary_to_file(self, report_lines: list) -> None:
        """Save summary report to a text file"""
        try:
            # Generate filename with current date and time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"expense_summary_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                for line in report_lines:
                    f.write(line + '\n')
            
            print(f"\nSummary report saved to: {filename}")
        except Exception as e:
            print(f"Error saving summary report: {e}")
    
    def add_category(self, category: str) -> bool:
        
        if category in self.categories:
            print(f"Category '{category}' already exists")
            return False
        
        self.categories.append(category)
        print(f"Category '{category}' added successfully")
        return True
    
    def view_categories(self) -> None:
        
        print("\nAvailable Categories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")






