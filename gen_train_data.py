from get_triples import produceTriples, write_to_file
from tqdm import tqdm

triples_list = []
sentences = [
    "Many construction and retail companies and banks have lowered their business targets after the coronavirus cuts into revenues and dampened growth prospects.",
    "Businesses lower targets after pandemic mauling",
    "Obama is Dead"
]
for sentence in tqdm(sentences):
    triples = produceTriples(sentence)
    triples_list.extend(triples)

print(triples_list)
write_to_file(triples_list, "OpenKE/benchmarks/FAKE_NEWS/triples.txt")
