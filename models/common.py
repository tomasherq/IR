import pyterrier as pt
import os
import matplotlib.pyplot as plt
import json

os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jdk-11.0.8'
INDEX = "C:/Users/murta/Desktop/IR/CoreIR/Group/terrier-project-5.5-bin.tar/terrier-project-5.5/var/index/passage_index"
OUTPUT = f"../runs/run_{len(os.listdir('../runs'))}.txt"
TOPICS_FILE = "../queries/queries.dev.tsv" # <-- BM25
TRAIN_TOPICS_FILE = "C:/Users/murta/Desktop/IR/CoreIR/Group/collectionandqueries/queries.train.tsv" # <-- L2R
TEST_TOPICS_FILE = "C:/Users/murta/Desktop/IR/CoreIR/Group/collectionandqueries/queries.eval.tsv" # <-- L2R
QRELS_FILE = "../queries/qrels.dev.tsv"
OUTPUT_EVAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_per_query.json"
OUTPUT_EVAL_GENERAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_general.json"
pt.init(boot_packages=["com.github.terrierteam:terrier-prf:-SNAPSHOT"])

topics = pt.io.read_topics(TOPICS_FILE, format="singleline")
train_topics = pt.io.read_topics(TRAIN_TOPICS_FILE, format="singleline")
test_topics = pt.io.read_topics(TEST_TOPICS_FILE, format="singleline")
qrels = pt.io.read_qrels(QRELS_FILE)


def write_eval(dictionary, outputFile):
    with open(outputFile, "w", encoding="utf-8") as file_write:
        file_write.write(json.dumps(dictionary, indent=4))
