import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests as re
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','style.css',
                        'https://fonts.googleapis.com/css2?family=Ranchers&display=swap']

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

url = "https://api.covid19api.com/summary"
con = re.get(url)
summary = con.json()

Glo = pd.DataFrame(summary["Global"],summary["Global"].keys())

df = pd.DataFrame(summary["Countries"])
df.drop(["Premium","Date","CountryCode","Slug"],axis=1,inplace=True)

df = df[df.Country != "Macao, SAR China"]
#Top 10 Countries

top10 = df.nlargest(10,["TotalConfirmed"])

fig = px.bar(df, y="TotalConfirmed", color="Country")
fig.update_layout(
plot_bgcolor = "Black",
paper_bgcolor = "Black",
title={
        'text': "Overview",
        'y':0.9,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top',
        'font':{"size":30}},
yaxis_title = "Total Confirmed Cases",
xaxis_title = "Countries",
font_color = "White"
)

fig2 = px.pie(top10,values="TotalConfirmed",names="Country")
fig2.update_layout(
plot_bgcolor = "Black",
paper_bgcolor = "Black",
title={'text':"Confirmed Cases"}
)

app.layout = html.Div(style={"text-align":"Center",},children=[html.H1(children="Corona Visualization Dashboard"),

html.Div(style={"align":"Center","color":"Black"},children=[

html.Div(style={"height":"200px","width":"33.33%","background-color":"#FC4F28","padding":"1%","display":"inline-block"},
children=[html.Div(style={"font-size":"30px","text-align":"Center","font-family":"Ranchers"},
children=["Total Active",html.Br(),html.Br(),Glo["TotalConfirmed"][0]])]),

html.Div(style={"height":"200px","width":"33.33%","background-color":"#5AE680","padding":"1%","display":"inline-block"},
children=[html.Div(style={"font-size":"30px","text-align":"Center"},
children=["Total Recovered",html.Br(),html.Br(),Glo["TotalRecovered"][0]])]),

html.Div(style={"height":"200px","width":"33.33%","background-color":"#FE8166","padding":"1%","display":"inline-block"},
children=[html.Div(style={"font-size":"30px","text-align":"Center"},
children=["Total Deaths",html.Br(),html.Br(),Glo["TotalDeaths"][0]])]),
]),

dcc.Graph(id="example",figure=fig),

html.Div(children=[html.H3("Most Affected Countries"),
html.Span(dcc.Graph(figure=fig2,style={"height":"400px","width":"33.33%","display":"inline-block"})),
html.Span(dcc.Graph(figure=fig2,style={"height":"400px","width":"33.33%","display":"inline-block"})),
html.Span(dcc.Graph(figure=fig2,style={"height":"400px","width":"33.33%","display":"inline-block"}))
])

])

if __name__ == '__main__':
    app.run_server(debug=True)
