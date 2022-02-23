

def compute_mrr(qids_relevant, qids_candidate, all_scores={}):
    """Compute MRR metric
    Args:    
    p_qids_to_relevant_passageids (dict): dictionary of query-passage mapping
        Dict as read in with load_reference or load_reference_from_stream
    p_qids_to_ranked_candidate_passages (dict): dictionary of query-passage candidates
    Returns:
        dict: dictionary of metrics {'MRR': <MRR Score>}
    """
    MRR = 0
    MAX_MRR = len(list(qids_candidate.values())[0])

    for qid in qids_candidate:
        if qid in qids_relevant:

            target_pids = qids_relevant[qid]
            candidate_pid = qids_candidate[qid]
            for i in range(0, MAX_MRR):
                if candidate_pid[i] in target_pids:
                    MRR += 1/(i + 1)
                    break

    MRR = MRR/len(qids_relevant)
    all_scores[f'MRR @{MAX_MRR}'] = MRR

    return all_scores
