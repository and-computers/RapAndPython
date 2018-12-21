import markovify


def markov_gen(train_text,state_size,output_size):

	markov_model = markovify.Text(train_text,state_size=state_size)

	output = ""
	for i in range(output_size):
		sentence = markov_model.make_sentence()
		output += sentence

	return output