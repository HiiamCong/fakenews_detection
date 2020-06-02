from get_triples import write_to_file
from utils.mongo import Mongo
import traceback

db = Mongo().get_client()
news_list = db['covid_news_data'].find({
    "status": 2
})

if news_list:
    count = 0
    total = news_list.count()
    triples_list = []
    try:
        for news in news_list:
            count += 1
            print("Processing key {}: {}/{}".format(news["_id"], count, total))
            triples = news["tripleSet"]
            triples_list.extend(triples)
    except :
        traceback.print_exc()
        print("Process failed {}".format(count))
    
    print("Writing {} triple set ...".format(len(triples_list)))
    write_to_file(triples_list, "OpenKE/benchmarks/FAKE_NEWS/triples.txt")
    print("Write {} triple set done".format(len(triples_list)))
else:
    print("DB NOT FOUND")