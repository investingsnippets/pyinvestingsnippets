import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.long_callback import DiskcacheLongCallbackManager

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

import datetime
import diskcache

import pandas_datareader as web

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import pyinvestingsnippets 

ASSET_TICKERS = ['Asset1', 'Asset2', 'Asset3', 'Asset4']
BENCHMARK_TICKERS = ['Bench1', 'Bench2']

def tracking_error(r_a, r_b):
    """
    Returns the Tracking Error between the two return series
    """
    return np.sqrt(((r_a - r_b)**2).sum())

def information_ratio(returns, benchmark_returns, periods=252):
    """It measures a trader’s ability to generate excess returns relative to a benchmark."""
    return_difference = returns.annualized(periods) - benchmark_returns.annualized(periods)
    volatility = (returns - benchmark_returns).std() * (periods ** 0.5)
    information_ratio = return_difference.mean() / volatility
    return information_ratio

def modigliani_ratio(returns, benchmark_returns, rf, periods=252):
    """The Modigliani ratio (M2) measures the returns of the portfolio,
    adjusted for the risk of the portfolio relative to that of some benchmark."""
    sharpe_ratio = returns.sharpe(rf, periods)
    benchmark_volatility = benchmark_returns.volatility_annualized(periods)
    m2_ratio = (sharpe_ratio * benchmark_volatility) + rf
    return m2_ratio

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig


def gbm(n_years = 10, n_scenarios=1000, mu=0.07, sigma=0.15, steps_per_year=12, s_0=100.0, prices=True):
    """
    Geometric Brownian Motion
    """
    dt = 1/steps_per_year
    n_steps = int(n_years*steps_per_year) + 1
    # the standard way ...
    # rets_plus_1 = np.random.normal(loc=mu*dt+1, scale=sigma*np.sqrt(dt), size=(n_steps, n_scenarios))
    # without discretization error ...
    rets_plus_1 = np.random.normal(loc=(1+mu)**dt, scale=(sigma*np.sqrt(dt)), size=(n_steps, n_scenarios))
    rets_plus_1[0] = 1
    ret_val = s_0*pd.DataFrame(rets_plus_1).cumprod() if prices else rets_plus_1-1
    return ret_val

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '22%',
    'margin-right': '2%',
    'padding': '10px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

controls = dbc.Row(
    [
        html.P('Tickers', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown_tickers',
            options=[{'label': i, 'value': i} for i in ASSET_TICKERS],
            value=[],  # default value
            multi=True
        ),
        html.P('Benchmark', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown_benchmark',
            options=[{'label': i, 'value': i} for i in BENCHMARK_TICKERS],
            value=[],  # default value
            multi=False
        ),
        html.Br(),
        html.P('Years', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_years',
            options=[{
                    'label': '1',
                    'value': 1
                },
                {
                    'label': '3',
                    'value': 3
                },
                {
                    'label': '5',
                    'value': 5
                }
            ],
            value=5,
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        html.P('Rolling Window (days)', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_rolling_window',
            options=[{
                    'label': '30',
                    'value': 30
                },
                {
                    'label': '90',
                    'value': 90
                },
                {
                    'label': '252',
                    'value': 252
                }
            ],
            value=252,
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Apply',
            color='primary'
        ),
        html.Button("Cancel Running Job!", id="cancel_button_id", style={"display": "none"}),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls,
        html.Div(
            [
                html.Progress(id="progress_bar", style={"display": "none"}),
            ]
        ),
    ],
    style=SIDEBAR_STYLE,
)

content_wealthindex = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_wi', figure = blank_fig()), md=12
        )
    ]
)

content_drawdown = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_dd', figure = blank_fig()), md=12,
        )
    ]
)

content_annual_rets = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_arets', figure = blank_fig()), md=12,
        )
    ]
)

content_rolling = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_rolling_rets', figure = blank_fig()), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_rolling_vol', figure = blank_fig()), md=6
        )
    ]
)

content_risk_reward = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_risk_reward', figure = blank_fig()), md=12,
        )
    ]
)

content_stats = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_stats', figure = blank_fig()), md=12,
        )
    ]
)

content = html.Div(
    [
        dcc.Store(id='memory'),
        html.H2('Report', style=TEXT_STYLE),
        html.Hr(),
        content_wealthindex,
        content_drawdown,
        content_annual_rets,
        content_rolling,
        content_risk_reward,
        content_stats,
    ],
    style=CONTENT_STYLE
)


cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)
app.layout = html.Div([sidebar, content])

