import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash import Dash, dash_table
import plotly.express as px
import plotly.graph_objects as go


from datetime import datetime, date

app = dash.Dash(__name__)

df1 = pd.read_csv('csv_1.csv')
df2 = pd.read_csv('family3.csv')
 
#TABLE
# We turn it into datetime object and make two lists out of the collumns (so that we can loop over them)
date_of_death = pd.to_datetime(df1['date_of_death'], errors='coerce')
date_of_birth = pd.to_datetime(df1['date_of_birth'], errors='coerce')

ages=[]
for i in range(len(date_of_death)):
    death_year = date_of_death[i].year #this .year is used for datetime objects
    birth_year = date_of_birth[i].year
    age = death_year-birth_year # but this only gives us the year for those that died after their birthday    
    death_month = date_of_death[i].month
    birth_month = date_of_birth[i].month
    death_day = date_of_death[i].day
    birth_day = date_of_birth[i].day
    if birth_month > death_month:
        age -= 1
    if birth_month == death_month:
        if death_day < birth_day:
            age -= 1
    #this gives us the year if the person died before their birthday
    ages.append(age) 
    
df1['age_when_they_died'] = ages

dftable = df1[['name', 'date_of_birth', 'date_of_death', 'age_when_they_died']]

tdata = dftable.fillna("unknown")

fig1 = go.Figure(data=[go.Table(
    header=dict(values=["Name", "Date of Birth", "Date of Death", "Reached the age of"]),
    cells=dict(values=[tdata.name, tdata.date_of_birth, tdata.date_of_death, tdata.age_when_they_died]))
    ])      

#MAP 
geo_data = pd.read_csv("person_information_geocoded.csv")

birth_place = geo_data.groupby(["place_of_birth",
                                "longitudes birth",
                                "latitudes birth"]).agg({"name": list, "person_ID": list}).reset_index() 

death_place = geo_data.groupby(["place_of_death",
                                "longitudes death",
                                "latitudes death"]).agg({"name": list, "person_ID": list}).reset_index()


birth_place["count"] = [len(names) for names in birth_place["name"]] 
death_place["count"] = [len(names) for names in death_place["name"]]
# Ændre begge de loops

birth_dot_size = (birth_place['count'] * 1.3)
death_dot_size = (death_place['count'] * 1.3)



## NETWORK GRAPH
import pandas as pd
import dash
import dash_cytoscape as cyto
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)
              
relation_data = pd.read_csv("directed_relationships.csv")

relation_data_subset = relation_data[
    relation_data['pID2'].astype(str).isin(geo_data['person_ID'].astype(str))]
    
relation_data_missing = relation_data[
    ~relation_data['pID2'].astype(str).isin(geo_data['person_ID'].astype(str))]

relation_last_nodes = relation_data_missing.drop_duplicates(subset=['pID2'])


nodes = [
    {'data': {'id': str(person_ID), 'label': str(name)},'grabbable': False} 
    for person_ID, name in zip(geo_data['person_ID'],geo_data['name'])
    ] + [
        
    {'data': {'id': str(pID2), 'label': str(general_relation)},'grabbable': False} 
    for pID2, general_relation in zip(relation_last_nodes['pID2'],relation_last_nodes['general_relation'])]

edges = [
        
    {'data': {'source': str(pID1), 'target': str(pID2)}}  
    for pID1, pID2 in zip(relation_data['pID1'],relation_data['pID2'])
    ]


        
base_stylesheet = [
     {
      'selector': 'node',
         'style': {
             'content': 'data(label)',
             'label': 'data(label)',
             'background-color': '#696969',
             'color': 'white',
             'font-size': '4px',
             'text-valign': 'center',
             'text-halign': 'center',
             "text-outline-width": 2,
             "text-outline-color": "#696969",
             'width':  40,
             'height': 40,
             }
        },     
     {
      "selector": "edge",
         "style": {
             'line-color': '#D3D3D3',
             "width": 1},
         },
     {
            "selector": ":selected",
            "style": {
                      "background-color": "#8A00C4",
                      'color': 'black',
                      'line-color': '#39FF14',
               }
            }
    ]

#DASH
        
app.layout = html.Div([
    html.H1("Dutch Sinti & Roma victims in WW2"),
    
    html.Div([
        dcc.Graph(id='victims-table', figure=fig1)
    ]),
    
    # Flex container for network + map
    html.Div([
        # Network (left)
        html.Div([
            cyto.Cytoscape(
                id="network-graph",
                elements=nodes + edges,
                stylesheet=base_stylesheet,
                style={"height": "600px", "width": "100%"},
                layout={'name': 'cose', 'cols': 10, 'fit': True},
            ),
            html.P(id='cytoscape-tapNodeData-output'),
        ], style={"flex": "1"}),
        
        # Map (right)
        html.Div([
            dcc.Graph(id="map", figure=map_figure)
        ], style={"flex": "1"}),
        
    ], style={"display": "flex", "width": "100%"}),
])


@app.callback(
    Output('cytoscape-tapNodeData-output', 'children'),
              Input('network-graph', 'tapNodeData'))
def displayTapNodeData(data):
    df = geo_data
    df = df.loc[df[df['name'] == data['label']]] ## filterdf
    return df.to_html()
    
    map_figure = go.Figure()

    map_figure.add_trace(go.Scattergeo(
            lon = df["longitudes birth"],
            lat = df["latitudes birth"],
            mode = "markers",
            marker = dict(size=birth_dot_size,
                          sizemin=1.5,
                          color="seagreen"),
            text = birth_place["place_of_birth"] + ": " + birth_place["count"].astype(str),
            name = "Number Of<br>Births  "
            )
        )

    map_figure.add_trace(go.Scattergeo(
            lon = df["longitudes death"],
            lat = df["latitudes death"],
            mode = "markers",
            marker = dict(size=death_dot_size,
                          sizemin=1.5,
                          color="darkred"),
            text = death_place["place_of_death"] + ": " + death_place["count"].astype(str),
            name = ('Number Of<br>Deaths'  )
            )
        )

    map_figure.update_geos(
            projection_type = "natural earth",
            fitbounds = "locations",
            landcolor = '#D3D3D3'
        )



    map_figure.update_layout(
            height = 1000,
            width = None,
            showlegend = False
        )
              
        
        
    return map_figure
        



# enter: http://localhost:8080
if __name__ == '__main__':
     app.run_server(debug=True, port=8080)




