import pyterrier as pt
import os
import json
from timeit import default_timer as timer
from common import *

# Tune the parameters

# topics = readQueryFile(TOPICS_FILE)

start = timer()
BM25_br = pt.BatchRetrieve(INDEX, wmodel="BM25", controls={"c": 0.6, "bm25.k_1": 0.6, "bm25.k_3": 0.5}, threads=24)
rm3_pipe = BM25_br >> pt.rewrite.RM3(INDEX) >> BM25_br

res = rm3_pipe.transform(topics)


eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"], perquery=True)
write_eval(eval_res, OUTPUT_EVAL)

eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"])
write_eval(eval_res, OUTPUT_EVAL_GENERAL)
print("Run time: ", timer()-start)
pt.io.write_results(res, OUTPUT, format='trec', append=False)
