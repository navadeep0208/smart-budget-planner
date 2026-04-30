"""
╔══════════════════════════════════════════════════════════════╗
║         SMART BUDGET PLANNER — CCC Algorithms Project        ║
║         Algorithms: Greedy + Dynamic Programming (DP)        ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont


# ══════════════════════════════════════════════════════════════
#  ALGORITHM CORE
# ══════════════════════════════════════════════════════════════

def greedy_expense_allocation(budget, expenses):
    """
    GREEDY ALGORITHM — Expense Prioritization
    ------------------------------------------
    Strategy: Sort expenses by priority/cost ratio (value-for-money).
    Always allocate to the highest-ratio expense that fits remaining budget.

    Parameters:
        budget   : total available budget (float)
        expenses : list of dict {name, cost, priority (1-5)}

    Returns:
        allocated : list of selected expense dicts
        total_spent: total amount spent
        remaining  : leftover budget
    """
    # Calculate ratio = priority / cost (higher = better value)
    for e in expenses:
        e['ratio'] = e['priority'] / e['cost'] if e['cost'] > 0 else 0

    sorted_expenses = sorted(expenses, key=lambda x: x['ratio'], reverse=True)

    allocated = []
    remaining = budget

    for expense in sorted_expenses:
        if expense['cost'] <= remaining:
            allocated.append(expense)
            remaining -= expense['cost']

    total_spent = budget - remaining
    return allocated, round(total_spent, 2), round(remaining, 2)


def dp_knapsack_budget(budget, expenses):
    """
    DYNAMIC PROGRAMMING — 0/1 Knapsack Budget Optimizer
    -----------------------------------------------------
    Strategy: Build a DP table to find the combination of expenses
    that maximizes total priority score within the budget.

    Parameters:
        budget   : total available budget (int, in whole units)
        expenses : list of dict {name, cost, priority}

    Returns:
        selected : list of selected expense dicts
        max_score: maximum priority score achieved
        total_cost: total cost of selected expenses
    """
    budget_int = int(budget)
    n = len(expenses)
    costs = [int(e['cost']) for e in expenses]
    priorities = [e['priority'] for e in expenses]

    # Build DP table
    dp = [[0] * (budget_int + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(budget_int + 1):
            dp[i][w] = dp[i - 1][w]
            if costs[i - 1] <= w:
                include = dp[i - 1][w - costs[i - 1]] + priorities[i - 1]
                if include > dp[i][w]:
                    dp[i][w] = include

    # Traceback
    selected = []
    w = budget_int
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(expenses[i - 1])
            w -= costs[i - 1]

    max_score = dp[n][budget_int]
    total_cost = sum(e['cost'] for e in selected)
    return list(reversed(selected)), max_score, round(total_cost, 2)


# ══════════════════════════════════════════════════════════════
#  GUI APPLICATION
# ══════════════════════════════════════════════════════════════

class BudgetPlannerApp:
    # ── Color Palette ──
    BG        = "#0f1117"
    PANEL     = "#1a1d27"
    CARD      = "#22263a"
    ACCENT    = "#4f8ef7"
    ACCENT2   = "#34d399"
    WARN      = "#f59e0b"
    TEXT      = "#e8eaf0"
    SUBTEXT   = "#8b92a8"
    BORDER    = "#2e3347"
    RED       = "#f87171"

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Budget Planner — CCC Algorithms Project")
        self.root.geometry("980x700")
        self.root.configure(bg=self.BG)
        self.root.resizable(True, True)

        self.expenses = []
        self._build_ui()

    # ── UI Builder ──────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=24, pady=(20, 0))

        tk.Label(header, text="💰 Smart Budget Planner",
                 font=("Georgia", 22, "bold"),
                 bg=self.BG, fg=self.TEXT).pack(side="left")

        tk.Label(header, text="Greedy  +  Dynamic Programming",
                 font=("Courier", 11),
                 bg=self.BG, fg=self.ACCENT).pack(side="right", pady=6)

        # Divider
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill="x", padx=24, pady=10)

        # Main layout
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=24, pady=0)

        # Left panel — Input
        left = tk.Frame(main, bg=self.PANEL, bd=0, relief="flat")
        left.pack(side="left", fill="y", padx=(0, 10), pady=4, ipadx=14, ipady=14)

        # Right panel — Results
        right = tk.Frame(main, bg=self.BG)
        right.pack(side="left", fill="both", expand=True, pady=4)

        self._build_input_panel(left)
        self._build_results_panel(right)

    def _build_input_panel(self, parent):
        tk.Label(parent, text="BUDGET SETUP", font=("Courier", 10, "bold"),
                 bg=self.PANEL, fg=self.ACCENT).pack(anchor="w", pady=(0, 10))

        # Budget entry
        tk.Label(parent, text="Total Budget ($)", font=("Georgia", 11),
                 bg=self.PANEL, fg=self.TEXT).pack(anchor="w")
        self.budget_var = tk.StringVar(value="1000")
        budget_entry = tk.Entry(parent, textvariable=self.budget_var,
                                font=("Courier", 13, "bold"),
                                bg=self.CARD, fg=self.ACCENT2,
                                insertbackground=self.TEXT,
                                relief="flat", bd=6, width=18)
        budget_entry.pack(anchor="w", pady=(2, 14))

        # Divider
        tk.Frame(parent, bg=self.BORDER, height=1).pack(fill="x", pady=6)

        tk.Label(parent, text="ADD EXPENSE", font=("Courier", 10, "bold"),
                 bg=self.PANEL, fg=self.ACCENT).pack(anchor="w", pady=(6, 10))

        # Expense Name
        tk.Label(parent, text="Expense Name", font=("Georgia", 10),
                 bg=self.PANEL, fg=self.SUBTEXT).pack(anchor="w")
        self.name_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.name_var,
                 font=("Georgia", 11), bg=self.CARD, fg=self.TEXT,
                 insertbackground=self.TEXT, relief="flat", bd=5, width=20
                 ).pack(anchor="w", pady=(2, 8))

        # Cost
        tk.Label(parent, text="Cost ($)", font=("Georgia", 10),
                 bg=self.PANEL, fg=self.SUBTEXT).pack(anchor="w")
        self.cost_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.cost_var,
                 font=("Georgia", 11), bg=self.CARD, fg=self.TEXT,
                 insertbackground=self.TEXT, relief="flat", bd=5, width=20
                 ).pack(anchor="w", pady=(2, 8))

        # Priority
        tk.Label(parent, text="Priority (1=Low → 5=High)", font=("Georgia", 10),
                 bg=self.PANEL, fg=self.SUBTEXT).pack(anchor="w")
        self.priority_var = tk.IntVar(value=3)
        pframe = tk.Frame(parent, bg=self.PANEL)
        pframe.pack(anchor="w", pady=(2, 10))
        for i in range(1, 6):
            tk.Radiobutton(pframe, text=str(i), variable=self.priority_var,
                           value=i, bg=self.PANEL, fg=self.TEXT,
                           selectcolor=self.ACCENT,
                           activebackground=self.PANEL,
                           font=("Courier", 10)).pack(side="left", padx=2)

        # Add button
        tk.Button(parent, text="＋  Add Expense",
                  command=self._add_expense,
                  font=("Georgia", 11, "bold"),
                  bg=self.ACCENT, fg="white",
                  activebackground="#3a7be0",
                  relief="flat", bd=0, cursor="hand2",
                  padx=12, pady=6).pack(fill="x", pady=(4, 12))

        # Divider
        tk.Frame(parent, bg=self.BORDER, height=1).pack(fill="x", pady=6)

        tk.Label(parent, text="EXPENSE LIST", font=("Courier", 10, "bold"),
                 bg=self.PANEL, fg=self.ACCENT).pack(anchor="w", pady=(6, 6))

        # Expense listbox
        listframe = tk.Frame(parent, bg=self.PANEL)
        listframe.pack(fill="both", expand=True)
        self.expense_list = tk.Listbox(listframe,
                                       font=("Courier", 9),
                                       bg=self.CARD, fg=self.TEXT,
                                       selectbackground=self.ACCENT,
                                       relief="flat", bd=0,
                                       height=8, width=26)
        self.expense_list.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(listframe, command=self.expense_list.yview)
        sb.pack(side="right", fill="y")
        self.expense_list.config(yscrollcommand=sb.set)

        # Remove + Clear buttons
        bframe = tk.Frame(parent, bg=self.PANEL)
        bframe.pack(fill="x", pady=(6, 4))
        tk.Button(bframe, text="Remove", command=self._remove_expense,
                  font=("Georgia", 9), bg=self.WARN, fg="white",
                  activebackground="#d97706", relief="flat", bd=0,
                  cursor="hand2", padx=8, pady=4).pack(side="left", padx=(0, 4))
        tk.Button(bframe, text="Clear All", command=self._clear_expenses,
                  font=("Georgia", 9), bg=self.RED, fg="white",
                  activebackground="#dc2626", relief="flat", bd=0,
                  cursor="hand2", padx=8, pady=4).pack(side="left")

        # Run button
        tk.Frame(parent, bg=self.BORDER, height=1).pack(fill="x", pady=8)
        tk.Button(parent, text="▶  RUN ALGORITHMS",
                  command=self._run_algorithms,
                  font=("Georgia", 12, "bold"),
                  bg=self.ACCENT2, fg="#0f1117",
                  activebackground="#22c55e",
                  relief="flat", bd=0, cursor="hand2",
                  padx=12, pady=8).pack(fill="x")

        # Load sample
        tk.Button(parent, text="Load Sample Data",
                  command=self._load_sample,
                  font=("Georgia", 9),
                  bg=self.CARD, fg=self.SUBTEXT,
                  activebackground=self.BORDER,
                  relief="flat", bd=0, cursor="hand2",
                  padx=8, pady=4).pack(fill="x", pady=(6, 0))

    def _build_results_panel(self, parent):
        # Tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=self.BG, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=self.CARD, foreground=self.SUBTEXT,
                        font=("Georgia", 11), padding=(14, 6))
        style.map("TNotebook.Tab",
                  background=[("selected", self.ACCENT)],
                  foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1 — Greedy
        self.greedy_frame = tk.Frame(self.notebook, bg=self.BG)
        self.notebook.add(self.greedy_frame, text="  Greedy Algorithm  ")

        # Tab 2 — DP
        self.dp_frame = tk.Frame(self.notebook, bg=self.BG)
        self.notebook.add(self.dp_frame, text="  DP Knapsack  ")

        # Tab 3 — Comparison
        self.cmp_frame = tk.Frame(self.notebook, bg=self.BG)
        self.notebook.add(self.cmp_frame, text="  Comparison  ")

        self._build_greedy_tab()
        self._build_dp_tab()
        self._build_comparison_tab()

    def _result_card(self, parent, title, color):
        frame = tk.Frame(parent, bg=self.CARD, bd=0)
        frame.pack(fill="both", expand=True, padx=8, pady=6)
        header = tk.Frame(frame, bg=color)
        header.pack(fill="x")
        tk.Label(header, text=title, font=("Courier", 11, "bold"),
                 bg=color, fg="white", padx=12, pady=6).pack(anchor="w")
        body = tk.Frame(frame, bg=self.CARD)
        body.pack(fill="both", expand=True, padx=10, pady=8)
        return body

    def _build_greedy_tab(self):
        tk.Label(self.greedy_frame,
                 text="Greedy — Priority/Cost Ratio Strategy",
                 font=("Georgia", 13, "bold"),
                 bg=self.BG, fg=self.TEXT).pack(anchor="w", padx=12, pady=(12, 2))
        tk.Label(self.greedy_frame,
                 text="Sorts expenses by priority÷cost ratio. Selects highest-value-for-money items first.",
                 font=("Georgia", 9), bg=self.BG, fg=self.SUBTEXT
                 ).pack(anchor="w", padx=12, pady=(0, 8))

        # Summary cards row
        self.g_summary = tk.Frame(self.greedy_frame, bg=self.BG)
        self.g_summary.pack(fill="x", padx=8)
        self.g_spent_lbl  = self._stat_card(self.g_summary, "Spent",     "$0",   self.ACCENT)
        self.g_remain_lbl = self._stat_card(self.g_summary, "Remaining", "$0",   self.ACCENT2)
        self.g_items_lbl  = self._stat_card(self.g_summary, "Items",     "0",    self.WARN)

        # Result text
        body = self._result_card(self.greedy_frame, "📋  Allocated Expenses", self.ACCENT)
        self.greedy_text = tk.Text(body, font=("Courier", 10),
                                   bg=self.CARD, fg=self.TEXT,
                                   relief="flat", bd=0,
                                   state="disabled", height=14,
                                   wrap="word")
        self.greedy_text.pack(fill="both", expand=True)

    def _build_dp_tab(self):
        tk.Label(self.dp_frame,
                 text="Dynamic Programming — 0/1 Knapsack Optimizer",
                 font=("Georgia", 13, "bold"),
                 bg=self.BG, fg=self.TEXT).pack(anchor="w", padx=12, pady=(12, 2))
        tk.Label(self.dp_frame,
                 text="Builds a DP table to find the combination that maximizes total priority score.",
                 font=("Georgia", 9), bg=self.BG, fg=self.SUBTEXT
                 ).pack(anchor="w", padx=12, pady=(0, 8))

        self.dp_summary = tk.Frame(self.dp_frame, bg=self.BG)
        self.dp_summary.pack(fill="x", padx=8)
        self.dp_score_lbl  = self._stat_card(self.dp_summary, "Priority Score", "0",  self.ACCENT)
        self.dp_cost_lbl   = self._stat_card(self.dp_summary, "Total Cost",     "$0", self.ACCENT2)
        self.dp_items_lbl  = self._stat_card(self.dp_summary, "Items",          "0",  self.WARN)

        body = self._result_card(self.dp_frame, "📋  Optimal Expense Selection", self.ACCENT2)
        self.dp_text = tk.Text(body, font=("Courier", 10),
                               bg=self.CARD, fg=self.TEXT,
                               relief="flat", bd=0,
                               state="disabled", height=14,
                               wrap="word")
        self.dp_text.pack(fill="both", expand=True)

    def _build_comparison_tab(self):
        tk.Label(self.cmp_frame,
                 text="Algorithm Comparison",
                 font=("Georgia", 13, "bold"),
                 bg=self.BG, fg=self.TEXT).pack(anchor="w", padx=12, pady=(12, 2))
        tk.Label(self.cmp_frame,
                 text="Side-by-side analysis of Greedy vs Dynamic Programming results.",
                 font=("Georgia", 9), bg=self.BG, fg=self.SUBTEXT
                 ).pack(anchor="w", padx=12, pady=(0, 8))

        body = self._result_card(self.cmp_frame, "📊  Results Breakdown", self.WARN)
        self.cmp_text = tk.Text(body, font=("Courier", 10),
                                bg=self.CARD, fg=self.TEXT,
                                relief="flat", bd=0,
                                state="disabled", height=20,
                                wrap="word")
        self.cmp_text.pack(fill="both", expand=True)

    def _stat_card(self, parent, label, value, color):
        frame = tk.Frame(parent, bg=self.CARD, padx=14, pady=8)
        frame.pack(side="left", padx=6, pady=6)
        tk.Label(frame, text=label, font=("Courier", 8),
                 bg=self.CARD, fg=self.SUBTEXT).pack()
        lbl = tk.Label(frame, text=value, font=("Georgia", 16, "bold"),
                       bg=self.CARD, fg=color)
        lbl.pack()
        return lbl

    # ── Actions ─────────────────────────────────────────────

    def _add_expense(self):
        name = self.name_var.get().strip()
        cost_str = self.cost_var.get().strip()
        priority = self.priority_var.get()

        if not name:
            messagebox.showerror("Error", "Please enter an expense name.")
            return
        try:
            cost = float(cost_str)
            if cost <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive cost.")
            return

        expense = {"name": name, "cost": cost, "priority": priority}
        self.expenses.append(expense)
        self.expense_list.insert(tk.END, f"{name:<16} ${cost:<8.0f}  ★{'★'*priority}{'☆'*(5-priority)}")
        self.name_var.set("")
        self.cost_var.set("")

    def _remove_expense(self):
        sel = self.expense_list.curselection()
        if not sel:
            return
        idx = sel[0]
        self.expense_list.delete(idx)
        self.expenses.pop(idx)

    def _clear_expenses(self):
        self.expense_list.delete(0, tk.END)
        self.expenses.clear()

    def _load_sample(self):
        self._clear_expenses()
        self.budget_var.set("1000")
        samples = [
            ("Rent",         500, 5),
            ("Groceries",    200, 5),
            ("Internet",      60, 4),
            ("Electricity",   80, 4),
            ("Gym",           40, 2),
            ("Netflix",       15, 2),
            ("Books",         50, 3),
            ("Dining Out",   120, 3),
            ("Clothing",     150, 2),
            ("Medical",      100, 5),
        ]
        for name, cost, pri in samples:
            self.expenses.append({"name": name, "cost": cost, "priority": pri})
            self.expense_list.insert(tk.END,
                f"{name:<16} ${cost:<8.0f}  ★{'★'*pri}{'☆'*(5-pri)}")

    def _run_algorithms(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "Please add at least one expense.")
            return
        try:
            budget = float(self.budget_var.get())
            if budget <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget.")
            return

        # Deep copy to avoid mutation
        import copy
        exp_copy = copy.deepcopy(self.expenses)

        # Run Greedy
        g_alloc, g_spent, g_remain = greedy_expense_allocation(budget, exp_copy)

        # Run DP
        exp_copy2 = copy.deepcopy(self.expenses)
        dp_alloc, dp_score, dp_cost = dp_knapsack_budget(budget, exp_copy2)

        self._display_greedy(g_alloc, g_spent, g_remain, budget)
        self._display_dp(dp_alloc, dp_score, dp_cost, budget)
        self._display_comparison(g_alloc, g_spent, g_remain,
                                  dp_alloc, dp_score, dp_cost, budget)
        self.notebook.select(0)

    def _write_text(self, widget, content):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content)
        widget.config(state="disabled")

    def _display_greedy(self, allocated, spent, remaining, budget):
        self.g_spent_lbl.config(text=f"${spent:.0f}")
        self.g_remain_lbl.config(text=f"${remaining:.0f}")
        self.g_items_lbl.config(text=str(len(allocated)))

        lines = ["GREEDY ALLOCATION RESULT\n"]
        lines.append(f"Budget : ${budget:.2f}")
        lines.append(f"Spent  : ${spent:.2f}")
        lines.append(f"Left   : ${remaining:.2f}\n")
        lines.append(f"{'#':<4} {'Expense':<18} {'Cost':>8}  {'Priority':>8}  {'Ratio':>8}")
        lines.append("─" * 54)
        for i, e in enumerate(allocated, 1):
            ratio = e['priority'] / e['cost']
            lines.append(f"{i:<4} {e['name']:<18} ${e['cost']:>7.2f}  {'★'*e['priority']:<8}  {ratio:>8.4f}")
        lines.append("─" * 54)
        lines.append(f"{'TOTAL':<23} ${spent:>7.2f}")

        not_selected = [e for e in self.expenses
                        if e['name'] not in [a['name'] for a in allocated]]
        if not_selected:
            lines.append(f"\n⚠  Couldn't fit ({len(not_selected)} items):")
            for e in not_selected:
                lines.append(f"   - {e['name']} (${e['cost']:.2f})")

        self._write_text(self.greedy_text, "\n".join(lines))

    def _display_dp(self, selected, score, total_cost, budget):
        self.dp_score_lbl.config(text=str(score))
        self.dp_cost_lbl.config(text=f"${total_cost:.0f}")
        self.dp_items_lbl.config(text=str(len(selected)))

        lines = ["DP KNAPSACK OPTIMAL RESULT\n"]
        lines.append(f"Budget        : ${budget:.2f}")
        lines.append(f"Total Cost    : ${total_cost:.2f}")
        lines.append(f"Priority Score: {score}\n")
        lines.append(f"{'#':<4} {'Expense':<18} {'Cost':>8}  {'Priority':>8}")
        lines.append("─" * 46)
        for i, e in enumerate(selected, 1):
            lines.append(f"{i:<4} {e['name']:<18} ${e['cost']:>7.2f}  {'★'*e['priority']}")
        lines.append("─" * 46)
        lines.append(f"{'TOTAL':<23} ${total_cost:>7.2f}  Score: {score}")

        not_selected = [e for e in self.expenses
                        if e['name'] not in [a['name'] for a in selected]]
        if not_selected:
            lines.append(f"\n⚠  Not selected ({len(not_selected)} items):")
            for e in not_selected:
                lines.append(f"   - {e['name']} (${e['cost']:.2f})")

        self._write_text(self.dp_text, "\n".join(lines))

    def _display_comparison(self, g_alloc, g_spent, g_remain,
                             dp_alloc, dp_score, dp_cost, budget):
        g_score = sum(e['priority'] for e in g_alloc)
        dp_remain = budget - dp_cost

        winner_score = "DP" if dp_score > g_score else ("Greedy" if g_score > dp_score else "Tie")
        winner_spend = "DP" if dp_cost > g_spent else ("Greedy" if g_spent > dp_cost else "Tie")

        lines = ["╔══════════════════════════════════════════╗"]
        lines.append("║         ALGORITHM COMPARISON             ║")
        lines.append("╚══════════════════════════════════════════╝\n")
        lines.append(f"{'Metric':<28} {'Greedy':>10}  {'DP':>10}")
        lines.append("─" * 52)
        lines.append(f"{'Budget':<28} ${budget:>9.2f}  ${budget:>9.2f}")
        lines.append(f"{'Total Spent':<28} ${g_spent:>9.2f}  ${dp_cost:>9.2f}")
        lines.append(f"{'Remaining':<28} ${g_remain:>9.2f}  ${dp_remain:>9.2f}")
        lines.append(f"{'Items Selected':<28} {len(g_alloc):>10}  {len(dp_alloc):>10}")
        lines.append(f"{'Total Priority Score':<28} {g_score:>10}  {dp_score:>10}")
        lines.append("─" * 52)

        lines.append(f"\n🏆 Higher Priority Score : {winner_score}")
        lines.append(f"💵 More Budget Used       : {winner_spend}\n")

        lines.append("── Greedy Selected ──")
        for e in g_alloc:
            lines.append(f"  ✔ {e['name']}")

        lines.append("\n── DP Selected ──")
        for e in dp_alloc:
            lines.append(f"  ✔ {e['name']}")

        only_dp = [e for e in dp_alloc if e['name'] not in [x['name'] for x in g_alloc]]
        only_g  = [e for e in g_alloc  if e['name'] not in [x['name'] for x in dp_alloc]]

        if only_dp:
            lines.append("\n── Only in DP (DP found these, Greedy missed) ──")
            for e in only_dp:
                lines.append(f"  ➕ {e['name']}")
        if only_g:
            lines.append("\n── Only in Greedy (Greedy found these, DP skipped) ──")
            for e in only_g:
                lines.append(f"  ➕ {e['name']}")

        lines.append("\n── Conclusion ──")
        if dp_score > g_score:
            lines.append("  DP Knapsack achieves a higher priority score by")
            lines.append("  evaluating ALL combinations. Greedy is faster but")
            lines.append("  may miss the globally optimal solution.")
        elif g_score > dp_score:
            lines.append("  Greedy achieved a higher score here, which can happen")
            lines.append("  when the priority/cost ratios align well.")
        else:
            lines.append("  Both algorithms reached the same result for this input!")

        self._write_text(self.cmp_text, "\n".join(lines))


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetPlannerApp(root)
    root.mainloop()
