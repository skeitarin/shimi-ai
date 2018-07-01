import os, sys
import numpy as np
path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)
import modules.domain.porker_neural_network as nn

role = [
    "役無し",
    "１ペア",
    "２ペア",
    "３カード",
    "ストレート",
    "フラッシュ",
    "フルハウス",
    "４カード",
    "ストレートフラッシュ",
    "ロイヤルストレートフラッシュ",
]

def predict(param):
    res = nn.predict([param])
    max_val = max(res)
    max_idx = np.argmax(res) 
    print("res:"+str(res))
    return "「{role}」です。その確率は、{rate}％です。".format(role=role[max_idx], rate=str(round(max_val, 1)))