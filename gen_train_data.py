from get_triples import produceTriples, write_to_file
from tqdm import tqdm
from utils.mongo import Mongo
from bson import ObjectId
import traceback

triples_list = []
sentences = []

db = Mongo().get_client()
news_list = db['covid_news_data'].find({
    "status": 0
})

if news_list:
    count = 0
    total = news_list.count()
    try:
        for news in news_list:
            count += 1
            print("Processing key {}: {}/{}".format(news["_id"], count, total))
            sentences = []
            if "sentences" in news:
                sentences = news["sentences"]
            else:
                sentences = [news["content"]]
            for sentence in sentences:
                sentence = sentence.replace("COVID-19", "COVID19").replace("Covid-19", "COVID19")
                triples = produceTriples(sentence)
                query = { "_id": news["_id"] }
                update_values = { "$set": { "tripleSet": triples, "status": 2 } }
                db['covid_news_data'].update_one(query, update_values)
                triples_list.extend(triples)
    except :
        traceback.print_exc()
        print("Process failed {}".format(count))

    print("Writing {} triple set ...".format(len(triples_list)))
    write_to_file(triples_list, "OpenKE/benchmarks/FAKE_NEWS/triples.txt")
    print("Write {} triple set done".format(len(triples_list)))
else:
    print("DB NOT FOUND")

