import struct
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class XGBPredictor:
    def __init__(self, model_path):
        with open(model_path, 'rb') as f:
            self.data = f.read()
        self.trees = self._parse_trees()
        self.base_score = 0.16528925 # Found in strings

    def _parse_trees(self):
        trees = []
        si_pos = self._find_all(b'split_indices')
        sc_pos = self._find_all(b'split_conditions')
        bw_pos = self._find_all(b'base_weights')
        
        # Assume they are in order
        for i in range(len(si_pos)):
            indices = self._extract_ints(si_pos[i] + 13, b'l')
            conditions = self._extract_floats(sc_pos[i] + 16, b'd')
            weights = self._extract_floats(bw_pos[i] + 12, b'd')
            trees.append({'indices': indices, 'conditions': conditions, 'weights': weights})
        return trees

    def _find_all(self, pattern):
        offsets = []
        pos = self.data.find(pattern)
        while pos != -1:
            offsets.append(pos)
            pos = self.data.find(pattern, pos + 1)
        return offsets

    def _extract_ints(self, p, type_char):
        if self.data[p:p+2] == b'[$' and self.data[p+2:p+3] == type_char:
            p += 4
            if self.data[p:p+1] == b'L':
                p += 1
                count = struct.unpack('>Q', self.data[p:p+8])[0]
                p += 8
                res = []
                for _ in range(count):
                    val = struct.unpack('>i', self.data[p:p+4])[0]
                    res.append(val)
                    p += 4
                return res
        return []

    def _extract_floats(self, p, type_char):
        if self.data[p:p+2] == b'[$' and self.data[p+2:p+3] == type_char:
            p += 4
            if self.data[p:p+1] == b'L':
                p += 1
                count = struct.unpack('>Q', self.data[p:p+8])[0]
                p += 8
                res = []
                for _ in range(count):
                    val = struct.unpack('>f', self.data[p:p+4])[0]
                    res.append(val)
                    p += 4
                return res
        return []

    def predict_tree(self, tree, features):
        node = 0
        while True:
            idx = tree['indices'][node]
            if idx == -1: # Leaf
                # In XGBoost JSON, leaf weights are usually at the same index as the node
                # but they are stored in a separate array sometimes.
                # Actually, if idx == -1, it's a leaf.
                # The weight for the leaf is in base_weights[node].
                return tree['weights'][node]
            
            cond = tree['conditions'][node]
            if features[idx] < cond:
                node = node * 2 + 1 # Typical binary tree indexing? 
                # No, XGBoost uses explicit left/right children.
                # Let's find those!
            else:
                node = node * 2 + 2
            # Wait, XGBoost trees are NOT always complete binary trees.
            # I need left_children and right_children arrays!

    # Let's find left_children and right_children.
