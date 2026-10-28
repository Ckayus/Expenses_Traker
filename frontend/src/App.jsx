
// import { useEffect, useState } from "react";

// const API_URL = "http://127.0.0.1:8000";

// function App() {
//   const [expenses, setExpenses] = useState([]);
//   const [description, setDescription] = useState("");
//   const [amount, setAmount] = useState("");
//   const [category, setCategory] = useState("Food");
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");
//   const [message, setMessage] = useState("");

//   async function fetchExpenses() {
//     const response = await fetch(`${API_URL}/expenses`);

//     if (!response.ok) {
//       throw new Error("Could not load expenses.");
//     }

//     const data = await response.json();
//     setExpenses(data);
//   }

//   useEffect(() => {
//     fetchExpenses()
//       .catch(() => setError("Could not connect to the API."))
//       .finally(() => setLoading(false));
//   }, []);

//   async function handleSubmit(event) {
//     event.preventDefault();
//     setError("");
//     setMessage("");

//     try {
//       const response = await fetch(`${API_URL}/expenses`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           description,
//           amount: Number(amount),
//           category,
//         }),
//       });

//       if (!response.ok) {
//         throw new Error("Could not add expense.");
//       }

//       await fetchExpenses();

//       setDescription("");
//       setAmount("");
//       setCategory("Food");
//       setMessage("Expense added successfully!");
//     } catch (err) {
//       setError(err.message || "Something went wrong.");
//     }
//   }
  
//   async function handleDelete(id) {
//     const confirmed = window.confirm(
//       "Are you sure you want to delete this expense?"
//     );
  
//     if (!confirmed) return;
  
//     try {
//       const response = await fetch(`${API_URL}/expenses/${id}`, {
//         method: "DELETE",
//       });
  
//       if (!response.ok) {
//         throw new Error("Could not delete expense.");
//       }
  
//       await fetchExpenses();
//       setMessage("Expense deleted successfully!");
//       setError("");
//     } catch (err) {
//       setError(err.message);
//       setMessage("");
//     }
//   }
  
  

//   const total = expenses.reduce(
//     (sum, expense) => sum + Number(expense.amount),
//     0
//   );

//   return (
//     <main>
//       <h1>My Expense Tracker</h1>

//       <h2>Total Expenses: ₦{total.toLocaleString()}</h2>

//       <h3>Add an Expense</h3>

//       <form onSubmit={handleSubmit}>
//         <div>
//           <label htmlFor="description">Description</label>
//           <input
//             id="description"
//             value={description}
//             onChange={(event) => setDescription(event.target.value)}
//             placeholder="e.g. Bought groceries"
//             required
//           />
//         </div>

//         <div>
//           <label htmlFor="amount">Amount (₦)</label>
//           <input
//             id="amount"
//             type="number"
//             min="0.01"
//             step="0.01"
//             value={amount}
//             onChange={(event) => setAmount(event.target.value)}
//             placeholder="e.g. 5000"
//             required
//           />
//         </div>

//         <div>
//           <label htmlFor="category">Category</label>
//           <select
//             id="category"
//             value={category}
//             onChange={(event) => setCategory(event.target.value)}
//           >
//             <option value="Food">Food</option>
//             <option value="Transport">Transport</option>
//             <option value="Utilities">Utilities</option>
//             <option value="Entertainment">Entertainment</option>
//             <option value="Other">Other</option>
//           </select>
//         </div>

//         <button type="submit">Add Expense</button>
//       </form>

//       {message && <p>{message}</p>}
//       {error && <p role="alert">{error}</p>}

//       <h3>Your Expenses</h3>

//       {loading ? (
//         <p>Loading expenses...</p>
//       ) : expenses.length === 0 ? (
//         <p>No expenses found.</p>
//       ) : (
//         <ul>
//             {expenses.map((expense) => (
//               <li key={expense.id}>
//                 {expense.description} — ₦
//                 {Number(expense.amount).toLocaleString()} (
//                 {expense.category})

                
//                 <button
//                   type="button"
//                   onClick={() => handleEdit(expense)}
//                 >
//                   Edit
//                 </button>

//                 <button
//                   type="button"
//                   onClick={() => handleDelete(expense.id)}
//                 >
//                   Delete
//                 </button>
//               </li>
//             ))}
//           </ul>
//       )}
//     </main>
//   );
// }

// export default App;


// async function handleEdit(expense) {
//   const description = window.prompt(
//     "Edit description:",
//     expense.description
//   );

//   if (description === null) return;

//   const amount = window.prompt(
//     "Edit amount:",
//     String(expense.amount)
//   );

//   if (amount === null) return;

//   const category = window.prompt(
//     "Edit category:",
//     expense.category
//   );

//   if (category === null) return;

