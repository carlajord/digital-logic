from dash import Dash, html, Input, Output, callback
import dash_cytoscape as cyto
from src.build_network import Network
import webbrowser
from threading import Timer

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

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(8050))

if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run(debug=False)
