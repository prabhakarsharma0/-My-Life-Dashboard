import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="My Life Dashboard", page_icon="📊", layout="wide")
st.title("📊 My Life Dashboard")
st.caption("Upload a CSV with columns: date, category, amount")

uploaded = st.sidebar.file_uploader("Upload your CSV", type="csv")
source = uploaded if uploaded else "expenses.csv"

df = pd.read_csv(source)
df.columns = df.columns.str.strip().str.lower()

missing = {"date", "category", "amount"} - set(df.columns)
if missing:
    st.error(f"Your CSV is missing these columns: {', '.join(sorted(missing))}")
    st.stop()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df = df.dropna(subset=["date", "amount", "category"])

min_d, max_d = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date range", (min_d, max_d), min_value=min_d, max_value=max_d
)
if len(date_range) != 2:
    st.info("Select both a start date and an end date.")
    st.stop()
start, end = date_range

cats = sorted(df["category"].unique())
chosen = st.sidebar.multiselect("Categories", cats, default=cats)

mask = (
    (df["date"].dt.date >= start)
    & (df["date"].dt.date <= end)
    & (df["category"].isin(chosen))
)
view = df[mask]
if view.empty:
    st.warning("No data for these filters.")
    st.stop()

days = (end - start).days + 1
c1, c2, c3 = st.columns(3)
c1.metric("Total", f"{view['amount'].sum():,.0f}")
c2.metric("Average per day", f"{view['amount'].sum() / days:,.0f}")
c3.metric("Top category", view.groupby("category")["amount"].sum().idxmax())

daily = view.groupby(view["date"].dt.date)["amount"].sum().reset_index()
daily.columns = ["date", "amount"]
st.plotly_chart(px.line(daily, x="date", y="amount", title="Daily total"), use_container_width=True)

left, right = st.columns(2)
by_cat = view.groupby("category")["amount"].sum().reset_index()
left.plotly_chart(px.pie(by_cat, names="category", values="amount", title="By category"), use_container_width=True)

monthly = (
    view.assign(month=view["date"].dt.to_period("M").astype(str))
    .groupby("month")["amount"]
    .sum()
    .reset_index()
)
right.plotly_chart(px.bar(monthly, x="month", y="amount", title="Monthly total"), use_container_width=True)

with st.expander("See raw data"):
    st.dataframe(view)
