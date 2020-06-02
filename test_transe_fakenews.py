from OpenKE.openke.config import Trainer, Tester
from OpenKE.openke.module.model import TransE
from OpenKE.openke.module.loss import SigmoidLoss
from OpenKE.openke.module.strategy import NegativeSampling
from OpenKE.openke.data import TrainDataLoader, TestDataLoader
from item2id import entity_map, relation_map
from utils.mongo import Mongo
from random import randrange
import random
import traceback

from utils.mongo import Mongo
db = Mongo().get_client()
threshlod = float(db['training_results'].find_one({'name': 'transe'})['threshold'])
print("Get transe threshold: {}".format(threshlod))
# threshlod = 6.679401874542236
number_of_test_example = 100

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
transe.load_checkpoint('OpenKE/checkpoint/transe_fn.ckpt')
tester = Tester(model = transe, use_gpu = False)

print("Predicting random entity and relation ...")
result_number_1 = 0
news_list = db['covid_news_data'].find({
	"status": 2
})
if news_list:
	count = 0
	try:
		for news in news_list:
			count += 1
			if count > number_of_test_example:
				break
			print("Processing key {}: {}/{}".format(news["_id"], count, number_of_test_example))
			triples = news["tripleSet"]
			triple_index = random.randint(0, len(triples) - 1)
			triples[triple_index][1] = random.choice(list(entity_map.keys()))
			predict_result = predict([triples[triple_index]], tester)
			if predict_result == "FAKE NEWS":
				result_number_1 += 1
	except :
		traceback.print_exc()
		print("Process failed {}".format(count))
else:
	print("DB NOT FOUND")


print("Predicting random news content ...")
result_number_2 = 0
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
				result_number_2 += 1
	except :
		traceback.print_exc()
		print("Process failed {}".format(count))
else:
	print("DB NOT FOUND")

print("Acc of Predicting random entity and relation: {}".format(result_number_1 / number_of_test_example))
print("Acc of Predicting random news content: {}".format(result_number_2 / number_of_test_example))