@app.long_callback(Output('memory', 'data'),
              [Input('submit_button', 'n_clicks')],
              [State('dropdown_tickers', 'value'),
                State('dropdown_benchmark', 'value'),
                State('radio_years', 'value'),
                State('radio_rolling_window', 'value')
              ],
              running=[
                (Output("submit_button", "disabled"), True, False),
                (Output("cancel_button_id", "disabled"), False, True),
                (
                    Output("progress_bar", "style"),
                    {"visibility": "visible"},
                    {"visibility": "hidden"},
                ),
              ],
              cancel=[Input("cancel_button_id", "n_clicks")],
              progress=[Output("progress_bar", "value"), Output("progress_bar", "max")],
              prevent_initial_call=True,
              )
def collect_params(set_progress, n_clicks, dropdown_tickers_value, dropdown_benchmark_value, radio_years_value, radio_rolling_window_value):
    if not n_clicks:
        return {}
    
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=radio_years_value*365)
    end_date_frmt = end_date.strftime("%Y-%m-%d")
    start_date_frmt = start_date.strftime("%Y-%m-%d")

    prices = pd.DataFrame()

    asset_colors = {}
    for i, asset in enumerate(dropdown_tickers_value):
        # asset_price = web.DataReader(asset, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
        asset_price = gbm(10, 1, steps_per_year=252).iloc[:, 0] # gets the fist column of dataframe as series
        asset_price.index = pd.bdate_range(end=datetime.datetime.now(), periods=asset_price.shape[0]) # generates a time index
        
        asset_price.name = asset
        asset_price = asset_price.loc[start_date.strftime("%Y-%m-%d"):]
        prices[asset] = asset_price
        asset_colors[asset] = px.colors.qualitative.Alphabet[i]
        set_progress((str(i + 1), str(len(dropdown_tickers_value))))

    # bench_price = web.DataReader(dropdown_benchmark_value, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
    bench_price = gbm(10, 1, steps_per_year=252).iloc[:, 0] # gets the fist column of dataframe as series
    bench_price.index = pd.bdate_range(end=datetime.datetime.now(), periods=bench_price.shape[0]) # generates a time index
    
    bench_price.name = dropdown_benchmark_value
    bench_price = bench_price.loc[start_date.strftime("%Y-%m-%d"):]
    prices[dropdown_benchmark_value] = bench_price
    asset_colors[dropdown_benchmark_value] = px.colors.qualitative.Alphabet[-1]

    return {
        'dropdown_tickers_value': dropdown_tickers_value,
        'dropdown_benchmark_value': dropdown_benchmark_value,
        'years': radio_years_value,
        'rolling_window_value': radio_rolling_window_value,
        'risk_free_rate': 0.03,
        'asset_colors': asset_colors,
        'prices': prices.to_json(orient='split'),
    }


@app.callback(
    Output('graph_wi', 'figure'),
    Input('memory', 'data'))
