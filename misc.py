def get_substrings(word):
    for start in xrange(len(word)):
        for end in xrange(start, len(word)):
            yield word[start:end]


def print_with_indices(li):
	i = 0
	for l in li:
		print "{} {}".format(i, l)
		i += 1

def load_word_set(filename):
	with open(filename, "r") as f:
		words = f.readlines()
	return {w.strip().lower() for w in words}