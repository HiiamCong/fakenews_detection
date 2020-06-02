import openke
from openke.config import Trainer, Tester
from openke.module.model import TransE
from openke.module.loss import SigmoidLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader
from item2id import entity_map, relation_map
from utils.mongo import Mongo
from random import randrange
import random

def predict(triples, tester):
	result = None
	result_true_count = 0
	for triple in triples:
		if triple[0] in entity_map and triple[1] in entity_map and triple[2] in relation_map:
			result_code = tester.triple_classification(
				int(entity_map[triple[0]]), 
				int(entity_map[triple[1]]), 
				int(relation_map[triple[2]]), 
				threshlod
			)
			if result_code == 1:
				result = "FAKE NEWS"
				break
			else:
				result_true_count += 1
	if result is None:
		if result_true_count >= len(triples) / 2:
			result = "TRUE NEWS"
		else:
			result = "I'M NOT SURE"
	return result

transe = TransE(
	ent_tot = len(entity_map.keys()),
	rel_tot = len(relation_map.keys()),
	dim = 1024,
	p_norm = 1,
	norm_flag = False,
	margin = 6.0
)
transe.load_checkpoint('./checkpoint/transe_fn.ckpt')
tester = Tester(model = transe, use_gpu = False)

number_of_test_example = 100
db = Mongo().get_client()

print("Predicting random entity and relation ...")
result_number = 0
news_list = db['covid_news_data'].find({
    "status": 2
})
if news_list:
	try:
		for news in news_list:
			count += 1
			if count > number_of_test_example:
				break
			print("Processing key {}: {}/{}".format(news["_id"], count, number_of_test_example))
			triples = news["tripleSet"]
			triple_index = randrange(len(triples))
			triples[triple_index][1] = random.choice(entity_map.keys())
			predict_result = predict([triples[triple_index]], tester)
			if predict_result == "FAKE NEWS":
				result_number += 1
	except :
		traceback.print_exc()
		print("Process failed {}".format(count))
	print("Acc: {}".format(result_number / number_of_test_example))
else:
    print("DB NOT FOUND")


print("Predicting random news content ...")
result_number = 0
news_list = db['covid_news_data'].find({
    "status": 2
})
if news_list:
    count = 0
    triples_list = []
    try:
        for news in news_list:
            count += 1
			if count > number_of_test_example:
				break
            print("Processing key {}: {}/{}".format(news["_id"], count, number_of_test_example))
            triples = news["tripleSet"]
            predict_result = predict(triples, tester)
			if predict_result == "TRUE NEWS":
				result_number += 1
    except :
        traceback.print_exc()
        print("Process failed {}".format(count))
    print("Acc: {}".format(result_number / number_of_test_example))
else:
    print("DB NOT FOUND")

# # dataloader for training
# train_dataloader = TrainDataLoader(
# 	in_path = "./benchmarks/FAKE_NEWS/", 
# 	# batch_size = 2000,
#     batch_size = 1,
# 	threads = 8,
# 	sampling_mode = "cross", 
# 	bern_flag = 0, 
# 	filter_flag = 1, 
# 	# neg_ent = 64,
# 	# neg_rel = 0
# )

# # dataloader for test
# test_dataloader = TestDataLoader("./benchmarks/FAKE_NEWS/", "link")

# # define the model
# transe = TransE(
# 	ent_tot = train_dataloader.get_ent_tot(),
# 	rel_tot = train_dataloader.get_rel_tot(),
# 	dim = 1024, 
# 	p_norm = 1,
# 	norm_flag = False,
# 	margin = 6.0)

# # test the model
# transe.load_checkpoint('./checkpoint/transe_fn.ckpt')
# tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = False)
# acc, threshlod = tester.run_triple_classification()