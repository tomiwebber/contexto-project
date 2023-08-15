from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from random_word import RandomWords
r = RandomWords()

sentences = []

# Return a single random word
word = r.get_random_word()

sentences.append(word)
#print(word)

model = SentenceTransformer('jinaai/jina-embedding-t-en-v1')

def start_game():
	x=0
	while x!=1:
		user_input = input("Enter the word: ")
		sentences.append(user_input)
		embeddings = model.encode(sentences)
		val = str(cos_sim(embeddings[0], embeddings[-1]))[6:].strip('\[[^()]*\]')
		val = float(val) * 100
		print (val)
		if user_input == sentences[0]:
			print("Congrats! You've guessed the word")
			print("The word is", sentences[0])
			x = 1
