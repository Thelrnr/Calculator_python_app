🧮 Advanced Python Calculator GUI

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![tkinter](https://img.shields.io/badge/GUI-tkinter-yellow?logo=python)
![Safe Eval](https://img.shields.io/badge/Secure-Evaluation-red)

A modern, secure, and fully-featured calculator app built with Python’s `tkinter`.  
This project goes beyond basic arithmetic—it includes parentheses support, calculation history, memory functions, and safe expression evaluation using Python's AST (Abstract Syntax Tree). Ideal for students, interns, and beginner developers learning GUI programming.


✨ Features
- ✅Safe Expression Evaluation (no `eval()`)
- 🧠Memory Functions: M+, M-, MR, MC
- 🕘Scrollable History Display
- 🧮Parentheses & Power Support
- 🔢Dynamic Font Size
- 🎨Clean UI with Grid Layout
- 💥Custom Popup Error Handling

---

🧠 How It Works

 🔧 GUI Setup (`tkinter`)
- Built using `Tk`, `Canvas`, and `Frame` for flexible layout.
- Buttons are generated using `functools.partial` for DRY code.
- Custom colors and fonts for better UX.

🧮 Expression Evaluation (No `eval()`)
- Input expressions are parsed using `ast.parse()`.
- The `evaluate_ast()` function walks through the AST to safely compute results.
- Supports `+`, `-`, `*`, `/`, `**`, and parentheses.

💾 Memory Operations
- Global `memory_value` stores temporary results.
- Buttons:
  - `M+` – Add to memory
  - `M-` – Subtract from memory
  - `MR` – Recall memory
  - `MC` – Clear memory

🕘 History Tracker
- A read-only scrollable `Text` widget logs each successful calculation.

---

📁 Project Structure

📦 calculator-project/
├── app.py # Main GUI app
└── README.txt # You're here!

yaml
Copy
Edit

---

▶️ Getting Started

🔃 Clone the Repository
```bash
git clone https://github.com/yourusername/advanced-python-calculator.git
cd advanced-python-calculator
🚀 Run the App
bash
Copy
Edit
python calculator.py
✅ No external dependencies required. Just Python 3.10+.

📌 Dependencies
Python Standard Library
tkinter
functools
ast

🌱 Ideal For
Python GUI beginners
Internship projects or academic demos
Learning safe expression handling
Portfolio builders

⚙️ Alternatives & Simplifications
🔁 Use eval() (not recommended) for early prototyping
🧮 Use libraries like sympy or simpleeval for math parsing
💡 Skip memory/history features initially and add them iteratively
📜 License
This project is licensed under the MIT License.

👨‍💻 Author
Made with 💻 by  Vinay
for details explaination of the code checkout my Linkedin profile

“Simplicity is the ultimate sophistication.” — Leonardo da Vinci
