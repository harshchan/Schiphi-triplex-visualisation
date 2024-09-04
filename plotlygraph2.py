import plotly.graph_objs as go
import networkx as nx
import ast

# Your data
'''
data = [
    '[1], COMPANY:search engine company', 
    '[2], string:Java source files', 
    '[3], methods:for(;;)', 
    '[4], object:int', 
    '[5], string:string', 
    '[6], boolean:boolean', 
    '[7], object:object array', 
    '[8], COMPANY:US government', 
    '[9], Gov:three-letter agency of the US government', 
    '[10], Gov:government', 
    '[9] WRAPPED_IN [4]', 
    '[9] WRAPPED_IN [5]', 
    '[9] WRAPPED_IN [6]', 
    '[9] WRAPPED_IN [7]', 
    '[11], Gov:Virginia', 
    '[12], IT:government IT'
]
'''


with open('code_story_op.txt', 'r') as file:
    file_content = file.read().strip()

data = ast.literal_eval(file_content)


entities = {}
relationships = []

for item in data:
    if 'WRAPPED_IN' in item:
        parts = item.split()
        source_id = parts[0][1:-1]
        target_id = parts[-1][1:-1]
        relation = ' '.join(parts[1:-1])
        relationships.append((source_id, target_id, relation))
    else:
        entity_id, entity_info = item.split('], ')
        entity_id = entity_id[1:]
        entities[entity_id] = entity_info

# Creating the graph
G = nx.DiGraph()

# Adding nodes
for entity_id, entity_info in entities.items():
    G.add_node(entity_id, label=entity_info)

# Adding edges
for source_id, target_id, relation in relationships:
    G.add_edge(source_id, target_id, label=relation)

# Plotting the graph
pos = nx.spring_layout(G)  # Positions for all nodes

# Create edge traces
edge_trace = []
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    text = edge[2]['label']
    edge_trace.append(
        go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=2, color='#888'),
            hoverinfo='text',
            text=f'{entities[edge[0]]} - {text} -> {entities[edge[1]]}',
            mode='lines'
        )
    )

# Create node traces
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    textposition="bottom center",
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color=[],
        size=10,
        line=dict(width=2)
    )
)

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['text'] += tuple([entities[node]])
    node_trace['marker']['color'] += tuple([len(G[node])])

# Create the figure
# Add relationship labels to the connecting lines
annotations = []
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    text = edge[2]['label']

    annotations.append(
        dict(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2,
            xref='x',
            yref='y',
            text=text,
            showarrow=False,
            font=dict(
                color='black',
                size=10
            ),
            align="center",
            ax=0,
            ay=0,
            bordercolor='black',
            borderwidth=1,
            borderpad=2,
            bgcolor='white',
            opacity=0.8
        )
    )

# Create the figure with annotations
fig = go.Figure(data=edge_trace + [node_trace],
                layout=go.Layout(
                    title='<br>Relationship Graph',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False),
                    height=600,
                    annotations=annotations  # Add the annotations here
                )
                )

fig.show()
