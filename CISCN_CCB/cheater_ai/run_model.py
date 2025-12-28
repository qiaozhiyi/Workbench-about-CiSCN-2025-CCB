import struct
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class XGBModel:
    def __init__(self, data):
        self.data = data
        self.trees = self._parse_trees()
        self.base_score = 0.16528925

    def _find_all(self, pattern):
        offsets = []
        pos = self.data.find(pattern)
        while pos != -1:
            offsets.append(pos)
            pos = self.data.find(pattern, pos + 1)
        return offsets

    def _extract_array(self, pos, type_marker, item_size, struct_format):
        # Array starts with [$<type_marker>#L<count>
        p = pos + len(b'split_indices') # Actually depends on the key
        # Let's find the start of the array marker [$
        p = self.data.find(b'[$', pos)
        if p == -1: return []
        p += 2
        # Marker is at p
        p += 1 # Skip type marker
        if self.data[p:p+1] != b'#': return []
        p += 1
        if self.data[p:p+1] != b'L': return []
        p += 1
        count = struct.unpack('>Q', self.data[p:p+8])[0]
        p += 8
        res = []
        for _ in range(count):
            val = struct.unpack(struct_format, self.data[p:p+item_size])[0]
            res.append(val)
            p += item_size
        return res

    def _parse_trees(self):
        trees = []
        si_pos = self._find_all(b'split_indices')
        sc_pos = self._find_all(b'split_conditions')
        bw_pos = self._find_all(b'base_weights')
        lc_pos = self._find_all(b'left_children')
        rc_pos = self._find_all(b'right_children')
        dl_pos = self._find_all(b'default_left')
        
        for i in range(len(si_pos)):
            si = self._extract_array(si_pos[i], b'l', 4, '>i')
            sc = self._extract_array(sc_pos[i], b'd', 4, '>f')
            bw = self._extract_array(bw_pos[i], b'd', 4, '>f')
            lc = self._extract_array(lc_pos[i], b'l', 4, '>i')
            rc = self._extract_array(rc_pos[i], b'l', 4, '>i')
            dl = self._extract_array(dl_pos[i], b'U', 1, '>B')
            trees.append({
                'si': si, 'sc': sc, 'bw': bw, 'lc': lc, 'rc': rc, 'dl': dl
            })
        return trees

    def predict_raw(self, features):
        score = 0
        for tree in self.trees:
            node = 0
            while tree['lc'][node] != -1:
                idx = tree['si'][node]
                cond = tree['sc'][node]
                if features[idx] < cond:
                    node = tree['lc'][node]
                else:
                    node = tree['rc'][node]
            score += tree['bw'][node]
        return score + np.log(self.base_score / (1 - self.base_score))

    def predict_proba(self, features):
        return sigmoid(self.predict_raw(features))

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    model_data = f.read()

model = XGBModel(model_data)

# Test on a normal sample
import pandas as pd
df_normal = pd.read_csv('normal_samples.csv')
features = df_normal.iloc[0].values[:-1]
print(f"Normal sample probability: {model.predict_proba(features)}")

# Test on a fraud sample
df_fraud = pd.read_csv('fraud_samples.csv')
features_fraud = df_fraud.iloc[0].values[:-1]
print(f"Fraud sample probability: {model.predict_proba(features_fraud)}")
