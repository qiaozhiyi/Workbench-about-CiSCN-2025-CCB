from run_model_v2 import model

# For each tree, find the leaf with the most negative weight
triggers = {}

for i, tree in enumerate(model.trees):
    min_w = min(tree['bw'])
    # Find the node index of this leaf
    leaf_idx = tree['bw'].index(min_w)
    
    # Trace back to root
    node = leaf_idx
    path = []
    while node != 0:
        # Find parent
        parent = -1
        is_left = False
        for p_idx, l in enumerate(tree['lc']):
            if l == node:
                parent = p_idx
                is_left = True
                break
        if parent == -1:
            for p_idx, r in enumerate(tree['rc']):
                if r == node:
                    parent = p_idx
                    is_left = False
                    break
        
        feat = tree['si'][parent]
        cond = tree['sc'][parent]
        path.append((feat, cond, is_left))
        node = parent
    
    # print(f"Tree {i} most negative path: {path}")
    for feat, cond, is_left in path:
        key = (feat, cond, is_left)
        triggers[key] = triggers.get(key, 0) + min_w

# Sort triggers by total impact
sorted_triggers = sorted(triggers.items(), key=lambda x: x[1])
for t, impact in sorted_triggers[:20]:
    print(f"Trigger {t}: total impact {impact}")
