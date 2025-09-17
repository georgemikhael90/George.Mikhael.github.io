import streamlit as st
from datetime import date, datetime

# Optional imports from your project (wrapped to avoid import errors if missing)
try:
    from utils import calculate_total_pay, format_currency, get_available_grades, ServiceCategory
except Exception as e:
    calculate_total_pay = None
    format_currency = lambda x: f"${x:,.2f}"
    get_available_grades = lambda : ["E1","E2","E3","E4","E5","E6","E7","E8","E9","O1","O2","O3","O4","O5","O6"]
    class ServiceCategory:  # simple placeholder
        ACTIVE = "Active"
        RESERVE = "Reserve"

st.set_page_config(page_title="Pay Calculator", page_icon="💵", layout="centered")
st.title("Military Pay Calculator")
st.caption("Local single-file app scaffold you can open in Microsoft Visual Studio and run with Streamlit.")

col1, col2 = st.columns(2)
with col1:
    grade = st.selectbox("Grade", get_available_grades())
    service_cat = st.selectbox("Service Category", [getattr(ServiceCategory,'ACTIVE','Active'), getattr(ServiceCategory,'RESERVE','Reserve')])
    start_date = st.date_input("Start Date", date.today())
    end_date = st.date_input("End Date", date.today())
with col2:
    bh = st.number_input("Base Hours / Days", min_value=0.0, value=8.0, step=1.0)
    bonus = st.number_input("Bonus / Special Pay", min_value=0.0, value=0.0, step=50.0)
    deductions = st.number_input("Deductions", min_value=0.0, value=0.0, step=25.0)

calc = st.button("Calculate Pay")
if calc:
    # simple placeholder computation if your utils is missing
    num_days = (end_date - start_date).days + 1
    base = num_days * bh * 10  # replace with your own logic
    total = base + bonus - deductions

    if calculate_total_pay:
        try:
            total = calculate_total_pay(grade=grade, service_category=service_cat, start_date=start_date, end_date=end_date, base_hours=bh, bonus=bonus, deductions=deductions)
        except Exception as e:
            st.warning(f"Falling back to placeholder calculation because utils.calculate_total_pay errored: {e}")

    st.success(f"Estimated Total Pay: {format_currency(total) if callable(format_currency) else f'${total:,.2f}'}")

st.divider()
st.subheader("Export")
st.write("To add PDF/Excel exports, implement `generate_pdf_report` / `generate_excel_report` in `report_generators.py` and call them here.")
