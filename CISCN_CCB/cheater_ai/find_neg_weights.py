from run_model_v2 import model

for i, tree in enumerate(model.trees):
    min_w = min(tree['bw'])
    if min_w < -1.0:
        print(f"Tree {i} has min weight {min_w}")
