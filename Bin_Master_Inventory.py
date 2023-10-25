#!/usr/bin/env python
# coding: utf-8

# # Analysis of Bin Master Data

# In[ ]:


#pip install dash


# In[ ]:


#importing necessary libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import random
import string


# In[ ]:


data=pd.read_csv('Test_data2.csv')


# In[ ]:


data


# In[ ]:


data.dropna()


# In[ ]:


#sorting the bay and Ailse in an ascending order
data = data.sort_values(by=["BayNo", "AisleNo"],ascending=[True, True])


# In[ ]:


data.dropna()


# In[ ]:


data=data.dropna()


# In[ ]:


data['AisleNo'] = data['AisleNo'].str.upper()
# Convert 'BayNo' to integers
data['BayNo'] = data['BayNo'].astype(int)


# In[ ]:


data


# In[ ]:


#adding Bin_Type column with the random values
bin_type=[random.choice(['PickFace','Goodsin','Null']) for _ in range(len(data))]
#generating the random bin values for the len of the data


# In[ ]:


#adding new column and assigning the values to that column
data['BinType']=bin_type


# In[ ]:


#bin_zone=[random.choice(['A','B','C']) for _ in range(len(data))]
#assigning random values to the 
bin_zone=[random.choice(string.ascii_uppercase) for _ in range(len(data))]
data['BinZone']=bin_zone


# In[ ]:


data['FloorNo'] = data['FloorNo'].str.upper()  # Convert all floor values to uppercase


# In[ ]:


data


# In[ ]:




# Get unique floor numbers
floor_numbers = sorted(data['FloorNo'].unique())

app = dash.Dash(__name__)
server=app.server

app.layout = html.Div(children=[
    html.H1("Warehouse Bin Inventory", style={"text-align": "center"}),

    # Filter components
    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'flex': '1'}, children=[
            html.H2("Search by Stock Code"),
            dcc.Input(id="stock-code-input", placeholder="Enter Stock Code")
        ]),

        html.Div(style={'flex': '1'}, children=[
            html.H3("Filter by Bin Type"),
            dcc.Dropdown(
                id="bin-type-dropdown",
                options=[{"label": bin_type, "value": bin_type} for bin_type in data["BinType"].unique()],
                value="All",
                placeholder="Select below",
                style={"width": "150px", "height": "30px"},
                clearable=True,
            )
        ]),

        html.Div(style={'flex': '1'}, children=[
            html.H3("Filter by Bin Zone"),
            dcc.Dropdown(
                id="bin-zone-dropdown",
                options=[{"label": bin_zone, "value": bin_zone} for bin_zone in data["BinZone"].unique()],
                value="All",
                placeholder="Select below",
                style={"width": "150px", "height": "30px"},
                clearable=True,
            )
        ])
    ]),

    # Dynamic graphs
    html.Div(id='floor-graphs-container')
])

     

# Create dynamic graphs for each floor
def create_floor_graph(floor_number, filtered_data):
    fig = go.Figure(data=[go.Scatter(
        x=filtered_data["BayNo"],
        y=filtered_data["AisleNo"],
        mode="markers",
        marker_symbol="square",
        marker_size=25,
        marker_line_width=1,
        marker_line_color="black",
        marker_colorscale="Viridis",
        marker_cmin=0,
        marker_cmax=filtered_data["SumofStock"].max(),
        marker_color=filtered_data["SumofStock"],
        hoverinfo="text",
        hovertext=[
            f"BinNo: {row['BinNo']}<br>\nFloorNo: {row['FloorNo']}<br>\nAisleNo: {row['AisleNo']}<br>\nBayNo: {row['BayNo']}<br>\nBatchLotNo: {row['BatchLotNo']}<br>\nStockCode: {row['StockCode']}<br>\nStockInHand: {row['StockInHand']}<br>\nSumofStock: {row['SumofStock']}"
            for index, row in filtered_data.iterrows()
        ]
    )])

    fig.update_layout(
        title=f"Floor {floor_number} - Warehouse Bin Inventory",
        xaxis_title="BayNo",
        yaxis_title="AisleNo",
        xaxis_type="category",
        yaxis_type="category",
        coloraxis_colorbar=dict(title="SumofStock")
    )

    return fig

@app.callback(
    Output('floor-graphs-container', 'children'),
    [
        Input("stock-code-input", "value"),
        Input("bin-type-dropdown", "value"),
        Input("bin-zone-dropdown", "value")
    ]
)
def update_floor_graphs(stock_code, bin_type, bin_zone):
    filtered_data = data

    if stock_code is not None and stock_code != "":
        filtered_data = filtered_data[filtered_data["StockCode"] == stock_code]

    if bin_type != "All":
        filtered_data = filtered_data[filtered_data["BinType"] == bin_type]

    if bin_zone != "All":
        filtered_data = filtered_data[filtered_data["BinZone"] == bin_zone]

    floor_graphs = []

    for floor_number in floor_numbers:
        floor_data = filtered_data[filtered_data["FloorNo"] == floor_number]
        floor_graph = create_floor_graph(floor_number, floor_data)
        floor_graphs.append(
            dcc.Graph(
                figure=floor_graph,
                style={'width': '100%'}
            )
        )

    return floor_graphs

if __name__ == "__main__":
    app.run_server(debug=True)




