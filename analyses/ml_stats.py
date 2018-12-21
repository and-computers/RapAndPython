import markovify


def markov_gen(train_text,state_size,output_size):


	if isinstance(train_text,list):
		# use the new line split functinoality built in
		markov_model = markovify.NewlineText(train_text,state_size=state_size)
	elif isinstance(train_text,str):
		markov_model = markovify.Text(train_text,state_size=state_size)

	output = ""
	for i in range(output_size):
		sentence = markov_model.make_sentence()
		output += ("\n"+sentence)

	return output