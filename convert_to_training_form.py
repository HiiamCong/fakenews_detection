f = open("OpenKE/benchmarks/FAKE_NEWS/triples.txt", "r")
list_triples = f.readlines()
f.close()
list_triples = [item.replace("\n", "") for item in list_triples]

entity_index = -1
entity_map = {}
relation_index = -1
relation_map = {}

entity2id = []
relation2id = []
train2id = []

for triple in list_triples:
    triple_arr = triple.split("\t")
    if triple_arr[0] not in entity_map:
        entity_index += 1
        entity_map[triple_arr[0]] = entity_index
        entity2id.append("{}\t{}".format(triple_arr[0], entity_index))
    if triple_arr[1] not in entity_map:
        entity_index += 1
        entity_map[triple_arr[1]] = entity_index
        entity2id.append("{}\t{}".format(triple_arr[1], entity_index))
    if triple_arr[2] not in relation_map:
        relation_index += 1
        relation_map[triple_arr[2]] = relation_index
        relation2id.append("{}\t{}".format(triple_arr[2], relation_index))
    train2id.append("{}\t{}\t{}".format(
        entity_map[triple_arr[0]], entity_map[triple_arr[1]], relation_map[triple_arr[2]]
    ))
f = open("OpenKE/benchmarks/FAKE_NEWS/entity2id.txt", "w")
f.write("{}\n".format(len(entity2id)))
for entity in entity2id:
    f.write(entity + "\n")
f.close()

f = open("OpenKE/benchmarks/FAKE_NEWS/relation2id.txt", "w")
f.write("{}\n".format(len(relation2id)))
for relation in relation2id:
    f.write(relation + "\n")
f.close()

f = open("OpenKE/benchmarks/FAKE_NEWS/train2id.txt", "w")
f.write("{}\n".format(len(train2id)))
for train in train2id:
    f.write(train + "\n")
f.close()

f = open("OpenKE/benchmarks/FAKE_NEWS/test2id.txt", "w")
f.write("{}\n".format(len(train2id)))
for train in train2id:
    f.write(train + "\n")
f.close()

f = open("OpenKE/benchmarks/FAKE_NEWS/valid2id.txt", "w")
f.write("{}\n".format(len(train2id)))
for train in train2id:
    f.write(train + "\n")
f.close()

print("Convert done")