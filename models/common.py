import pyterrier as pt
import os
import matplotlib.pyplot as plt
import json

INDEX = "/home/tomas/Escritorio/IR/project/IR/createIndex/passage_index"
OUTPUT = f"../runs/run_{len(os.listdir('../runs'))}.txt"
TOPICS_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/msmarco-test2019-queries.tsv"
QRELS_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/2019qrels-pass.txt"
OUTPUT_EVAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_per_query.json"
OUTPUT_EVAL_GENERAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_general.json"
pt.init(boot_packages=["com.github.terrierteam:terrier-prf:-SNAPSHOT"])

topics = pt.io.read_topics(TOPICS_FILE, format="singleline")


qrels = pt.io.read_qrels(QRELS_FILE)


def write_eval(dictionary, outputFile):
    with open(outputFile, "w") as file_write:
        file_write.write(json.dumps(dictionary, indent=4))
