import openke
from openke.config import Trainer, Tester
from openke.module.model import TransE
from openke.module.loss import SigmoidLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader
from utils.mongo import Mongo

# dataloader for training
train_dataloader = TrainDataLoader(
	in_path = "./benchmarks/FAKE_NEWS/", 
	# batch_size = 2000,
    batch_size = 1,
	threads = 8,
	sampling_mode = "cross", 
	bern_flag = 0, 
	filter_flag = 1, 
	# neg_ent = 64,
	# neg_rel = 0
)

# dataloader for test
test_dataloader = TestDataLoader("./benchmarks/FAKE_NEWS/", "link")

# define the model
transe = TransE(
	ent_tot = train_dataloader.get_ent_tot(),
	rel_tot = train_dataloader.get_rel_tot(),
	dim = 1024, 
	p_norm = 1,
	norm_flag = False,
	margin = 6.0)


# define the loss function
model = NegativeSampling(
	model = transe, 
	loss = SigmoidLoss(adv_temperature = 1),
	batch_size = train_dataloader.get_batch_size(), 
	regul_rate = 0.0
)

# train the model
trainer = Trainer(model = model, data_loader = train_dataloader, train_times = 3000, alpha = 2e-5, use_gpu = False, opt_method = "adam")
trainer.run()
transe.save_checkpoint('./checkpoint/transe_fn.ckpt')

# test the model
transe.load_checkpoint('./checkpoint/transe_fn.ckpt')
tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = False)
# tester.run_link_prediction(type_constrain = False)
acc, threshlod = tester.run_triple_classification()

db = Mongo().get_client()
db_col = db["training_results"]

transe_result = db_col.find_one({"name": "transe"})

if transe_result:
	print("update acc and threshold to existed transe result")
	query = { "name": "transe" }
	update_values = { "$set": { "acc": acc, "threshold": threshlod } }
	db_col.update_one(query, update_values)
else:
	print("add new transe result")
	transe_dict = { "name": "transe", "acc": acc, "threshold": threshlod }
	x = db_col.insert_one(transe_dict)
