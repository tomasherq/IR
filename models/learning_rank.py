from sklearn.ensemble import RandomForestRegressor
from common import *
import sys

pipeline = pt.FeaturesBatchRetrieve(INDEX, wmodel="BM25", features=["WMODEL:Tf", "WMODEL:PL2"])
# bm25 = pt.BatchRetrieve(INDEX, wmodel="BM25", controls={"c": 0.6, "bm25.k_1": 0.6, "bm25.k_3": 0.5})

rf = RandomForestRegressor(n_estimators=100)
rf_pipe = pipeline >> pt.ltr.apply_learned_model(rf)
rf_pipe.fit(topics, qrels)


rtr = pt.Experiment([rf_pipe], topics, qrels, ['map', "ndcg", "recip_rank"],
                    names=["LTR"], perquery=True)

results = rtr.to_json(orient="table")

OUTPUT_EVAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_per_query_ltr.json"
OUTPUT_EVAL_GENERAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_general_ltr.json"


write_eval(results, OUTPUT_EVAL)


rtr = pt.Experiment([rf_pipe], topics, qrels, ['map', "ndcg", "recip_rank"],
                    names=["LTR"], perquery=False)

results = rtr.to_json(orient="table")

write_eval(results, OUTPUT_EVAL_GENERAL)


pt.io.write_results(rtr, OUTPUT, format='trec', append=False)


# print(results)
