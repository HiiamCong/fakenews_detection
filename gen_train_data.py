from get_triples import produceTriples, write_to_file
from tqdm import tqdm
from utils.mongo import Mongo

triples_list = []
sentences = []

db = Mongo().get_client()
news_list = db['news'].find({
    "status": 0
})

if news_list:
    for news in news_list:
        triples_set = []
        sentences = news["sentences"]
        for sentence in sentences:
            triples = produceTriples(sentence)
            triples_list.extend(triples)
            triples_set.extend(triples)
        query = { "key": news["key"] }
        update_values = { "$set": { "tripleSet": triples_set} }
        db['news'].update_one(query, update_values)

    print("Writing {} triple set".format(len(triples_list)))
    write_to_file(triples_list, "OpenKE/benchmarks/FAKE_NEWS/triples.txt")
else:
    print("DB NOT FOUND")
