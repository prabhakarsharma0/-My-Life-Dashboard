# My Life Dashboard

A free Streamlit app that turns any CSV (`date`, `category`, `amount`) into an interactive dashboard with charts and filters.

**Live demo:** [https://my-life-dashboardd.streamlit.app](https://my-life-dashboardd.streamlit.app)

![Dashboard screenshot](images/dashboard.png)

---

## What it does

- Upload a CSV or use the sample `expenses.csv`
- Filter by date range and category
- See:
  - Total spend
  - Average per day
  - Top category
  - Daily line chart
  - Category pie chart
  - Monthly bar chart

No Excel. No pivot tables. Upload a new file and the charts update.

![Demo GIF](images/demo.gif)

---

## Project files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit dashboard |
| `expenses.csv` | Sample data for demo |
| `requirements.txt` | Python dependencies |
| `images/` | Screenshots and demo GIF |

---

## CSV format

Your file needs these 3 columns:

| Column | Example |
|--------|---------|
| `date` | 2026-07-15 |
| `category` | Food |
| `amount` | 250.50 |

Column names are cleaned automatically (spaces and capital letters are handled).

---

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
