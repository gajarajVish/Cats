app = dash.Dash(__name__)

characteristic_columns = [col for col in df.columns if col not in ['name', 'origin','length']]

app.layout = html.Div([
    html.H1("Cat Characteristics Dashboard"),
    
    dcc.Dropdown(
        id = 'breed-dropdown',
        options = [{'label': name, 'value': name} for name in df['name'].unique()],
        value = df['name'].iloc[0]  
    ),
    
    html.Div(id='characteristics'),
    
    html.Div(id='comparison'),
    
    dcc.Checklist(
        id='checklist',
        options=[{'label': name, 'value': name} for name in df['name'].unique()],
        value=[]
    ),
    
    dcc.Graph(id='comparison-chart'), 
    
])

@app.callback(
    Output('characteristics', 'children'),
    Output('comparison', 'children'),
    Input('breed-dropdown', 'value')
)

def update_display(selected_breed):
    breed_data = df[df['name'] == selected_breed]
    
    characteristics = html.Div([
        html.H2(f"Characteristics of {selected_breed}"),
        html.P(f"Origin: {breed_data['origin'].iloc[0]} "),
        html.P(f"Length: {breed_data['length'].iloc[0]}"),
        html.P(f"Minimum Life Expectancy: {breed_data['min_life_expectancy'].iloc[0]} Years"),
        html.P(f"Maximum Life Expectancy: {breed_data['max_life_expectancy'].iloc[0]} Years"),
        html.P(f"Minimum Weight: {breed_data['min_weight'].iloc[0]} lbs"),
        html.P(f"Maximum Weight: {breed_data['max_weight'].iloc[0]} lbs"),
        html.P(f"Family Friendliness: {breed_data['family_friendly'].iloc[0]}, Rated out of 5"),
        html.P(f"Amount of Shedding: {breed_data['shedding'].iloc[0]}, Rated out of 5"),
        html.P(f"General Health: {breed_data['general_health'].iloc[0]}, Rated out of 5"),
        html.P(f"Playfulness: {breed_data['playfulness'].iloc[0]}, Rated out of 5"),
        html.P(f"Children Friendliness: {breed_data['children_friendly'].iloc[0]}, Rated out of 5"),
        html.P(f"Amount of Grooming Required : {breed_data['grooming'].iloc[0]}, Rated out of 5"),
        html.P(f"Intelligence: {breed_data['intelligence'].iloc[0]}, Rated out of 5"),
        html.P(f"Friendliness with other pets: {breed_data['other_pets_friendly'].iloc[0]}, Rated out of 5"),

    ])
    comparison = html.Div([
        html.H2("Compare with Another Breed"),
        dcc.Dropdown(
            id='compare-dropdown',
            options=[{'label': name, 'value': name} for name in df['name'].unique()],
            value=df['name'].iloc[1]  # Default value
        ),
        html.Div(id='comparison-results')
    ])
    
    return characteristics, comparison


@app.callback(
    Output('comparison-chart', 'figure'),
    Input('checklist', 'value')
)
def updateComparison(selected):
    comparison_data = df[df['name'].isin(selected)]
    
    fig = go.Figure()
    for col in characteristic_columns:
        for name in selected:
            breed_data = comparison_data[comparison_data['name'] == name]
            fig.add_trace(go.Bar(
                x=[breed],  
                y=[breed_data[col].values[0]],  
                name=f'{breed} - {col}'
            ))
    
    fig.update_layout(
        title='Comparison of Cat Characteristics',
        xaxis_title='Cat Breeds',
        yaxis_title='Value Counts',
        barmode='group',  
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
