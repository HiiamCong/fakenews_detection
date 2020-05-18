entity_map = {}
relation_map = {}

f = open("data/entity2id.txt", "r")
number = (int)(f.readline())
for i in range(number):
    item_arr = f.readline().split("\t")
    entity_map[item_arr[0]] = item_arr[1]
f.close()

f = open("data/relation2id.txt", "r")
number = (int)(f.readline())
for i in range(number):
    item_arr = f.readline().split("\t")
    relation_map[item_arr[0]] = item_arr[1]
f.close()

