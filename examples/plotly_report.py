import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.long_callback import DiskcacheLongCallbackManager
from utils import gbm
from _plotly_dash_board_template import content, configure_sidebar

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
    """It measures a trader's ability to generate excess returns relative to a benchmark."""
    return_difference = returns.annualized(periods) - benchmark_returns.annualized(periods)
    volatility = (returns - benchmark_returns).std() * (periods ** 0.5)
    if volatility == 0:
        return np.nan
    information_ratio = return_difference.mean() / volatility
    return information_ratio

def modigliani_ratio(returns, benchmark_returns, rf, periods=252):
    """The Modigliani ratio (M2) measures the returns of the portfolio,
    adjusted for the risk of the portfolio relative to that of some benchmark."""
    sharpe_ratio = returns.sharpe(rf, periods)
    benchmark_volatility = benchmark_returns.volatility_annualized(periods)
    m2_ratio = (sharpe_ratio * benchmark_volatility) + rf
    return m2_ratio


cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)
app.layout = html.Div([configure_sidebar(ASSET_TICKERS, BENCHMARK_TICKERS), content])

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
        asset_price = gbm(10, 1, steps_per_year=252).iloc[:, 0]  # gets first column
        
        asset_price.name = asset
        asset_price = asset_price.loc[start_date.strftime("%Y-%m-%d"):]
        prices[asset] = asset_price
        asset_colors[asset] = px.colors.qualitative.Alphabet[i]
        set_progress((str(i + 1), str(len(dropdown_tickers_value))))

    # bench_price = web.DataReader(dropdown_benchmark_value, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
    bench_price = gbm(10, 1, steps_per_year=252).iloc[:, 0]  # gets first column
    
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
        try:
            fig_wi_asset = prices[asset_name].returns.cwi.plotly()
        except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
            fig_wi_asset = prices[asset_name].returns.cwi.plotly()
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
        try:
            fig1 = prices[asset_name].returns.cwi.drawdown.plotly()
        except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
            fig1 = prices[asset_name].returns.cwi.drawdown.plotly()
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
        ann_rets = pd.concat([ann_rets, prices[asset_name].annual_returns.data], axis=1)
    ann_rets = ann_rets.dropna(how='all')

    try:
        ann_rets_fig = px.bar(ann_rets, barmode="group", color_discrete_map=data['asset_colors'])
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
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
        rr = pyinvestingsnippets.RollingReturns(prices[asset_name].returns.data, rolling_window=data['rolling_window_value'])
        try:
            fig1_r = rr.plotly()
        except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
            fig1_r = rr.plotly()
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
        rv = pyinvestingsnippets.RollingVolatility(prices[asset_name].returns.data, rolling_window=data['rolling_window_value'], window=252)
        try:
            fig1_v = rv.plotly()
        except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
            fig1_v = rv.plotly()
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
        ann_vol = prices[asset_name].returns.volatility_annualized(252)
        ann_ret = prices[asset_name].returns.annualized(ppy=252)
        all_values = pd.concat([all_values, pd.DataFrame({'Name': asset_name, 'Risk': ann_vol, 'Return': ann_ret, 'Color': data['asset_colors'][asset_name]}, index=[asset_name])], axis=0)

    try:
        fig = px.scatter(all_values, x='Risk', y='Return', hover_data=['Name'], color="Name", color_discrete_map=data['asset_colors'])
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
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

    all_stats = [{'name': "Stat\Symbol", 'vals': ['Total Return', 'CAGR', 'Volatility', 'Max DrawDown', 'Min DrawDown Duration (days)', 'Max DrawDown Duration (days)', 'Beta', 'Tracking Error', 'Sharpe Ratio', 'M2 Ratio', 'Information Ratio', 'SRRI']}]
    for asset_name in prices.columns:
        asset_values = []
        asset_values.append(f"{prices[asset_name].returns.cwi.total_return*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.cwi.annualized(252)*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.volatility_annualized(252)*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.cwi.drawdown.max_drawdown*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.cwi.drawdown.durations.mean.days}")
        asset_values.append(f"{prices[asset_name].returns.cwi.drawdown.durations.max.days}")
        asset_values.append(f"{pyinvestingsnippets.BetaCovariance(prices.iloc[: , -1].returns.data, prices[asset_name].returns.data).beta:.2}")
        asset_values.append(f"{tracking_error(prices[asset_name].returns.data, prices.iloc[: , -1].returns.data):.4f}")
        asset_values.append(f"{prices[asset_name].returns.sharpe(data['risk_free_rate'], 252):.2f}")
        asset_values.append(f"{modigliani_ratio(prices[asset_name].returns, prices.iloc[: , -1].returns, data['risk_free_rate'], 252):.2f}")
        asset_values.append(f"{information_ratio(prices[asset_name].returns, prices.iloc[: , -1].returns, 252):.2f}")
        asset_values.append(f"{prices[asset_name].monthly_returns.srri.risk_class}") if prices[asset_name].monthly_returns.data.shape[0] >=60 else '-' 
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