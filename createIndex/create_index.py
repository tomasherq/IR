import pyterrier as pt


pt.init()


def msmarco_generate():
    with open("C:/Users/Computer/IR_Project/collectionandqueries/collection.tsv", "r", encoding='utf-8') as file_read:
        for line in file_read:

            if line:

                docno, passage = line.split("\t")

                yield {'docno': docno.strip(), 'text': passage.strip()}


iter_indexer = pt.IterDictIndexer("C:/Users/Computer/IR_Project/createdIndex/passage_index")
indexref3 = iter_indexer.index(msmarco_generate())

# # list of filenames to index
# files = pt.io.find_files("/home/tomas/Escritorio/IR/project/code/collectionandqueries/collection")
# # build the index
# indexer = pt.TRECCollectionIndexer("./wt2g_index", verbose=True, blocks=False, type=pt.index.IndexingType(2))
# indexref = indexer.index(files)

# # load the index, print the statistics
# index = pt.IndexFactory.of(indexref)
# print(index.getCollectionStatistics().toString())
