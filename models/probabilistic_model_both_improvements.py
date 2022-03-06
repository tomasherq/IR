import pyterrier as pt
import os
import json
from timeit import default_timer as timer
from common import *
from spellchecker import SpellChecker


def check_term_in_corpus(term):
    if term in index.getLexicon():
        index.getLexicon()[term].getFrequency() / index.getCollectionStatistics().getNumberOfTokens()
        return 1
    else:
        return 0


def spell_check(query, corpus):
    sp = SpellChecker()
    edited_query = query.strip().split()

    for word in range(1, len(edited_query)):
        if check_term_in_corpus(edited_query[word]) == 0 and len(sp.unknown([edited_query[word]])) > 0:
            if len(edited_query[word]) > 3:
                corrected = sp.correction(edited_query[word])
                # print(f"Corrected {edited_query[word]} to {corrected}")
                edited_query[word] = corrected

    return str(edited_query[0] + "\t" + " ".join(edited_query[1:]))


TOPICS_FILE = "../queries/msmarco-test2019-queries.tsv"
index = pt.IndexFactory.of("C:/Users/murta/Desktop/IR/CoreIR/Group/terrier-project-5.5-bin.tar/terrier-project-5"
                           ".5/var/index/passage_index/data.properties")

start = timer()
new_topics = []
with open(TOPICS_FILE, "r") as f:
    lines = f.readlines()

    for line in lines:
        new_topics.append(spell_check(line, index))

CORRECTED_TOPICS = "../queries/corrected_topics2.tsv"

with open(CORRECTED_TOPICS, "w") as new_f:

    for line in new_topics:
        new_f.write(line+"\n")

    new_f.close()

spell_checked_topics = pt.io.read_topics(CORRECTED_TOPICS, format="singleline")

BM25_br = pt.BatchRetrieve(INDEX, wmodel="BM25", controls={"c": 0.6, "bm25.k_1": 0.6, "bm25.k_3": 0.5}, threads=24)
rm3_pipe = BM25_br >> pt.rewrite.RM3(INDEX) >> BM25_br

res = rm3_pipe.transform(spell_checked_topics)

eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"], perquery=True)
write_eval(eval_res, OUTPUT_EVAL)

eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"])
write_eval(eval_res, OUTPUT_EVAL_GENERAL)
print("Run time: ", timer() - start)
pt.io.write_results(res, OUTPUT, format='trec', append=False)
