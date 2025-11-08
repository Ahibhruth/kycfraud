import streamlit as st
import networkx as nx
import plotly.graph_objects as go

def show_risk_graph(df):
    G = nx.Graph()

    for i in range(len(df)):
        G.add_node(i, prob=df.loc[i, "GNN_Fraud_Probability"])

    for i in range(len(df)):
        for j in range(i+1, len(df)):
            if df.loc[i, "Address_clean"] == df.loc[j, "Address_clean"]:
                G.add_edge(i, j)

    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x = []
    node_y = []
    colors = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        colors.append(G.nodes[node]["prob"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color="gray"),
        hoverinfo="none",
        mode="lines"))

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode="markers",
        marker=dict(
            size=12,
            color=colors,
            colorscale="Reds",
            showscale=True
        ),
        text=[f"Prob: {p:.2f}" for p in colors],
        hoverinfo="text"
    ))

    st.plotly_chart(fig, use_container_width=True)
