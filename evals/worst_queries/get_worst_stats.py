import json
import pyterrier as pt

QUERIES_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/msmarco-test2019-queries.tsv"
PASSAGES_FILE = "/home/tomas/Escritorio/IR/project/code/collectionandqueries/collection/collection.tsv"
INDEX = "/home/tomas/Escritorio/IR/project/IR/createIndex/passage_index"
ALL_PASSAGES = "all_passages.json"


def read_all_document(filename):

    queries = []

    with open(filename, "r") as file_read:

        for line in file_read:
            queries.append(line.split("\t")[1].strip())

    return queries


def read_json(filename):

    with open(filename, "r") as file_read:
        return json.load(file_read)


def get_avg_length(queries):
    avg_len = 0
    for query in queries:
        avg_len += len(query)/len(queries)

    return round(avg_len, 2)


def get_avg_stop(queries):
    stop_words = read_json("stop_words_english.json")
    counter_stop = 0
    counter_tot = 0

    for query in queries:
        words = query[1].split(" ")
        for word in words:
            if word in stop_words:
                counter_stop += 1
            counter_tot += 1

    return round(float(counter_stop/counter_tot), 2)


def get_stats(all, worst):
    avg_len = get_avg_length(all)
    avg_len_bad = get_avg_length(worst)

    avg_stop = get_avg_stop(all)
    avg_stop_bad = get_avg_stop(worst)

    print("Average length: ")

    print(f"All: {avg_len}")
    print(f"Worst: {avg_len_bad}")

    print("\n Average stop-words: ")
    print(f"All : {avg_stop}")
    print(f"Worst : {avg_stop_bad}")


def get_term_frequency(worst_queries, worst_passages):

    index = 0
    for query_info in worst_queries:
        times_appear = 0
        word_least = ""

        queryId = query_info[0]
        query = query_info[1]

        passage = worst_passages[index]
        for term in query.split(" "):

            if term not in passage:
                times_appear = 0
                word_least = term
                break
            number_apperances = len(passage.split(term))

            if number_apperances < times_appear or times_appear == 0:
                word_least = term
                times_appear = number_apperances
        index += 1
        print(
            f"For the query {queryId} the word that appears the least is {word_least} and it appears {times_appear} times")


# NB: postings will be null if the document is empty

worst_queries_read = read_json("worst_queries.json")
worst_queries = list()

for query_info in worst_queries_read:
    worst_queries.append(query_info[1])


get_stats(read_all_document(QUERIES_FILE), worst_queries)

worst_passages_read = read_json("worst_passages.json")
worst_passages = list()
for passage_info in worst_passages_read:
    worst_passages.append(passage_info[1])


get_stats(read_json(ALL_PASSAGES), worst_passages)

get_term_frequency(worst_queries_read, worst_passages_read)

get_term_frequency(read_json(ALL_PASSAGES), read_all_document(QUERIES_FILE))

# Documents


# See the documents that they are linked to the queries!!!
# Then come with an hypothesis
