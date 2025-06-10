# app.py
from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd
from src.layout import create_layout
from src.callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

df = pd.read_csv("data/monthly_budget_data.csv")
df["Month"] = pd.to_datetime(df["Month"])  # Ensure datetime parsing

app.layout = create_layout(df)
register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)