def update_wi(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    wi_figures = []

    for asset_name in prices.columns:
        fig_wi_asset = prices[asset_name].prices.returns.wealth_index.plotly()
        fig_wi_asset.update_traces(line_color=data['asset_colors'][asset_name], line_width=1)
        wi_figures.append(fig_wi_asset)

    fig_wi = go.Figure(data=sum((fig.data for fig in wi_figures), ()))
    fig_wi.update_layout(
        title="Performance on 1$",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig_wi


@app.callback(
    Output('graph_dd', 'figure'),
    Input('memory', 'data'))
def update_dd(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    dd_figures = []

    for asset_name in prices.columns:
        fig1 = prices[asset_name].prices.returns.wealth_index.drawdown.plotly()
        fig1.update_traces(line_color=data['asset_colors'][asset_name], line_width=1)
        dd_figures.append(fig1)

    fig_dd = go.Figure(data=sum((fig.data for fig in dd_figures), ()))
    fig_dd.layout.yaxis.tickformat = '.1%'

    fig_dd.update_layout(
        title="Drawdown",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig_dd


@app.callback(
    Output('graph_arets', 'figure'),
    Input('memory', 'data'))
def update_arets(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    ann_rets = pd.DataFrame()
    for asset_name in prices.columns:
        ann_rets = pd.concat([ann_rets, prices[asset_name].prices.returns.wealth_index.annual_returns.data], axis=1)
    ann_rets = ann_rets.dropna(how='all')

    ann_rets_fig = px.bar(ann_rets, barmode="group", color_discrete_map=data['asset_colors'])
    ann_rets_fig.layout.yaxis.tickformat = ',.1%'

    ann_rets_fig.update_layout(
        title="Annual Returns",
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return ann_rets_fig


@app.callback(
    Output('graph_rolling_rets', 'figure'),
    Input('memory', 'data'))
def update_graph_rolling_rets(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')
    rolling_rets_figures = []

    for asset_name in prices.columns:
        fig1_r = pyinvestingsnippets.RollingReturns(prices[asset_name].prices.returns.data, rolling_window=data['rolling_window_value']).plotly()
        fig1_r.update_traces(line_color=data['asset_colors'][asset_name], line_width=1)
        rolling_rets_figures.append(fig1_r)

    fig = go.Figure(data=sum((fig.data for fig in rolling_rets_figures), ()))
    fig.layout.yaxis.tickformat = ',.1%'

    fig.update_layout(
        title="Rolling Returns",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig

@app.callback(
    Output('graph_rolling_vol', 'figure'),
    Input('memory', 'data'))
def update_graph_rolling_vol(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')
    rolling_vol_figures = []

    for asset_name in prices.columns:
        fig1_v = pyinvestingsnippets.RollingVolatility(prices[asset_name].prices.returns.data, rolling_window=data['rolling_window_value'], window=252).plotly()
        fig1_v.update_traces(line_color=data['asset_colors'][asset_name], line_width=1)
        rolling_vol_figures.append(fig1_v)

    fig = go.Figure(data=sum((fig.data for fig in rolling_vol_figures), ()))
    fig.layout.yaxis.tickformat = ',.1%'

    fig.update_layout(
        title="Rolling Volatility",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig


@app.callback(
    Output('graph_risk_reward', 'figure'),
    Input('memory', 'data'))
def update_graph_risk_reward(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    all_values = pd.DataFrame()
    for asset_name in prices.columns:
        ann_vol = prices[asset_name].prices.returns.volatility_annualized(252)
        ann_ret = prices[asset_name].prices.returns.annualized(ppy=252)
        all_values = pd.concat([all_values, pd.DataFrame({'Name': asset_name, 'Risk': ann_vol, 'Return': ann_ret, 'Color': data['asset_colors'][asset_name]}, index=[asset_name])], axis=0)

    fig = px.scatter(all_values, x='Risk', y='Return', hover_data=['Name'], color="Name", color_discrete_map=data['asset_colors'])
    fig.update_traces(marker_size=10)
    fig.layout.yaxis.tickformat = '.1%'
    fig.layout.xaxis.tickformat = '.1%'
    fig.update_layout(
        title="Risk/Reward",
        xaxis_title="Risk",
        yaxis_title="Reward",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig


@app.callback(
    Output('graph_stats', 'figure'),
    Input('memory', 'data'))
def update_graph_stats(data):
    if data is None:
        raise PreventUpdate
    
    prices = pd.read_json(data["prices"], orient='split')

    all_stats = [{'name': "Stat\Symbol", 'vals': ['Total Return', 'Return Annualized', 'CAGR', 'Volatility', 'Max DrawDown', 'Min DrawDown Duration', 'Max DrawDown Duration', 'Beta', 'Tracking Error', 'Sharpe Ratio', 'M2 Ratio', 'Information Ratio', 'SRRI']}]
    for asset_name in prices.columns:
        asset_values = []
        asset_values.append(f"{prices[asset_name].prices.returns.wealth_index.total_return*100:.2f}%")
        asset_values.append(f"{prices[asset_name].prices.returns.annualized(252)*100:.2f}%")
        asset_values.append(f"{prices[asset_name].prices.returns.wealth_index.cagr*100:.2f}%")
        asset_values.append(f"{prices[asset_name].prices.returns.volatility_annualized(252)*100:.2f}%")
        asset_values.append(f"{prices[asset_name].prices.returns.wealth_index.drawdown.max_drawdown*100:.2f}%")
        asset_values.append(f"{prices[asset_name].prices.returns.wealth_index.drawdown.durations.mean().days} days")
        asset_values.append(f"{prices[asset_name].prices.returns.wealth_index.drawdown.durations.max().days} days")
        asset_values.append(f"{pyinvestingsnippets.BetaCovariance(prices.iloc[: , -1].prices.returns.data, prices[asset_name].prices.returns.data).beta:.2f}")
        asset_values.append(f"{tracking_error(prices[asset_name].prices.returns.data, prices.iloc[: , -1].prices.returns.data):.4f}")
        asset_values.append(f"{prices[asset_name].prices.returns.sharpe(data['risk_free_rate'], 252):.2f}")
        asset_values.append(f"{modigliani_ratio(prices[asset_name].prices.returns, prices.iloc[: , -1].prices.returns, data['risk_free_rate'], 252):.2f}")
        asset_values.append(f"{information_ratio(prices[asset_name].prices.returns, prices.iloc[: , -1].prices.returns, 252):.2f}")
        asset_values.append(f"{prices[asset_name].prices.monthly_returns.srri.risk_class}") if data['years'] >=5 else '-' 
        all_stats.append({'name':asset_name, 'vals': asset_values})

    fig = go.Figure(data=[go.Table(
        header=dict(values=[i['name'] for i in all_stats],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[i['vals'] for i in all_stats],
                fill_color='lavender',
                align='left'))
    ])
    fig.update_layout(
        title="Stats",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)