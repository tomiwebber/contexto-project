from flask import Flask, render_template, request, session
from flask_session import Session
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from random_word import RandomWords
r = RandomWords()
sentences = []

# Return a single random word
#word = r.get_random_word()
word = "candy"
sentences.append(word)
model = SentenceTransformer('jinaai/jina-embedding-t-en-v1')
guesses = {}
sorted_guesses = {}

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def hello_world():

    if request.method == "POST":
        guess = request.form.get("guess")
        x=0
        while x!=1:
            user_input = guess
            if user_input == "" or len(user_input) <= 2:
                return render_template("contexto.html", modal_trigger = True, guesses = guesses)
            sentences.append(user_input)
            embeddings = model.encode(sentences)
            val = str(cos_sim(embeddings[0], embeddings[-1]))[6:].strip('\[[^()]*\]')
            val = float(val) * 100
            val = round(val, 2)
            guesses[user_input] = val
            num_guesses = len(guesses)

            sorted_values = sorted(guesses.values()) # Sort the values
            sorted_guesses = {}
            for i in sorted_values:
                for k in guesses.keys():
                    if guesses[k] == i:
                        sorted_guesses[k] = guesses[k]
            
            sorted_guesses = dict(reversed(list(sorted_guesses.items())))

            if user_input == sentences[0]:
                return render_template("winner.html")
                #return("The word is", sentences[0])
                x = 1

            else:
                return render_template("contexto.html", user_input = user_input, val = val, sorted_guesses = sorted_guesses, num_guesses = num_guesses)
        return render_template("contexto.html",  guess=guess)
    else:
        session.clear()
        guesses.clear()
        return render_template("contexto.html")
    