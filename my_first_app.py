import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
from dash.dependencies import Input, Output
import dash_auth

USERNAME_PASSWORD_PAIRS = [['username','password'],['naruto','uzumaki']]

# create Dash application
app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server #deploy to server
# styling tabs
tab_style = {"background": "darkred", 'color': 'white',
             'text-transform': 'uppercase',
             'justify-content': 'center',
             'border': 'grey', 'border-radius': '10px',
             'font-size': '12px', 'font-weight': 600,
             'align-items': 'center', 'padding': '12px'}
tab_selected_style = {"background": "darkblue", 'color': 'white',
                      'text-transform': 'uppercase',
                      'justify-content': 'center',
                      'border-radius': '10px',
                      'font-weight': 600, 'font-size': '12px',
                      'align-items': 'center', 'padding': '12px'}
# import data
# df = pd.read_csv('pw_demo_new_fixed.csv')
df = pd.read_csv('sample_data.csv')
df_agg = df.groupby(['datecl', 'ps_id', 'co_name', 'card_brand', 'payment_method', 'gender']).agg({'cl_id': 'count', 'cl_tracked': 'sum', 'pv': 'sum', 'revenue': 'sum'}).reset_index()
df_agg.columns = ['datecl', 'ps_id', 'country', 'card_brand', 'payment_method', 'gender', 'clicks', 'conversions', 'pv', 'revenue']

# markdown
markdown_text = '''
## This Demo Dashboard serving as a showcase for interactive dashboard built by Plotly-Dash.

The time frame of data in this demo is **2021-01-01** to **2021-04-01**, we assume today/current period is the last date, which is 2021-04-01.

'''
# filters
ps_options = []
for ps in df['ps_id'].unique():
    ps_options.append({'label': str(ps), 'value': ps})

co_options = []
for country in df['co_name'].unique():
    co_options.append({'label': str(country), 'value': country})

# create layout
colors = {'background': '#111111', 'text': '#8aa150', 'paper_color': '#73bd53'}

app.layout = html.Div([
    html.H1('Demo Dashboard', style={'textAlign': 'center', 'color': colors['text']}),
    dcc.Markdown(children=markdown_text),
    html.Div([
        html.Label('Filter by date:'),
        dcc.DatePickerRange(
            id='input-date', month_format='YYYY-MM-DD', show_outside_days=True
            , min_date_allowed=datetime.strptime(df['datecl'].min(), '%Y-%m-%d').date()
            , max_date_allowed=datetime.strptime(df['datecl'].max(), '%Y-%m-%d').date()
            , start_date=datetime.strptime(df['datecl'].min(), '%Y-%m-%d').date()
            , end_date=datetime.strptime(df['datecl'].max(), '%Y-%m-%d').date()
        ),
        html.Br(),
        html.Label('PS ID', style={'paddingTop': '2rem'}),
        dcc.Dropdown(id='ps-picker', options=ps_options, value=df['ps_id'].max(), multi=True),
        html.Label('Country', style={'paddingTop': '2rem'}),
        dcc.Dropdown(id='co-picker', options=co_options, value=df['co_name'][0], multi=True)
    ], style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
              'marginTop': '2rem'}),
    html.Div([
        html.Div([
            html.H3(id='plot1', style={'fontWeight': 'bold', 'fontSize': 30}),
            html.Label('Total clicks', style={'paddingTop': '.3rem'})]),
        html.Div([
            html.H3(id='plot2', style={'fontWeight': 'bold', 'color': '#f73600', 'fontSize': 30}),
            html.Label('Total conversions', style={'paddingTop': '.3rem'})]),
        html.Div([
            html.H3(id='plot3', style={'fontWeight': 'bold', 'color': '#00aeef', 'fontSize': 30}),
            html.Label('Total paid amount', style={'paddingTop': '.3rem'})]),
        html.Div([
            html.H3(id='plot4', style={'fontWeight': 'bold', 'color': '#a0aec0', 'fontSize': 30}),
            html.Label('Total revenue', style={'paddingTop': '.3rem'})])
    ], style={'margin': '1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': 'auto',
              'flex-wrap': 'wrap'}),
    html.Div([
        dcc.Graph(id='plot5')
    ], style={'padding': '.3rem', 'marginTop': '1rem', 'marginLeft': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px',
              'border-radius': '10px', 'backgroundColor': 'white', }),
    html.Div([
        html.Br(),
        dcc.Tabs(id='Chart_Tabs',
                 value='Chart_P',
                 children=[
                     dcc.Tab(label='Piechart',
                             value='Chart_P',
                             style=tab_style,
                             selected_style=tab_selected_style),
                     dcc.Tab(label='Barchart',
                             value='Chart_B',
                             style=tab_style,
                             selected_style=tab_selected_style)
                 ]),
        html.Div([
            html.Br(),
            dcc.Graph(id='plot6'),
            dcc.Graph(id='plot7')
                ])
        ])
], style={'backgroundColor': '#f2f2f2'}
)


