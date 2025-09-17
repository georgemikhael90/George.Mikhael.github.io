# Pay Calculator — Microsoft Visual Studio (Windows) Setup

## 1) Install prerequisites
- **Microsoft Visual Studio 2022** (Community is fine)
  - During install, check **Python development** workload.
- **Python 3.11 or 3.12 (64‑bit)** installed on Windows (from python.org).

## 2) Open this folder in Visual Studio
- Start Visual Studio → **Open a local folder** → select this `msvs_pay_calculator` folder.

## 3) Create and select a virtual environment
- View → Other Windows → **Python Environments**.
- Click **+** to **Add environment** → **Virtual environment** → Base interpreter: your Python 3.11/3.12 → Create.
- Right‑click the environment → **Activate**.

## 4) Install dependencies
- Open **Terminal** panel (View → Terminal) and run:
  ```
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

## 5) Run the app (Streamlit)
- In the terminal:
  ```
  streamlit run app.py
  ```
- A browser window opens at `http://localhost:8501`.

## 6) Wire up your business logic
- If you already have `utils.py` and `report_generators.py`, copy them into this folder (or replace the stubs).
- Ensure `utils.py` defines:
  ```python
  def calculate_total_pay(grade, service_category, start_date, end_date, base_hours, bonus, deductions) -> float: ...
  def format_currency(x: float) -> str: ...
  def get_available_grades() -> list[str]: ...
  class ServiceCategory: ...
  ```
- Ensure `report_generators.py` defines:
  ```python
  def generate_pdf_report(data_dict: dict, output_path: str) -> str: ...
  def generate_excel_report(data_dict: dict, output_path: str) -> str: ...
  ```

## 7) Debug inside Visual Studio
- Debug → **New Configuration** → choose **Python**.
- Program: the full path to your `streamlit` executable (inside the venv), e.g.:
  `C:\...\msvs_pay_calculator\.venv\Scripts\streamlit.exe`
- Arguments: `run app.py`
- Working directory: this folder.
- Now press **F5** to debug.

## 8) Package to an EXE (optional)
- Install PyInstaller in your venv:
  ```
  pip install pyinstaller
  ```
- Create a simple CLI entry point (optional): `cli.py`
  ```python
  import subprocess, sys
  if __name__ == "__main__":
      sys.exit(subprocess.call(["streamlit", "run", "app.py"]))
  ```
- Build:
  ```
  pyinstaller --onefile --noconsole cli.py
  ```
- Your EXE will be in `dist/cli.exe`. You can ship this with your `app` folder.

## 9) Troubleshooting
- If port 8501 is blocked, run with `streamlit run app.py --server.port 8502`.
- If imports fail, confirm your activated interpreter is the venv you created in Step 3.
- If `pyarrow` errors on Windows, reinstall with: `pip install --upgrade --force-reinstall pyarrow`.

## 10) Alternative UI (fully offline desktop)
- If you prefer a pure desktop app (no browser), swap Streamlit for **Tkinter** or **PyQt6** and run directly via Python.

---
_This starter is intentionally minimal so you can drop in your own pay rules and report code._
