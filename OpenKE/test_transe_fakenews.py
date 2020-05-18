import openke
from openke.config import Trainer, Tester
from openke.module.model import TransE
from openke.module.loss import SigmoidLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader

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

# test the model
transe.load_checkpoint('./checkpoint/transe_fn.ckpt')
tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = False)
acc, threshlod = tester.run_triple_classification()