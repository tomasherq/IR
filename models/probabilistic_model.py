import pyterrier as pt
import os
import json
from common import *
from timeit import default_timer as timer

# Use optimal from pyserini github and add extensions! from pyserini
K1 = float(0.82)
B = float(0.68)
K = 1000

if __name__ == '__main__':

    # Tune the parameters
    start = timer()
    # topics = readQueryFile(TOPICS_FILE)
    BM25_br = pt.BatchRetrieve(INDEX, wmodel="BM25", ontrols={"c": 0.6, "bm25.k_1": 0.6, "bm25.k_3": 0.5}, threads=24)
    res = BM25_br.transform(topics)

    eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"], perquery=True)
    write_eval(eval_res, OUTPUT_EVAL)

    print("Runtime: ", timer()-start)
    eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"])
    write_eval(eval_res, OUTPUT_EVAL_GENERAL)

    pt.io.write_results(res, OUTPUT, format='trec', append=False)