//   if (!description.trim() || !Number.isFinite(Number(amount)) ||
//       Number(amount) <= 0 || !category.trim()) {
//     setError("Enter a valid description, positive amount, and category.");
//     return;
//   }

//   try {
//     const response = await fetch(
//       `${API_URL}/expenses/${expense.id}`,
//       {
//         method: "PUT",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           description: description.trim(),
//           amount: Number(amount),
//           category: category.trim(),
//         }),
//       }
//     );

//     if (!response.ok) {
//       throw new Error("Could not update expense.");
//     }

//     await fetchExpenses();
//     setMessage("Expense updated successfully!");
//     setError("");
//   } catch (err) {
//     setError(err.message);
//     setMessage("");
//   }
// }


import { useEffect, useMemo, useState } from "react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import "./App.css";

// The UI calls the local FastAPI service; its routes read/write the JSON files
// and return the records that drive the dashboard below.
const API_URL = "http://127.0.0.1:8000";

// Pie-chart slices use these colors in order, repeating when there are more
// categories than colors.
const CHART_COLORS = [
  "#0f766e",
  "#2563eb",
  "#f59e0b",
  "#9333ea",
  "#e11d48",
  "#64748b",
];

// Keep all displayed amounts in the same Nigerian naira format.
const formatMoney = (amount) =>
  new Intl.NumberFormat("en-NG", {
    style: "currency",
    currency: "NGN",
    maximumFractionDigits: 2,
  }).format(Number(amount) || 0);

