from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0
    ),
    dcc.Graph(id='live-update-graph'),
    html.Div(id='live-update-text')
])

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('SELECT profit FROM trades ORDER BY id DESC LIMIT 50')
    profits = c.fetchall()
    profits = [p[0] for p in profits]
    conn.close()

    # Create the graph with subplots
    fig = go.Figure(data=[go.Scatter(x=list(range(len(profits))), y=profits)])
    return fig

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    metrics = calculate_performance_db()
    return html.Div([
        html.P(f"Win Rate: {metrics['win_rate']*100:.2f}%"),
        html.P(f"Average Profit: {metrics['average_profit']:.2f}"),
        html.P(f"Max Drawdown: {metrics['max_drawdown']:.2f}")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
