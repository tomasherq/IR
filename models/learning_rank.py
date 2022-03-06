from sklearn.ensemble import RandomForestRegressor
from common import *
from timeit import default_timer as timer
import sys

start = timer()
pipeline = pt.FeaturesBatchRetrieve(INDEX, wmodel="BM25", features=["WMODEL:PL2"])
bm25 = pt.BatchRetrieve(INDEX, wmodel="BM25")

rf = RandomForestRegressor(n_estimators=100)
rf_pipe = pipeline >> pt.ltr.apply_learned_model(rf)
print("About to fit:")
rf_pipe.fit(train_topics, test_topics)
print("fitted the models")

results = pt.Experiment([bm25, rf_pipe], topics, qrels, ['map', "ndcg", "recip_rank"], names=["BM25 Baseline", "LTR"])

print(timer()-start)
print(results)
