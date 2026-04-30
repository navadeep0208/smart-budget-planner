# smart-budget-planner
A Python budget planning system that uses Greedy and Dynamic Programming (DP) algorithms to optimize expense allocation within a given budget. Features an interactive GUI built with tkinter.

---

## 📋 Project Report

### 1. Introduction

Managing a personal budget requires making decisions under constraints — a fixed amount of money must be allocated across many competing expenses, each with different costs and levels of importance. This is a classic optimization problem that maps directly onto two fundamental algorithm paradigms taught in class: **Greedy Algorithms** and **Dynamic Programming (DP)**.

This project implements a **Smart Budget Planner** — an interactive desktop application that allows a user to input their budget and a list of expenses (with cost and priority), then runs both a Greedy and a DP algorithm to determine the best allocation. The results are displayed side by side so the user can compare how each algorithm approaches the problem.

---

### 2. Objectives

- Build a functional system that applies **Greedy** and **Dynamic Programming** algorithms to a real-world problem
- Allow users to interactively input their budget and expenses through a **GUI**
- Run both algorithms on the same input and display results clearly
- Compare the outputs of both algorithms to illustrate their differences in approach and outcome

---

### 3. System Overview

The application is a **Personal Budget Planner** with a graphical user interface (GUI) built using Python's built-in `tkinter` library. No external libraries are required.

**How it works:**
1. User enters a total budget
2. User adds expenses (name, cost, priority from 1–5)
3. User clicks **RUN ALGORITHMS**
4. The system runs both algorithms and displays results across 3 tabs:
   - **Greedy Tab** — results from the Greedy approach
   - **DP Knapsack Tab** — results from the DP approach
   - **Comparison Tab** — side-by-side breakdown and conclusion

---

### 4. Algorithms Used

#### 4.1 Greedy Algorithm — Priority/Cost Ratio Strategy

**Problem:** Given a budget and a list of expenses, select expenses that maximize "value for money."

**Strategy:**
- For each expense, compute a **ratio = priority ÷ cost**
- Sort all expenses in descending order of this ratio
- Greedily select each expense (in order) if it fits within the remaining budget

**Why Greedy?**
This is analogous to the **Fractional Knapsack** problem, where the greedy approach of always picking the highest value-per-weight item is optimal. Here we use priority as "value" and cost as "weight."

**Time Complexity:** O(n log n) — dominated by sorting  
**Space Complexity:** O(n)

**Limitation:** Greedy does not evaluate all combinations. It makes locally optimal choices which may not always lead to the globally optimal solution in the 0/1 case.

---

#### 4.2 Dynamic Programming — 0/1 Knapsack

**Problem:** Find the combination of expenses that maximizes total priority score without exceeding the budget.

**Strategy:**
- Build a 2D DP table where `dp[i][w]` = maximum priority score achievable using the first `i` expenses with budget `w`
- For each expense, decide: **include it** (if it fits) or **exclude it**, whichever gives higher score
- Traceback through the table to find which expenses were selected

**Recurrence relation:**
```
dp[i][w] = max(
    dp[i-1][w],                            # exclude item i
    dp[i-1][w - cost[i]] + priority[i]     # include item i (if cost[i] <= w)
)
```

**Why DP?**
This is the classic **0/1 Knapsack Problem** — each expense is either fully included or excluded (unlike fractional knapsack). DP guarantees the globally optimal solution by systematically evaluating all possible combinations.

**Time Complexity:** O(n × W) where W = budget  
**Space Complexity:** O(n × W)

---

### 5. Comparison: Greedy vs Dynamic Programming

| Aspect | Greedy | Dynamic Programming |
|---|---|---|
| **Approach** | Locally optimal choices | Globally optimal (evaluates all combos) |
| **Speed** | Faster — O(n log n) | Slower — O(n × W) |
| **Optimality** | Not always optimal (0/1 case) | Always optimal |
| **Memory** | Low — O(n) | Higher — O(n × W) |
| **Best for** | Large inputs, quick estimates | Smaller inputs, exact optimal answer |

**Key insight:** In this system, DP will always find the combination with the highest total priority score. Greedy is faster but may miss a better combination because it decides item-by-item without looking ahead.

---

### 6. Implementation Details

**Language:** Python 3.7+  
**GUI Library:** `tkinter` (built-in, no installation needed)  
**External Libraries:** None

**Project Structure:**
```
budget_planner/
├── main.py       # Full application (algorithms + GUI)
└── README.md     # This report
```

**Key components in `main.py`:**

| Function | Description |
|---|---|
| `greedy_expense_allocation()` | Greedy algorithm — ratio-based selection |
| `dp_knapsack_budget()` | DP algorithm — 0/1 knapsack optimization |
| `BudgetPlannerApp` | Full tkinter GUI class |
| `_run_algorithms()` | Triggers both algorithms and updates all tabs |
| `_display_comparison()` | Side-by-side results with conclusion |

---

### 7. How to Run

**Requirements:**
- Python 3.7 or higher
- No external packages needed (`tkinter` is included with Python)

**Steps:**
```bash
python main.py
```

**Using the app:**
1. Set your total budget in the "Total Budget" field
2. Enter an expense name, cost, and priority (1–5 stars)
3. Click **＋ Add Expense** to add it to the list
4. Repeat for all expenses (or click **Load Sample Data** to try a preset)
5. Click **▶ RUN ALGORITHMS** to see results
6. Browse the 3 tabs: Greedy, DP Knapsack, and Comparison

---

### 8. Sample Output

Given a $1,000 budget with expenses like Rent ($500, ★★★★★), Groceries ($200, ★★★★★), Medical ($100, ★★★★★), Internet ($60, ★★★★), etc.:

- **Greedy** selects by best ratio first — fast, efficient, practical allocation
- **DP** selects the combination with the highest total priority score — mathematically optimal

The **Comparison tab** highlights differences and declares which algorithm performed better for that specific input.

---

### 9. Conclusion

This project demonstrates that classic algorithm paradigms — Greedy and Dynamic Programming — have direct, practical applications in everyday problems like budget management. The Greedy approach offers speed and simplicity, making it useful for large-scale or real-time scenarios. Dynamic Programming guarantees optimality by exhaustively evaluating combinations, making it ideal when precision matters most.

By building an interactive system around these algorithms, this project goes beyond textbook problems and shows how algorithms power real-world decision-making tools.
