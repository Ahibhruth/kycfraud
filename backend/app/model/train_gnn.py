# # train_gnn.py

# import sys
# sys.path.append("D:/kyc_aml_system")

# import torch
# import torch.nn.functional as F
# from torch_geometric.nn import GCNConv
# from torch.nn import Linear
# from torch_geometric.utils import from_networkx
# import networkx as nx

# from model.preprocess import preprocess_dataset


# # ✅ Exported model class ONLY
# class FraudGNN(torch.nn.Module):
#     def __init__(self, input_dim=8, hidden_dim=32, output_dim=16):
#         super().__init__()
#         self.conv1 = GCNConv(input_dim, hidden_dim)
#         self.conv2 = GCNConv(hidden_dim, output_dim)
#         self.fc = Linear(output_dim, 1)

#     def forward(self, data):
#         x, edge_index = data.x, data.edge_index
#         x = F.relu(self.conv1(x, edge_index))
#         x = F.relu(self.conv2(x, edge_index))
#         return torch.sigmoid(self.fc(x))


# # ✅ ✅ ✅ Prevent auto-training when imported by FastAPI
# if __name__ == "__main__":

#     # ✅ 1. Load dataset
#     df, X_scaled = preprocess_dataset("data/raw_data.csv")

#     # ✅ 2. Graph construction
#     G = nx.Graph()
#     for i in range(len(df)):
#         G.add_node(i)

#     for col in ["Address_clean", "Document_Number"]:
#         groups = df.groupby(col)
#         for _, g in groups:
#             idx = list(g.index)
#             for i in range(len(idx) - 1):
#                 G.add_edge(idx[i], idx[i + 1])

#     # ✅ 3. Convert to PyTorch Geometric format
#     data = from_networkx(G)
#     data.x = torch.tensor(X_scaled, dtype=torch.float)
#     data.y = torch.tensor((df["Fraud_Risk_Level"] == "High").astype(int).values)

#     # ✅ 4. Train model
#     model = FraudGNN(input_dim=data.x.shape[1])
#     opt = torch.optim.Adam(model.parameters(), lr=0.005)
#     crit = torch.nn.BCELoss()

#     for epoch in range(60):
#         opt.zero_grad()
#         out = model(data)
#         loss = crit(out.view(-1), data.y.float())
#         loss.backward()
#         opt.step()
#         print(f"Epoch {epoch + 1}/60 Loss: {loss.item():.4f}")

#     # ✅ 5. Save trained model
#     torch.save(model.state_dict(), "model/model.pth")
#     print("✅ Model saved successfully!")



# train_gnn.py

import sys
sys.path.append("D:/kyc_aml_system")

import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch.nn import Linear
from torch_geometric.utils import from_networkx
import networkx as nx
import pandas as pd

from model.preprocess import preprocess_dataset


# ✅ Exportable GNN model
class FraudGNN(torch.nn.Module):
    def __init__(self, input_dim=8, hidden_dim=32, output_dim=16):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)
        self.fc = Linear(output_dim, 1)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        return torch.sigmoid(self.fc(x))


# ✅ Prevent auto-training when imported by FastAPI
if __name__ == "__main__":

    print("✅ Starting GNN Training...")

    # ✅ 1. Load dataset
    df, X_scaled = preprocess_dataset("data/raw_data.csv")

    # ✅ 2. Build Graph (Address / Document similarity)
    G = nx.Graph()
    for i in range(len(df)):
        G.add_node(i)

    for col in ["Address_clean", "Document_Number"]:
        groups = df.groupby(col)
        for _, g in groups:
            idx = list(g.index)
            for i in range(len(idx) - 1):
                G.add_edge(idx[i], idx[i + 1])

    # ✅ 3. Convert to PyTorch Geometric format
    data = from_networkx(G)
    data.x = torch.tensor(X_scaled, dtype=torch.float)
    data.y = torch.tensor((df["Fraud_Risk_Level"] == "High").astype(int).values)

    # ✅ 4. Train the model
    model = FraudGNN(input_dim=data.x.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=0.005)
    crit = torch.nn.BCELoss()

    for epoch in range(60):
        opt.zero_grad()
        out = model(data)
        loss = crit(out.view(-1), data.y.float())
        loss.backward()
        opt.step()
        print(f"Epoch {epoch + 1}/60 Loss: {loss.item():.4f}")

    # ✅ 5. Save trained model
    torch.save(model.state_dict(), "model/model.pth")
    print("✅ Model saved successfully!")

    # ✅ 6. Generate GNN Output CSV for Dashboard
    with torch.no_grad():
        preds = model(data).view(-1).numpy()

    df["GNN_Fraud_Probability"] = preds
    df["GNN_Fraud_Level"] = df["GNN_Fraud_Probability"].apply(
        lambda x: "High" if x > 0.75 else ("Medium" if x > 0.50 else "Low")
    )

    df.to_csv("model/output_of_GNN_part2.csv", index=False)
    print("✅ Saved: model/output_of_GNN_part2.csv")
