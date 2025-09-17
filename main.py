hazard_pay': 0, 'hardship_pay': 0, 'danger_pay': 0,
                    'special_pay': 0, 'allowances': 0, 'total': 0, 'per_diem': 0, 'minimum_income_adjustment':0
                })
                corr_month = correct_pay['monthly_breakdown'].get(month, {
                'days': 0, 'base_pay': 0, 'bah': 0, 'bas': 0,
                'hazard_pay': 0, 'hardship_pay': 0, 'danger_pay': 0,
                'special_pay': 0, 'allowances': 0, 'total': 0, 'per_diem': 0, 'minimum_income_adjustment':0
            })

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("Original Pay:")
                st.write(f"Base Pay: {format_currency(orig_month['base_pay'])}")
                if ServiceCategory(original_service_category) == ServiceCategory.TEXAS_SG:
                    st.write(f"Special Pay: {format_currency(orig_month.get('special_pay', 0))}")
                    st.write(f"Allowances: {format_currency(orig_month.get('allowances', 0))}")
                else:
                    st.write(f"BAH: {format_currency(orig_month['bah'])}")
                    st.write(f"BAS: {format_currency(orig_month['bas'])}")
                    st.write(f"Per Diem: {format_currency(orig_month['per_diem'])}")
                    if original_present_this_month:
                        if original_hazardous_duty:
                            st.write(f"Hazard Pay: {format_currency(orig_month.get('hazard_pay', 0))}")
                        if original_hardship_duty:
                            st.write(f"Hardship Pay: {format_currency(orig_month.get('hardship_pay', 0))}")
                        if original_at_border:
                            st.write(f"Danger Pay: {format_currency(orig_month.get('danger_pay', 0))}")
                    if orig_month.get('minimum_income_adjustment', 0)>0:
                        st.write(f"Min Income Adj: {format_currency(orig_month['minimum_income_adjustment'])}")
                st.write(f"Total: {format_currency(orig_month['total'])}")


            with col2:
                st.write("Correct Pay:")
                st.write(f"Base Pay: {format_currency(corr_month['base_pay'])}")
                if ServiceCategory(correct_service_category) == ServiceCategory.TEXAS_SG:
                    st.write(f"Special Pay: {format_currency(corr_month.get('special_pay', 0))}")
                    st.write(f"Allowances: {format_currency(corr_month.get('allowances', 0))}")
                else:
                    st.write(f"BAH: {format_currency(corr_month['bah'])}")
                    st.write(f"BAS: {format_currency(corr_month['bas'])}")
                    st.write(f"Per Diem: {format_currency(corr_month['per_diem'])}")
                    if correct_present_this_month:
                        if correct_hazardous_duty:
                            st.write(f"Hazard Pay: {format_currency(corr_month.get('hazard_pay', 0))}")
                        if correct_hardship_duty:
                            st.write(f"Hardship Pay: {format_currency(corr_month.get('hardship_pay', 0))}")
                        if correct_at_border:
                            st.write(f"Danger Pay: {format_currency(corr_month.get('danger_pay', 0))}")
                    if corr_month.get('minimum_income_adjustment', 0)>0:
                        st.write(f"Min Income Adj: {format_currency(corr_month['minimum_income_adjustment'])}")
                st.write(f"Total: {format_currency(corr_month['total'])}")

            with col3:
                st.write("Difference:")
                base_diff = corr_month['base_pay'] - orig_month['base_pay']
                st.write(f"Base Pay: {format_currency(base_diff)}")

                if ServiceCategory(original_service_category) == ServiceCategory.TEXAS_SG:
                    special_diff = corr_month.get('special_pay', 0) - orig_month.get('special_pay', 0)
                    allowances_diff = corr_month.get('allowances', 0) - orig_month.get('allowances', 0)
                    st.write(f"Special Pay: {format_currency(special_diff)}")
                    st.write(f"Allowances: {format_currency(allowances_diff)}")
                else:
                    bah_diff = corr_month['bah'] - orig_month['bah']
                    bas_diff = corr_month['bas'] - orig_month['bas']
                    per_diem_diff = corr_month['per_diem'] - orig_month['per_diem']
                    min_income_adj_diff = corr_month.get('minimum_income_adjustment', 0) - orig_month.get('minimum_income_adjustment', 0)

                    st.write(f"BAH: {format_currency(bah_diff)}")
                    st.write(f"BAS: {format_currency(bas_diff)}")
                    st.write(f"Per Diem: {format_currency(per_diem_diff)}")

                    if min_income_adj_diff != 0:
                        st.write(f"Min Income Adj: {format_currency(min_income_adj_diff)}")

                    if original_present_this_month or correct_present_this_month:
                        hazard_diff = corr_month.get('hazard_pay', 0) - orig_month.get('hazard_pay', 0)
                        hardship_diff = corr_month.get('hardship_pay', 0) - orig_month.get('hardship_pay', 0)
                        danger_diff = corr_month.get('danger_pay', 0) - orig_month.get('danger_pay', 0)

                        if original_hazardous_duty or correct_hazardous_duty:
                            st.write(f"Hazard Pay: {format_currency(hazard_diff)}")
                        if original_hardship_duty or correct_hardship_duty:
                            st.write(f"Hardship Pay: {format_currency(hardship_diff)}")
                        if original_at_border or correct_at_border:
                            st.write(f"Danger Pay: {format_currency(danger_diff)}")

                total_diff = corr_month['total'] - orig_month['total']
                st.metric(
                    "Monthly Difference",
                    format_currency(abs(total_diff)),
                    delta=format_currency(total_diff)
                )

    # Add report generation buttons for correction comparison
    st.subheader("📄 Generate Correction Reports")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Correction PDF Report", key="btn_pdf_report") and 'original_pay' in st.session_state:
            try:
                original_pay = st.session_state.original_pay
                pdf_file = generate_pdf_report(
                    original_pay,
                    ServiceCategory(correct_service_category),
                    correct_grade,
                    correct_years,
                    correct_start_date,
                    correct_end_date,
                    correct_dependents,
                    correct_hazardous_duty,
                    correct_hardship_duty,
                    correct_at_border,
                    sm_name,
                    sm_dodid,
                    sm_task_force,
                    sm_company,
                    is_correction=True,
                    original_details={
                        'service_category': original_service_category,
                        'grade': original_grade,
                        'years': original_years,
                        'start_date': original_start_date,
                        'end_date': original_end_date,
                        'dependents': original_dependents,
                        'hazardous_duty': original_hazardous_duty,
                        'hardship_duty': original_hardship_duty,
                        'at_border': original_at_border,
                        'present_this_month': original_present_this_month
                    }
                )
                st.markdown(
                    get_download_link(pdf_file, "📥 Download Correction PDF Report"),
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Error generating PDF report: {str(e)}")

    with col2:
        if st.button("Generate Correction Excel Report", key="btn_excel_report") and 'original_pay' in st.session_state:
            try:
                original_pay = st.session_state.original_pay
                excel_file = generate_excel_report(
                    original_pay,
                    ServiceCategory(correct_service_category),
                    correct_grade,
                    correct_years,
                    correct_start_date,
                    correct_end_date,
                    correct_dependents,
                    correct_hazardous_duty,
                    correct_hardship_duty,
                    correct_at_border,
                    sm_name,
                    sm_dodid,
                    sm_task_force,
                    sm_company,
                    is_correction=True,
                    original_details={
                        'service_category': original_service_category,
                        'grade': original_grade,
                        'years': original_years,
                        'start_date': original_start_date,
                        'end_date': original_end_date,
                        'dependents': original_dependents,
                        'hazardous_duty': original_hazardous_duty,
                        'hardship_duty': original_hardship_duty,
                        'at_border': original_at_border,
                        'present_this_month': original_present_this_month
                    }
                )
                st.markdown(
                    get_download_link(excel_file, "📥 Download Correction Excel Report"),
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Error generating Excel report: {str(e)}")

# Footer with signature
st.markdown("---")
st.markdown(
    '<div class="signature-container">Created by OLS JTF J1</div>',
    unsafe_allow_html=True
)

st.markdown("🪖 SAD Pay Calculator | Made with Streamlit")