import re
import networkx as nx
from bokeh.io import show, output_file
from bokeh.plotting import figure, from_networkx
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4

# Example input
data = [
    '[1], PDF:sample PDF', '[2], DOCUMENT:documents', '[3], DOCUMENT:PDF', 
    '[4], DOCUMENT:Prince samples repository', '[5], DOCUMENT:CSS For Publishing web site', 
    '[6], DOCUMENT:Dictionary', '[7], DOCUMENT:Dictionaries', '[8], DOCUMENT:multi-column layout', 
    '[9], DOCUMENT:running headers', '[10], PDF:Satyr', '[11], DOCUMENT:Satyr and Faunus', 
    '[3] IS PART OF [6]', '[12], DOCUMENT:Faunus', '[13], DOCUMENT:Faunus dictionary', 
    '[14], DOCUMENT:Dictionary samples', '[15], DOCUMENT:Old Icelandic dictionary', 
    '[16], PDF:Old Icelandic dictionary sample', '[17], DOCUMENT:HTML invoices', 
    '[3] IS PART OF [8]', '[18], INVOICE:invoice'
]

# Parse entities and relationships
entities = {}
relationships = []

entity_pattern = re.compile(r'\[(\d+)\], (\w+):(.+)')
relationship_pattern = re.compile(r'\[(\d+)\] (IS PART OF) \[(\d+)\]')

for line in data:
    entity_match = entity_pattern.match(line)
    relationship_match = relationship_pattern.match(line)
    
    if entity_match:
        idx, entity_type, entity_name = entity_match.groups()
        entities[idx] = f"{entity_type}: {entity_name}"
        
    elif relationship_match:
        source, relation, target = relationship_match.groups()
        relationships.append((source, target, relation))

# Create the graph
G = nx.DiGraph()

# Add nodes
for idx, entity_name in entities.items():
    G.add_node(idx, label=entity_name)

# Add edges
for source, target, relation in relationships:
    G.add_edge(source, target, label=relation)

# Plotting with Bokeh
plot = Plot(width=800, height=800,
            x_range=Range1d(-2, 2), y_range=Range1d(-2, 2))

# Apply spring layout to position nodes
pos = nx.spring_layout(G)

# Draw with Bokeh
graph_renderer = from_networkx(G, pos, scale=1, center=(0, 0))

# Customize nodes
graph_renderer.node_renderer.glyph = Circle(radius=5, fill_color=Spectral4[0], radius_units="screen")
graph_renderer.node_renderer.selection_glyph = Circle(radius=5, fill_color=Spectral4[2], radius_units="screen")
graph_renderer.node_renderer.hover_glyph = Circle(radius=5, fill_color=Spectral4[1], radius_units="screen")

# Customize edges
graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_width=1)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=2)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=2)

# Add the tools
graph_renderer.selection_policy = NodesAndLinkedEdges()
graph_renderer.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(graph_renderer)

# Adding HoverTool
hover_tool = HoverTool(tooltips=[("Entity", "@label")])
plot.add_tools(hover_tool, TapTool(), BoxSelectTool())

# Output to HTML file
output_file("graph_plot.html")

# Show the plot
show(plot)
