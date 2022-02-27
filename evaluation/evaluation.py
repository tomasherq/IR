
import sys

from collections import defaultdict
from tools.mrr import compute_mrr
from tools.mp import compute_mp
from tools.map import compute_map, compute_gmap
from tools.recall import compute_recall
from tools.nDCG import compute_ndcg

PATH_REFERENCE = "/home/tomas/Escritorio/IR/project/IR/queries/2019qrels-pass.txt"
PATH_RUN = "/home/tomas/Escritorio/IR/project/IR/runs/run_prob_passage_5_train.txt"


def load_file(path_to_file, candidate):
    '''Loads the info of the run/reference file

    Args:
        path_to_file (string): 
        candidate (bool): True if the file is a run file.

    Raises:
        IOError: Bad input.

    Returns:
        dict: Contains the important info about the file.
    '''

    information_passages = defaultdict(list)
    if candidate:
        information_passages = defaultdict(lambda: defaultdict(int))

    with open(path_to_file, 'r') as file:
        for line in file:
            try:
                charSplit = "\t"
                if "\t" not in line:
                    charSplit = " "
                l = line.strip().split(charSplit)
                qid = int(l[0])

                if candidate:
                    pid = int(l[1])
                    rank = int(l[2])
                    information_passages[qid][rank-1] = pid
                else:
                    information_passages[qid].append(int(l[2]))

            except:
                raise IOError('\"%s\" is not valid format' % l)
    return information_passages


def load_reference(path):
    return load_file(path, False)


def load_candidate(path):
    return load_file(path, True)


def quality_checks_qids(qids_candidate):

    message = ''

    # Check that we do not have multiple passages per query
    for qid, values in qids_candidate.items():

        values_dict = list(values.values())
        unique = list(set(values_dict))

        values_dict.sort()
        unique.sort()

        if unique != values_dict:
            message = "There are duplicate keys."

    return message


def compute_metrics_from_files(PATH_REFERENCE, PATH_RUN, perform_checks=True):

    qids_relevant = load_reference(PATH_REFERENCE)
    qids_candidate = load_candidate(PATH_RUN)
    if perform_checks:
        message = quality_checks_qids(qids_candidate)
        if message != '':
            print(message)

    all_scores = compute_mrr(qids_relevant, qids_candidate)
    # all_scores = compute_mp(qids_relevant, qids_candidate, all_scores)
    # all_scores = compute_map(qids_relevant, qids_candidate, all_scores)
    # all_scores = compute_gmap(qids_relevant, qids_candidate, all_scores)
    # all_scores = compute_recall(qids_relevant, qids_candidate, all_scores)
    all_scores = compute_ndcg(qids_candidate, all_scores)
    all_scores['QueriesRanked'] = len(qids_candidate)

    return all_scores


def main():

    metrics = compute_metrics_from_files(PATH_REFERENCE, PATH_RUN)
    print('#####################')
    for metric in sorted(metrics):
        print('{}: {}'.format(metric, metrics[metric]))
    print('#####################')


if __name__ == '__main__':
    main()
