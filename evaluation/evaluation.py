"""
This module computes evaluation metrics for MSMARCO dataset on the ranking task.
Command line:
python msmarco_eval_ranking.py <path_reference_file> <path_to_candidate_file>

Creation Date : 06/12/2018
Last Modified : 1/21/2019
Authors : Daniel Campos <dacamp@microsoft.com>, Rutger van Haasteren <ruvanh@microsoft.com>
"""
import sys

from collections import defaultdict
from tools.mrr import compute_mrr
from tools.mp import compute_mp
from tools.map import compute_map, compute_gmap


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
                l = line.strip().split("\t")
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
    """Perform quality checks on the dictionaries

    Args:
    p_qids_to_relevant_passageids (dict): dictionary of query-passage mapping
        Dict as read in with load_reference or load_reference_from_stream
    p_qids_to_ranked_candidate_passages (dict): dictionary of query-passage candidates
    Returns:
        str: If there are duplicate keys we show a message
    """
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


def compute_metrics_from_files(path_reference, path_candidate, perform_checks=True):
    """Compute MRR metric
    Args:    
    p_path_reference_file (str): path to reference file.
        Reference file should contain lines in the following format:
            QUERYID\tPASSAGEID
            Where PASSAGEID is a relevant passage for a query. Note QUERYID can repeat on different lines with different PASSAGEIDs
    p_path_to_candidate_file (str): path to candidate file.
        Candidate file sould contain lines in the following format:
            QUERYID\tPASSAGEID1\tRank
            If a user wishes to use the TREC format please run the script with a -t flag at the end. If this flag is used the expected format is 
            QUERYID\tITER\tDOCNO\tRANK\tSIM\tRUNID 
            Where the values are separated by tabs and ranked in order of relevance 
    Returns:
        dict: dictionary of metrics {'MRR': <MRR Score>}
    """

    qids_relevant = load_reference(path_reference)
    qids_candidate = load_candidate(path_candidate)
    if perform_checks:
        message = quality_checks_qids(qids_candidate)
        if message != '':
            print(message)

    all_scores = compute_mrr(qids_relevant, qids_candidate)
    all_scores = compute_mp(qids_relevant, qids_candidate, all_scores)
    all_scores = compute_map(qids_relevant, qids_candidate, all_scores)
    all_scores = compute_gmap(qids_relevant, qids_candidate, all_scores)
    all_scores['QueriesRanked'] = len(qids_candidate)

    return all_scores


def main():
    """Command line:
    python msmarco_eval_ranking.py <path_reference_file> <path_to_candidate_file>
    """

    if len(sys.argv) == 3:
        path_reference = sys.argv[1]
        path_candidate = sys.argv[2]
        metrics = compute_metrics_from_files(path_reference, path_candidate)
        print('#####################')
        for metric in sorted(metrics):
            print('{}: {}'.format(metric, metrics[metric]))
        print('#####################')

    else:
        print('Usage: msmarco_eval_ranking.py <reference ranking> <candidate ranking>')
        exit()


if __name__ == '__main__':
    main()