@app.callback([Output('plot1', 'children'),
               Output('plot2', 'children'),
               Output('plot3', 'children'),
               Output('plot4', 'children')],
              [Input('ps-picker', 'value'),
               Input('co-picker', 'value'),
               Input('input-date', 'start_date'),
               Input('input-date', 'end_date')])
def callback_1(selected_ps, selected_co, start_date, end_date):
    # start = datetime.strptime(start_date[:10],'%Y-%m-%d').date()
    # end = datetime.strptime(end_date[:10],'%Y-%m-%d').date()
    filtered_df = df_agg[(df_agg['ps_id'].isin(selected_ps)) & (df_agg['country'].isin(selected_co)) & (
                df_agg['datecl'] >= start_date) & (df_agg['datecl'] < end_date)]
    # filtered_df = df_agg[(df_agg.ps_id==selected_ps)&(df_agg.country==selected_co)]
    return sum(filtered_df['clicks']), sum(filtered_df['conversions']), round(sum(filtered_df['pv']), 2), round(
        sum(filtered_df['revenue']), 2)


@app.callback(Output('plot5', 'figure'),
              [Input('ps-picker', 'value'),
               Input('co-picker', 'value'),
               Input('input-date', 'start_date'),
               Input('input-date', 'end_date')])
def callback_2(selected_ps, selected_co, start_date, end_date):
    filtered_df = df_agg[(df_agg['ps_id'].isin(selected_ps)) & (df_agg['country'].isin(selected_co)) & (
                df_agg['datecl'] >= start_date) & (df_agg['datecl'] < end_date)]
    filtered_df = filtered_df.datecl.value_counts().sort_index()
    return {
        'data': [dict(
            x=filtered_df.index,
            y=filtered_df.values,
            type='scatter',
            mode='line',
            marker={'size': 15, 'opacity': 0.5, 'line': {'width': 0.5, 'color': 'white'}},
            line={'color': "#7bc7ff"}
        )],
        'layout': dict(
            title={"text": "Number of clicks in the given date range"},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 20},
            hovermode='closest',
            height=300,
        )}


@app.callback(Output('plot6', 'figure'),
               Output('plot7', 'figure'),
              [Input('ps-picker', 'value'),
               Input('co-picker', 'value'),
               Input('input-date', 'start_date'),
               Input('input-date', 'end_date'),
               Input('Chart_Tabs', 'value')])
def callback_3(selected_ps, selected_co, start_date, end_date, value_T):
    if value_T == 'Chart_P':
        filtered_df = df_agg[(df_agg['ps_id'].isin(selected_ps)) & (df_agg['country'].isin(selected_co)) & (
                    df_agg['datecl'] >= start_date) & (df_agg['datecl'] < end_date)]
        fig1 = px.pie(filtered_df, values='pv', names='card_brand', color='card_brand', hole=.3,
                      color_discrete_sequence=px.colors.sequential.RdBu,
                      title='Paid Amount by Card Brand')
        fig2 = px.pie(filtered_df, values='pv', names='payment_method', color='payment_method', hole=.3,
                      title='Paid Amount by Payment Method')
        color_pie = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig2.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                           marker=dict(colors=color_pie, line=dict(color='#000000', width=2)))
        return fig1, fig2
    elif value_T == 'Chart_B':
        filtered_df = df_agg[(df_agg['ps_id'].isin(selected_ps)) & (df_agg['country'].isin(selected_co)) & (
                    df_agg['datecl'] >= start_date) & (df_agg['datecl'] < end_date)]
        filtered_date = filtered_df.groupby('datecl').agg({'revenue': 'sum'}).reset_index()
        fig3 = px.bar(filtered_date, x='datecl', y='revenue', title='Revenue by date')
        fig3.update_xaxes(title_text='Date')
        fig3.update_yaxes(title_text='Revenue ($)')
        filtered_gender = filtered_df.groupby('gender').agg({'clicks':'sum'}).reset_index()
        fig4 = px.bar(filtered_gender, x='gender', y='clicks', title='Traffic by gender')
        fig4.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                           marker_line_width=1.5, opacity=0.6)
        return fig3, fig4


if __name__ == '__main__':
    app.run_server()
