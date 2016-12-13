#I'm documenting my progress in case this is incomplete.
#I'm learning how to implement mapreduce here.
import string, example_map_reduce

filenames = ["texta.txt","textb.txt","textc.txt"]
i = {}
for filename in filenames:
  f = open(filename)
  i[filename] = f.read()
  f.close()


def mapper(input_key, input_value):
	return [(word,1) for word in remove_punctuation(input_value.lower()).split()]

def remove_punctuation(s):
	return s.translate(string.maketrans("",""), string.punctuation)

def reducer(intermediate_key, intermediate_value_list):
	return (intermediate_key, sum(intermediate_value_list))

print example_map_reduce.map_reduce(i,mapper,reducer)

