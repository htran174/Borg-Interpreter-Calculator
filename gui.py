import tkinter as tk
from backend import HashTable
import re

class BORGCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BORG Calculator")
        self.hash_table = HashTable()
        self.line_number = 0

        # --- Variable Set Toggle Button ---
        self.set_mode = False
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        self.set_button = tk.Button(top_frame, text="SET", command=self.toggle_set_mode)
        self.set_button.pack(side=tk.LEFT, padx=10)

        self.var_buttons = {}
        self.var_value_labels = {}
        for var in ['X', 'Y', 'Z']:
            var_frame = tk.Frame(top_frame)
            var_frame.pack(side=tk.LEFT, padx=5)

            btn = tk.Button(var_frame, text=var, command=lambda v=var: self.var_button_click(v))
            btn.pack()

            label = tk.Label(var_frame, text="Value = ", font=("Arial", 10))
            label.pack()

            self.var_buttons[var] = btn
            self.var_value_labels[var] = label

        # --- Calculator Display ---
        self.display = tk.Entry(root, font=("Arial", 18), justify="right", bd=10, relief=tk.RIDGE, width=25)
        self.display.pack(pady=10)

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '^', '%', '+'],
            ['(', ')', 'CLR', '=']
        ]

        for row in buttons:
            row_frame = tk.Frame(btn_frame)
            row_frame.pack()
            for btn_text in row:
                tk.Button(row_frame, text=btn_text, width=5, height=2, font=("Arial", 14),
                          command=lambda b=btn_text: self.on_button_click(b)).pack(side=tk.LEFT, padx=2, pady=2)

    def toggle_set_mode(self):
        self.set_mode = not self.set_mode
        mode_text = "SET MODE ON" if self.set_mode else "SET"
        self.set_button.config(text=mode_text)

    def var_button_click(self, var):
        if self.set_mode:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, f"VAR {var} = ")
            self.set_mode = False
            self.set_button.config(text="SET")
        else:
            self.display.insert(tk.END, var)

    def on_button_click(self, char):
        if char == 'CLR':
            self.display.delete(0, tk.END)
        elif char == '=':
            expr = self.display.get().strip()
            self.display.delete(0, tk.END)
            result = self.evaluate_expression(expr)
            if result != "OK":
                self.display.insert(tk.END, result)
        else:
            self.display.insert(tk.END, char)

    def evaluate_expression(self, expr):
        tokens = expr.strip().split()
        if len(tokens) >= 4 and tokens[0] == "VAR" and tokens[2] == "=":
            var = tokens[1].upper()
            rhs_expr = ' '.join(tokens[3:])
            evaluated_rhs = self._evaluate_rhs(rhs_expr)
            if isinstance(evaluated_rhs, str) and evaluated_rhs.startswith("Error"):
                return evaluated_rhs
            self.hash_table.insert(var, evaluated_rhs)
            self.var_value_labels[var].config(text=f"Value = {evaluated_rhs}")
            return "OK"

        result = self._evaluate_rhs(expr)
        if isinstance(result, str) and result.startswith("Error"):
            return result
        return str(result)

    def _evaluate_rhs(self, expr):
        def replace_var(match):
            var = match.group().upper()
            value = self.hash_table.search_value(var)
            if value == -1:
                raise ValueError(f"Error: {var} is undefined")
            return str(value)

        try:
            replaced_expr = re.sub(r'\b[A-Za-z]\b', replace_var, expr)
            result = eval(replaced_expr)
            return int(result) if isinstance(result, float) and result.is_integer() else result
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    root = tk.Tk()
    app = BORGCalculator(root)
    root.mainloop()