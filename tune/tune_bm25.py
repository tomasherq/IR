from common import *


c_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
k1_values = [0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 2]
k2_values = [0.5, 2, 4, 6, 8, 10, 12, 14, 20]


BM25 = pt.BatchRetrieve(INDEX, wmodel="BM25", controls={"c": 0.75, "bm25.k_1": 0.75, "bm25.k_3": 0.75})
rtr = pt.GridScan(BM25, {BM25: {"c": c_values,
                                "bm25.k_1": k1_values,
                                "bm25.k_3": k2_values
                                }},
                  topics,
                  qrels,
                  ['map', "ndcg", "recip_rank"])

# Best setting is ['BR(BM25) c=0.6', 'BR(BM25) bm25.k_1=0.6', 'BR(BM25) bm25.k_3=0.5']

result = rtr.to_json(orient="table")

parsed = json.loads(result)


with open("tune_results.json", "w") as file_w:

    file_w.write(json.dumps(parsed, indent=4))
