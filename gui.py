import tkinter as tk
from tkinter import ttk, scrolledtext
from backend import HashTable
import re

class BORGCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BORG Interpreter & Calculator")
        self.hash_table = HashTable()

        self.root.configure(bg="#1e1e1e")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#2d2d2d", foreground="white")
        style.configure("TNotebook.Tab", background="#2d2d2d", foreground="white")
        style.map("TNotebook.Tab", background=[("selected", "#3c3f41")])

        self.notebook = ttk.Notebook(root)
        self.calc_frame = tk.Frame(self.notebook, bg="#1e1e1e")
        self.command_frame = tk.Frame(self.notebook, bg="#1e1e1e")

        self.notebook.add(self.calc_frame, text='Calculator Mode')
        self.notebook.add(self.command_frame, text='Command Console')
        self.notebook.pack(expand=1, fill='both')

        self.setup_calculator_tab()
        self.setup_command_tab()

    def setup_calculator_tab(self):
        self.set_mode = False
        top_frame = tk.Frame(self.calc_frame, bg="#1e1e1e")
        top_frame.pack(pady=10)

        self.set_button = tk.Button(top_frame, text="SET", command=self.toggle_set_mode, bg="white", fg="black")
        self.set_button.pack(side=tk.LEFT, padx=10)

        self.var_buttons = {}
        self.var_value_labels = {}
        for var in ['X', 'Y', 'Z']:
            var_frame = tk.Frame(top_frame, bg="#1e1e1e")
            var_frame.pack(side=tk.LEFT, padx=5)

            btn = tk.Button(var_frame, text=var, command=lambda v=var: self.var_button_click(v), bg="white", fg="black")
            btn.pack()

            label = tk.Label(var_frame, text="Value = ", font=("Arial", 10), bg="#1e1e1e", fg="white")
            label.pack()

            self.var_buttons[var] = btn
            self.var_value_labels[var] = label

        self.display = tk.Entry(self.calc_frame, font=("Arial", 18), justify="right", bd=10, relief=tk.RIDGE,
                                width=25, bg="white", fg="black", insertbackground="black")
        self.display.pack(pady=10)

        btn_frame = tk.Frame(self.calc_frame, bg="#1e1e1e")
        btn_frame.pack()

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '^', '%', '+'],
            ['(', ')', 'CLR', '=']
        ]

        for row in buttons:
            row_frame = tk.Frame(btn_frame, bg="#1e1e1e")
            row_frame.pack()
            for btn_text in row:
                tk.Button(row_frame, text=btn_text, width=5, height=2, font=("Arial", 14),
                          command=lambda b=btn_text: self.on_button_click(b),
                          bg="white", fg="black", activebackground="#ddd", activeforeground="black")\
                    .pack(side=tk.LEFT, padx=2, pady=2)

    def setup_command_tab(self):
        ref_frame = tk.Frame(self.command_frame, bg="#1e1e1e")
        ref_frame.pack(fill='x', padx=10, pady=10)

        header1 = tk.Label(ref_frame, text="Command", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white")
        header2 = tk.Label(ref_frame, text="Description", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white")
        header1.grid(row=0, column=0, sticky="w")
        header2.grid(row=0, column=1, sticky="w", padx=30)

        examples = [
            ("VAR X = 5", "Declare variable X with value 5"),
            ("VAR Y", "Declare variable Y with default value 0"),
            ("X = Y + 3", "Assign expression to a variable"),
            ("PRINT X", "Print value of X"),
            ("START", "Start a new variable scope"),
            ("DONE", "End the current scope"),
            ("SHOW", "Display all defined variables"),
            ("CLEAR", "Clear the command output"),
            ("RESET", "Reset all variables and scopes")
        ]

        half = len(examples) // 2 + len(examples) % 2
        for i, (cmd, desc) in enumerate(examples):
            col = 0 if i < half else 2
            row = i if i < half else i - half
            tk.Label(ref_frame, text=cmd, bg="#1e1e1e", fg="white").grid(row=row + 1, column=col, sticky="w")
            tk.Label(ref_frame, text=desc, bg="#1e1e1e", fg="white").grid(row=row + 1, column=col + 1, sticky="w", padx=10)

        input_frame = tk.Frame(self.command_frame, bg="#1e1e1e")
        input_frame.pack(fill='x', padx=10, pady=(0, 5))

        self.command_entry = tk.Entry(input_frame, font=("Courier", 12), bg="#2d2d2d", fg="white", insertbackground="white")
        self.command_entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.command_entry.bind("<Return>", lambda event: self.run_single_command())

        run_button = tk.Button(input_frame, text="Run", command=self.run_single_command,
                               bg="#3c3f41", fg="black", activebackground="#555", activeforeground="white")
        run_button.pack(side=tk.LEFT, padx=5)

        self.command_output = scrolledtext.ScrolledText(
            self.command_frame,
            height=15,
            font=("Courier", 12),
            state='disabled',
            bg="#2d2d2d",
            fg="white",
            insertbackground="white"
        )
        self.command_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def run_single_command(self):
        command = self.command_entry.get().strip()
        self.command_entry.delete(0, tk.END)
        if command:
            result = self.evaluate_expression(command)
            if command.upper() != "CLEAR":
                self.command_output.configure(state='normal')
                self.command_output.insert(tk.END, f"> {command}\n")
                if result:
                    self.command_output.insert(tk.END, result + "\n")
                self.command_output.see(tk.END)
                self.command_output.configure(state='disabled')

    def toggle_set_mode(self):
        self.set_mode = not self.set_mode
        self.set_button.config(text="SET MODE ON" if self.set_mode else "SET")

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
        if not tokens:
            return ""

        command = tokens[0].upper()

        if command == "VAR":
            if len(tokens) == 2:
                var = tokens[1].upper()
                self.hash_table.insert(var, 0)
                if var in self.var_value_labels:
                    self.var_value_labels[var].config(text=f"Value = 0")
                return "OK"
            elif len(tokens) >= 4 and tokens[2] == "=":
                var = tokens[1].upper()
                rhs_expr = ' '.join(tokens[3:])
                evaluated_rhs = self._evaluate_rhs(rhs_expr)
                if isinstance(evaluated_rhs, str) and evaluated_rhs.startswith("Error"):
                    return evaluated_rhs
                self.hash_table.insert(var, evaluated_rhs)
                if var in self.var_value_labels:
                    self.var_value_labels[var].config(text=f"Value = {evaluated_rhs}")
                return "OK"

        if len(tokens) >= 3 and tokens[1] == "=":
            var = tokens[0].upper()
            if not self.hash_table.key_exists(var):
                return f"Error: {var} is not declared"
            rhs_expr = ' '.join(tokens[2:])
            evaluated_rhs = self._evaluate_rhs(rhs_expr)
            if isinstance(evaluated_rhs, str) and evaluated_rhs.startswith("Error"):
                return evaluated_rhs
            self.hash_table.insert(var, evaluated_rhs, update_existing=True)
            if var in self.var_value_labels:
                self.var_value_labels[var].config(text=f"Value = {evaluated_rhs}")
            return "OK"

        if command == "PRINT":
            expr_to_print = ' '.join(tokens[1:])
            evaluated = self._evaluate_rhs(expr_to_print)
            if isinstance(evaluated, str) and evaluated.startswith("Error"):
                return evaluated
            return f"{expr_to_print.strip()} IS {evaluated}"

        if command == "START":
            self.hash_table.start_scope()
            return "Scope started"

        if command == "DONE":
            self.hash_table.finish_scope()
            return "Scope finished"

        if command == "CLEAR":
            self.command_output.configure(state='normal')
            self.command_output.delete("1.0", tk.END)
            self.command_output.configure(state='disabled')
            return ""

        if command == "RESET":
            self.hash_table = HashTable()
            for label in self.var_value_labels.values():
                label.config(text="Value = ")
            return "All variables and scopes reset"

        if command == "SHOW":
            in_scope_output = []
            out_of_scope_output = []
            for i, scope in enumerate(reversed(self.hash_table.scopes[:self.hash_table.current_scope_index + 1])):
                for bucket in scope.table:
                    current = bucket
                    while current:
                        entry = f"{current.key} = {current.value}"
                        if i == 0:
                            in_scope_output.append(entry)
                        else:
                            out_of_scope_output.append(entry)
                        current = current.next
            result_lines = []
            if out_of_scope_output:
                result_lines.append("Out of scope vars:")
                result_lines.extend([f"  {line}" for line in out_of_scope_output])
            if in_scope_output:
                result_lines.append("In scope vars:")
                result_lines.extend([f"  {line}" for line in in_scope_output])
            return "\n".join(result_lines) if result_lines else "No variables defined"

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