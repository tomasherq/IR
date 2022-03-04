import pyterrier as pt
import os
import matplotlib.pyplot as plt
import json

INDEX = "createdIndex/passage_index"
OUTPUT = f"runs/run_{len(os.listdir('runs'))}.txt"
TRAIN_TOPICS_FILE = "collectionandqueries/queries.train.tsv"
TEST_TOPICS_FILE = "collectionandqueries/queries.eval.tsv"
QRELS_FILE = "collectionandqueries/qrels.train.tsv"
OUTPUT_EVAL = f"evals/run_{len(os.listdir('runs'))}_eval_per_query.json"
OUTPUT_EVAL_GENERAL = f"evals/run_{len(os.listdir('runs'))}_eval_general.json"
pt.init(boot_packages=["com.github.terrierteam:terrier-prf:-SNAPSHOT"])

train_topics = pt.io.read_topics(TRAIN_TOPICS_FILE, format="singleline")
test_topics = pt.io.read_topics(TEST_TOPICS_FILE, format="singleline")
qrels = pt.io.read_qrels(QRELS_FILE)


def write_eval(dictionary, outputFile):
    with open(outputFile, "w") as file_write:
        file_write.write(json.dumps(dictionary, indent=4))
