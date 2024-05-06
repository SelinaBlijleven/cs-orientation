"""
tree_graph.py

Show just the tree map
"""
from config import DOMAIN_FILE, MAX_DEPTH
import plotly.graph_objects as go
import pandas as pd


def treemap(df: pd.DataFrame):
    treemap = go.Treemap(
        ids=df.id,
        labels=df.name,
        parents=df.parent_id,
        maxdepth=MAX_DEPTH,
        textinfo="label+text",  # Display both label and text
        text=df.description
    )

    fig = go.Figure()
    fig.add_trace(treemap)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig


if __name__ == '__main__':
    fig = treemap(pd.read_csv(DOMAIN_FILE))
    fig.show()
