import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Завантаження даних
data = pd.read_csv('stock_data.csv')

# Ініціалізація Dash додатка
app = dash.Dash(__name__)

# Макет додатка
app.layout = html.Div(
    children=[
        html.H1("Графік залежності ціни акцій"),
        dcc.Dropdown(
            id="stock-dropdown",
            options=[{"label": stock, "value": stock} for stock in data.columns[1:]],
            value=data.columns[1],
        ),
        dcc.Graph(id="stock-graph"),
    ]
)

# Оновлення графіку при виборі акції
@app.callback(
    Output("stock-graph", "figure"),
    [Input("stock-dropdown", "value")]
)
def update_graph(stock):
    fig = px.line(data, x="Date", y=stock)
    return fig

# Запуск додатка
if __name__ == '__main__':
    app.run_server(debug=True)