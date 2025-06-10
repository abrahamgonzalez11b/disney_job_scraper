# src/callbacks.py
from dash import Input, Output, State
import plotly.express as px
import pandas as pd
from dash import dcc

def register_callbacks(app, df):

    @app.callback(
        Output("budget-vs-actual", "figure"),
        Output("variance-table", "data"),
        Input("view-selector", "value")
    )
    def update_view(view_type):
        dff = df.copy()
        dff["Variance"] = dff["Budget"] - dff["Actual"]

        if view_type == "Quarterly":
            dff["Quarter"] = dff["Month"].dt.to_period("Q").astype(str)
            grouped = dff.groupby("Quarter")[["Budget", "Actual"]].sum().reset_index()
            grouped["Variance"] = grouped["Budget"] - grouped["Actual"]
            grouped.rename(columns={"Quarter": "Month"}, inplace=True)
        else:
            grouped = dff.copy()
            grouped["Month"] = grouped["Month"].dt.strftime("%b %Y")

        fig = px.bar(
            grouped,
            x="Month",
            y=["Budget", "Actual"],
            barmode="group",
            title=f"{view_type} Budget vs Actual",
            labels={"value": "Amount", "variable": "Category"}
        )
        fig.update_layout(xaxis_tickangle=-45)

        return fig, grouped.to_dict("records")

    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("btn-download", "n_clicks"),
        State("variance-table", "data"),
        prevent_initial_call=True
    )
    def download_csv(n_clicks, data):
        df_download = pd.DataFrame(data)
        return dcc.send_data_frame(df_download.to_csv, "budget_variance.csv", index=False)
