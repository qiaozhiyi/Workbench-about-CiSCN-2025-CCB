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
        p = self.data.find(b'[$', pos)
        if p == -1: return []
        p += 2
        p += 1 
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
            # default_left array uses 1 byte per node
            dl_offset = self.data.find(b'[$U#L', dl_pos[i]) + 5
            count = struct.unpack('>Q', self.data[dl_offset:dl_offset+8])[0]
            dl = [self.data[dl_offset+8+j] for j in range(count)]
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
                val = features[idx]
                if np.isnan(val):
                    if tree['dl'][node]:
                        node = tree['lc'][node]
                    else:
                        node = tree['rc'][node]
                elif val < cond:
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
