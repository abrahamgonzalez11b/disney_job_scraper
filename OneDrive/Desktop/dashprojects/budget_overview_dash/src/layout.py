# src/layout.py
from dash import html, dcc
from dash import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

def create_layout(df):
    df["Variance"] = df["Budget"] - df["Actual"]
    total_budget = df["Budget"].sum()
    total_actual = df["Actual"].sum()
    variance = total_budget - total_actual

    fig = px.bar(
        df,
        x=df["Month"].dt.strftime("%b %Y"),
        y=["Budget", "Actual"],
        barmode="group",
        title="Monthly Budget vs Actual",
        labels={"value": "Amount", "variable": "Category"}
    )

    return dbc.Container([
        html.H1("Budget Overview Dashboard", className="text-center my-4"),

        # Dropdown Filter
        html.Div([
            html.Label("Select View:"),
            dcc.Dropdown(
                id="view-selector",
                options=[
                    {"label": "Monthly View", "value": "Monthly"},
                    {"label": "Quarterly View", "value": "Quarterly"}
                ],
                value="Monthly"
            )
        ], className="mb-4"),

        # KPI Cards
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Total Budget"),
                html.H2(f"${total_budget:,.2f}")
            ])), width=4),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Total Actual"),
                html.H2(f"${total_actual:,.2f}")
            ])), width=4),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Variance"),
                html.H2(f"${variance:,.2f}", className="text-success" if variance >= 0 else "text-danger")
            ])), width=4),
        ], className="mb-4"),

        # Bar Chart
        dcc.Graph(id="budget-vs-actual", figure=fig),

        # Variance Table
        html.H4("Monthly Variance Table"),
        dash_table.DataTable(
            id="variance-table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center"},
            style_header={"fontWeight": "bold"}
        ),

        html.Br(),
        html.Button("Download CSV", id="btn-download", className="btn btn-primary"),
        dcc.Download(id="download-dataframe-csv")
    ])
