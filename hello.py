from preswald import text, plotly, connect, get_df, table, query, slider
import pandas as pd
import plotly.express as px
import numpy as np

text("# My Data Analysis App")


connect()

sql = """
SELECT Country, Year, GDP_Per_Capita, Per_Capita_Sugar_Consumption
FROM sugar_csv
WHERE Country = 'China' AND Year BETWEEN 1980 AND 2023
"""
df = query(sql, "sugar_csv")

text("# Changes in Per Capita Sugar Consumption in China over Time and Per Capita GDP")

if df.empty:
    text("No data found for China between 1980 and 2023.")
else:

    df = df.dropna(subset=["GDP_Per_Capita", "Per_Capita_Sugar_Consumption"])
    df = df.groupby("Year", as_index=False)[["GDP_Per_Capita", "Per_Capita_Sugar_Consumption"]].mean()

    min_gdp = df["GDP_Per_Capita"].min()
    max_gdp = df["GDP_Per_Capita"].max()
    df["Bubble_Size"] = 10 + (df["GDP_Per_Capita"] - min_gdp) / (max_gdp - min_gdp) * 90

    threshold = slider("Select start year", min_val=1980, max_val=2023, default=1980)


    filtered_df = df[df["Year"] >= threshold]

    fig = px.scatter(
        filtered_df,
        x="Year",
        y="Per_Capita_Sugar_Consumption",
        size="Bubble_Size",
        color_discrete_sequence=["#1f77b4"],
        title="China's Per Capita Sugar Consumption 1980–2023 (Bubble Size = GDP)",
        size_max=30,
    )
    fig.update_traces(mode='markers+lines')
    fig.update_layout(template='plotly_white')

    plotly(fig)
    table(filtered_df, title="Dynamic Data View")
