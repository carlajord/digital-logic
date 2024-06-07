from dash import Dash, html, Input, Output, callback
import dash_cytoscape as cyto
from build_network import Network

nw = Network()

app = Dash(__name__)

custom_stylesheet = nw.stylesheet
elements = nw.network

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '90vh'},
        elements=elements,
        stylesheet=custom_stylesheet
    )
])

@app.callback(
    Output('cytoscape', 'elements'),
    Input('cytoscape', 'tapNode')
)
def generate_elements(node):

    if not node:
        return nw.network
    
    elements = nw.update(node)
    return elements


if __name__ == '__main__':
    app.run(debug=True)