function App() {
  // Server data and form inputs live in React state so successful requests
  // update the rendered dashboard without a full page reload.
  const [expenses, setExpenses] = useState([]);
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [categories, setCategories] = useState([]);
  const [newCategory, setNewCategory] = useState("");
  const [categorySaving, setCategorySaving] = useState(false);

  // Load saved expenses from GET /expenses and put them in state for all
  // summary values, charts, and transaction rows.
  async function fetchExpenses() {
    try {
      setError("");

      const response = await fetch(`${API_URL}/expenses`);

      if (!response.ok) {
        throw new Error("Could not load expenses.");
      }

      const data = await response.json();
      setExpenses(data);
    } catch (err) {
      setError(
        "Unable to connect to the backend. Check that FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  }

  // Load the category list used to populate the expense form's select menu.
  async function fetchCategories() {
    const response = await fetch(`${API_URL}/categories`);
  
    if (!response.ok) {
      throw new Error("Could not load categories.");
    }
  
    const data = await response.json();
    setCategories(data);
  
  }

  // Fetch initial data once when the dashboard first appears.
  useEffect(() => {
    fetchExpenses();
  
    fetchCategories().catch(() => {
      setError("Could not load categories from the backend.");
    });
  }, []);

  // Derive display values from the same expense list returned by the API;
  // useMemo avoids recomputing these aggregates when unrelated form state changes.
  const totalExpenses = useMemo(
    () =>
      expenses.reduce(
        (total, expense) => total + Number(expense.amount || 0),
        0
      ),
    [expenses]
  );

  const averageExpense =
    expenses.length > 0 ? totalExpenses / expenses.length : 0;

  const categoryData = useMemo(() => {
    const totals = {};

    expenses.forEach((expense) => {
      const name = expense.category || "Other";
      totals[name] = (totals[name] || 0) + Number(expense.amount || 0);
    });

    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value.toFixed(2)),
    }));
  }, [expenses]);

  const recentExpenses = useMemo(
    () => [...expenses].reverse().slice(0, 5),
    [expenses]
  );

  const barData = useMemo(
    () =>
      [...expenses]
        .reverse()
        .slice(0, 7)
        .map((expense) => ({
          name:
            expense.description.length > 14
              ? `${expense.description.slice(0, 14)}…`
              : expense.description,
          amount: Number(expense.amount || 0),
        })),
    [expenses]
  );

  // Send the new record to POST /expenses. An empty category is intentional:
  // the backend then predicts one from the description.
  async function handleAddExpense(event) {
    event.preventDefault();

    if (!description.trim() || !amount || Number(amount) <= 0) {
      setError("Enter a description and an amount greater than zero.");
      return;
    }

    try {
      setSaving(true);
      setError("");
      setMessage("");

      const response = await fetch(`${API_URL}/expenses`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: description.trim(),
          amount: Number(amount),
          category,
        }),
      });

      if (!response.ok) {
        throw new Error("Could not add the expense.");
      }

      setDescription("");
      setAmount("");
      setCategory("");
      setMessage("Expense added successfully.");

      await fetchExpenses();
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setSaving(false);
    }
  }

  

  // Delete the chosen record through the API, then reload the list so all
  // totals and charts stay synchronized with persisted data.
  async function handleDelete(id) {
    if (!window.confirm("Are you sure you want to delete this expense?")) {
      return;
    }

    try {
      setError("");
      setMessage("");

      const response = await fetch(`${API_URL}/expenses/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Could not delete the expense.");
      }

      setMessage("Expense deleted successfully.");
      await fetchExpenses();
    } catch (err) {
      setError(err.message || "Something went wrong.");
    }
  }

  // Edit uses prompts for the replacement values, PUTs the full record, then
  // reloads the list because the backend replaces the saved record.
  async function handleEdit(expense) {
    const newDescription = window.prompt(
      "Edit description:",
      expense.description
    );

    if (newDescription === null) return;

    const newAmount = window.prompt(
      "Edit amount:",
      String(expense.amount)
    );

    if (newAmount === null) return;

    const newCategory = window.prompt(
      "Edit category:",
      expense.category || "Other"
    );

    if (newCategory === null) return;

    if (!newDescription.trim() || !newAmount.trim() ||
        Number(newAmount) <= 0) {
      setError("Enter a valid description and positive amount.");
      return;
    }

    try {
      setError("");
      setMessage("");

      const response = await fetch(
        `${API_URL}/expenses/${expense.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            description: newDescription.trim(),
            amount: Number(newAmount),
            category: newCategory.trim() || "Other",
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Could not update the expense.");
      }

      setMessage("Expense updated successfully.");
      await fetchExpenses();
    } catch (err) {
      setError(err.message || "Something went wrong.");
    }
  }

// Add a category through POST /categories; reload the choices so the new
// category is immediately available in the expense form.
async function handleAddCategory(event) {
  event.preventDefault();

  const name = newCategory.trim();

  if (!name) {
    setError("Enter a category name.");
    return;
  }

  try {
    setCategorySaving(true);
    setError("");
    setMessage("");

    const response = await fetch(`${API_URL}/categories`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Could not add category.");
    }

    await fetchCategories();
    setCategory(name);
    setNewCategory("");
    setMessage(`Category "${name}" added successfully.`);
  } catch (err) {
    setError(err.message || "Something went wrong.");
  } finally {
    setCategorySaving(false);
  }
}

  return (
  /* The page is divided into navigation, financial summaries, visual
     breakdowns, recent records, and forms that write data back to the API. */
    <main className="dashboard">
      <aside className="sidebar">
        <div className="brand">
          <svg
            className="brand-icon"
            viewBox="0 0 32 32"
            role="img"
            aria-label="PennyPilot logo"
          >
            <path
              d="M5 22.5 12 15l5 4 9-10M21 9h5v5"
              fill="none"
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2.5"
            />
            <path
              d="M27 17v2.5A11 11 0 1 1 21.5 9"
              fill="none"
              stroke="currentColor"
              strokeLinecap="round"
              strokeWidth="2"
            />
          </svg>
          <span>PennyPilot</span>
        </div>

        <nav className="navigation">
          <a className="nav-link active" href="#dashboard">
            ◫ Dashboard
          </a>
          <a className="nav-link" href="#transactions">
            ⇄ Transactions
          </a>
          <a className="nav-link" href="#categories">
            ◉ Categories
          </a>
          <a className="nav-link" href="#add-expense">
            ＋ Add expense
          </a>
        </nav>

        <div className="sidebar-note">
          <span>✦</span>
          <strong>Smarter spending starts here.</strong>
          <p>Track your expenses and understand your habits.</p>
        </div>
      </aside>

      <section className="main-content" id="dashboard">
        <header className="page-header">
          <div>
            <p className="eyebrow">YOUR PERSONAL FINANCES</p>
            <h1>Expense Dashboard</h1>
            <p className="subtitle">
              Welcome back! Here is your spending overview.
            </p>
          </div>

          <button className="refresh-button" onClick={fetchExpenses}>
            ↻ Refresh
          </button>
        </header>

        {error && <div className="alert error">{error}</div>}
        {message && <div className="alert success">{message}</div>}

        {/* These cards summarize the same expense state used by both charts. */}
        <section className="summary-grid">
          <article className="summary-card primary-card">
            <span className="summary-label">Total Expenses</span>
            <h2>{formatMoney(totalExpenses)}</h2>
            <p>All recorded expenses</p>
          </article>

          <article className="summary-card">
            <span className="summary-label">Transactions</span>
            <h2>{expenses.length}</h2>
            <p>Recorded expenses</p>
          </article>

          <article className="summary-card">
            <span className="summary-label">Average Expense</span>
            <h2>{formatMoney(averageExpense)}</h2>
            <p>Per transaction</p>
          </article>
        </section>

        {/* Charts receive the pre-aggregated data derived above, not API calls. */}
        <section className="charts-grid">
          <article className="panel chart-panel" id="categories">
            <div className="panel-heading">
              <div>
                <h3>Spending by Category</h3>
                <p>How your expenses are distributed</p>
              </div>
            </div>

            {categoryData.length === 0 ? (
              <div className="empty-chart">
                Add an expense to see your category chart.
              </div>
            ) : (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={categoryData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="45%"
                      innerRadius={60}
                      outerRadius={95}
                      paddingAngle={3}
                    >
                      {categoryData.map((entry, index) => (
                        <Cell
                          key={entry.name}
                          fill={CHART_COLORS[index % CHART_COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value) => formatMoney(value)}
                    />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </article>

          <article className="panel chart-panel">
            <div className="panel-heading">
              <div>
                <h3>Expense Comparison</h3>
                <p>Your latest recorded expenses</p>
              </div>
            </div>

            {barData.length === 0 ? (
              <div className="empty-chart">
                Add an expense to see your bar chart.
              </div>
            ) : (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={barData}
                    margin={{ top: 10, right: 8, left: 8, bottom: 35 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis
                      dataKey="name"
                      angle={-25}
                      textAnchor="end"
                      interval={0}
                      height={60}
                      fontSize={11}
                    />
                    <YAxis
                      tickFormatter={(value) =>
                        value >= 1000
                          ? `₦${Math.round(value / 1000)}k`
                          : `₦${value}`
                      }
                      fontSize={11}
                    />
                    <Tooltip
                      formatter={(value) => formatMoney(value)}
                    />
                    <Bar
                      dataKey="amount"
                      name="Amount"
                      fill="#0f766e"
                      radius={[6, 6, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </article>
        </section>

        {/* Recent records offer edit/delete actions that call the matching API
            endpoints and then refresh the expense state. */}
        <section className="panel transactions-panel" id="transactions">
          <div className="panel-heading">
            <div>
              <h3>Recent Transactions</h3>
              <p>Your latest recorded expenses</p>
            </div>
            <span className="transaction-count">
              {expenses.length} total
            </span>
          </div>

          {loading ? (
            <p className="status-message">Loading expenses...</p>
          ) : recentExpenses.length === 0 ? (
            <p className="status-message">
              No expenses yet. Add your first expense below.
            </p>
          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {recentExpenses.map((expense) => (
                    <tr key={expense.id}>
                      <td>
                        <div className="expense-description">
                          <span className="expense-icon">₦</span>
                          <strong>{expense.description}</strong>
                        </div>
                      </td>
                      <td>
                        <span className="category-pill">
                          {expense.category || "Other"}
                        </span>
                      </td>
                      <td className="amount-cell">
                        {formatMoney(expense.amount)}
                      </td>
                      <td>
                        <div className="action-buttons">
                          <button
                            className="edit-button"
                            onClick={() => handleEdit(expense)}
                          >
                            Edit
                          </button>
                          <button
                            className="delete-button"
                            onClick={() => handleDelete(expense.id)}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Leaving the category blank asks the backend to classify the text. */}
        <section className="panel add-panel" id="add-expense">
          <div className="panel-heading">
            <div>
              <h3>Add an Expense</h3>
              <p>Record a new transaction</p>
            </div>
          </div>

          <form className="expense-form" onSubmit={handleAddExpense}>
            <label>
              Description
              <input
                type="text"
                placeholder="e.g. Grocery shopping"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                required
              />
            </label>

            <label>
              Amount (₦)
              <input
                type="number"
                min="0.01"
                step="0.01"
                placeholder="e.g. 12500"
                value={amount}
                onChange={(event) => setAmount(event.target.value)}
                required
              />
            </label>

            <label>
              Category
              <select
                value={category}
                onChange={(event) => setCategory(event.target.value)}
              >
                <option value="">Let AI predict</option>

                {categories.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                ))}
              </select>
            </label>

            <button className="submit-button" type="submit" disabled={saving}>
              {saving ? "Saving..." : "+ Add Expense"}
            </button>
          </form>
        </section>

        {/* Categories are maintained separately from labeled AI training
            examples; this form only adds a selectable category. */}
        <section className="panel add-panel">
          <div className="panel-heading">
            <div>
              <h3>Manage Categories</h3>
              <p>Create categories for your personal expenses.</p>
            </div>
          </div>

          <form className="expense-form" onSubmit={handleAddCategory}>
            <label>
              New Category
              <input
                type="text"
                placeholder="e.g. Personal Care"
                value={newCategory}
                onChange={(event) => setNewCategory(event.target.value)}
                maxLength={50}
                required
              />
            </label>

            <button
              className="submit-button"
              type="submit"
              disabled={categorySaving}
            >
              {categorySaving ? "Saving..." : "+ Add Category"}
            </button>
          </form>

          <p>Available categories: {categories.join(", ")}</p>
        </section>

        <footer className="dashboard-footer">
          PennyPilot · Personal expense tracking
        </footer>
      </section>
    </main>
  );
}

export default App;
