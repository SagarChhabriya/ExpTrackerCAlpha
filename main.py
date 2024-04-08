import streamlit as st
import plotly.graph_objects as go
import calendar
from streamlit_option_menu import option_menu # pip install streamlit-option-menu

#----------------SETTINGS---------------
incomes = ["Salary","Blog","Other income"]
expenses = ["Rent","Utilites","Groceries","Car","Other Expenses","Saving"]
currency = "USD"
page_title = "Expense Tracker"
page_icon = ":money_with_wings:"
layout = "centered"
#---------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " "+ page_icon)

#------------DROP down values for selecting the period
years = [2022, 2023,2024]
months = list(calendar.month_name[1:])

# ----------------- Hide Streamlit Style----- Using CSS
hide_st_style = """
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            header{visibility: hidden;}
            </style>

"""
st.markdown(hide_st_style, unsafe_allow_html=True)



# -------Navigation Menu
selected = option_menu(
    menu_title=None,
    options=["Data Entry","Data Visualization"],
    icons=["pencil-fill",'bar-chart-fill'], # https://icons.getbootstrap.com/
    orientation="horizontal"
)

# selected_year = st.sidebar.selectbox("Select Year", years)
# selected_month = st.sidebar.multiselect("Select Month (hold ctrl to select multiple)", months)

# -----Inputs & Save Periods
if selected=="Data Entry":
    st.header(f"Data Entry in {currency}")
    # Create form
    with st.form("entry_form",clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month: ", months, key="month")
        col2.selectbox("Select Year",years,key="year")

        "---"

        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0,format="%i",step=10, key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:",min_value=0,format="%i",step=10, key=expense)
        with st.expander("Comment"):
            comment = st.text_area("",placeholder="Enter a comment here...")

        "---"
        submmitted = st.form_submit_button("Save Data")
        if submmitted:
            period = str(st.session_state["year"])  + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes} # Dict comprehension
            expenses = {expense: st.session_state[expense] for expense in expenses}
            # TODO : Insert values into database
            st.write(f"income: {incomes}")
            st.write(f"expenses: {expenses}")
            st.success("Data saved!")

# --------Plot Periods
if selected=="Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        # TODO: Get periods from database
        period = st.selectbox("Select Period : ", ["2022_March"])
        submmitted = st.form_submit_button("Plot Period")
        if submmitted:
            # TODO: Get data from database
            comment = "Some comment"
            incomes = {'Salary':1500, 'Blog':50, "Other Income":10 }
            expenses= {"Rent":600, "Utilities":200, "Groceries":300, "Car":100, "Other Expenses":50,"Saving":10}

            # Create metrics
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income",f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
            st.text(f"Comment: {comment}")
            
            # Create sankey chart
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
            value = list(incomes.values()) + list(expenses.values())

            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

            # Plot it!
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)