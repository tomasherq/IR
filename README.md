# Instructions

You need to create the indexes folder from the collectionandqueries.tar.gz from <https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019.html>.

Download that file, decompress it and run:

```bash
python tools/scripts/msmarco/convert_collection_to_jsonl.py \
 --collection-path collectionandqueries/collection.tsv \
 --output-folder collections/msmarco-passage/collection_jsonl
```

This will make a folder with the data divided in JSON files (9 of them), now you have to create the indexes:

```bash
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 9 -input collectionandqueries/msmarco-passage \
 -index indexes/lucene-index-msmarco-passage -storePositions -storeDocvectors -storeRaw
```

Once this is done, you can use the probabilistic\_model.py that is in the repo.

To evaluate the results you have to use this for now:

```bash
python tools/scripts/msmarco/msmarco_passage_eval.py  queries/qrels.dev.small.tsv
```
