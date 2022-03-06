from sklearn.ensemble import RandomForestRegressor
from common import *
import sys

pipeline = pt.FeaturesBatchRetrieve(INDEX, wmodel="BM25", features=["WMODEL:Tf", "WMODEL:PL2"])
bm25 = pt.BatchRetrieve(INDEX, wmodel="BM25")

rf = RandomForestRegressor(n_estimators=400)
rf_pipe = pipeline >> pt.ltr.apply_learned_model(rf)
rf_pipe.fit(train_topics, qrels)

results = pt.Experiment([bm25, rf_pipe], test_topics, qrels, ['map', "ndcg", "recip_rank"], names=["BM25 Baseline", "LTR"])

print(results)
