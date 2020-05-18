from get_triples import produceTriples
from OpenKE.openke.config import Trainer, Tester
from OpenKE.openke.module.model import TransE
from OpenKE.openke.module.loss import MarginLoss
from OpenKE.openke.module.strategy import NegativeSampling
from OpenKE.openke.data import TrainDataLoader, TestDataLoader
from item2id import entity_map, relation_map

# test_dataloader = TestDataLoader("./benchmarks/FAKE_NEWS/", "classification")
# print(len(entity_map.keys()))
# print(len(relation_map.keys()))
transe = TransE(
	ent_tot = len(entity_map.keys()),
	rel_tot = len(relation_map.keys()),
	dim = 1024,
	p_norm = 1,
	norm_flag = False,
	margin = 6.0
)
transe.load_checkpoint('OpenKE/checkpoint/transe_fn.ckpt')
# tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = True)
tester = Tester(model = transe, use_gpu = False)

print("Process input sentence")
sentence = "coronavirus cut into revenues"
threshlod = 1.6558074951171875

triples = produceTriples(sentence)
result = None
result_true_count = 0
for triple in triples:
    print(triple)
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
    if result_true_count == len(triples):
        result = "TRUE NEWS"
    else:
        result = "I'M NOT SURE"
print(result)