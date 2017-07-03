import glob


ReduceOutput = glob.glob('../data/MapReduce/*')

DataPath = '../data/'

with open(DataPath + "FullNgrams.txt", 'w') as outfile:
    for fname in ReduceOutput:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)


# class JoinOutput:
#     def reading(self):
#         with open('../MapReduce/reducer-00.txt', 'r') as f:
#             s = f.read()
#             self.whip = ast.literal_eval(s)

