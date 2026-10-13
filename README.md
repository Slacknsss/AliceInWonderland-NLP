# 📚 ALICE'S ADVENTURES IN WONDERLAND, book to classification.
 
For this project, we 'joined' Through the Looking-Glass — a startup building a lightweight tool that creates ”book cards”
to help publishers and editors quickly make sense of Wonderland's endless library, without having to read the books entirely..
The challenge is to develop a prototype NLP engine performing operations on books from Project
Gutenberg through dedicated CLI commands.

Epitech Paris, B-AIA-200, team of three: Théo Busiris, Jules Fischer, Simon Slack.

**My part (Simon):** the named entities feature (characters and places, `--entities`) and its diagram in `diagrams/named_entities.md`, a first draft of the clustering that Théo then rewrote, and my bootstrap in `alice_bootstrap/bootstrap_Simon`. Most of the engine, the dashboard and the tests are from Théo and Jules.

## 🧾 License
This code is published for demonstration purposes only.  
© 2026 — **All rights reserved.**

## ⚙️ Tech Stack

(ML models)
- scikit-learn

(NLP analyses)
- NLTK
- spaCy

(csv data analyse)
- pandas

(http requests)
- requests

(creation of a dashboard)
- Streamlit

(unitaires tests)
- unittest (unittest.mock to mock function returns)

## 📬 Contact

Théo Busiris :
- Email pro : [contact@busiristheo.com](contact@busiristheo.com)
- LinkedIn : [linkedin.com/in/theobusiris](https://linkedin.com/in/theobusiris)
- GitHub : [github.com/MXXR-Fivem](https://github.com/MXXR-Fivem)

Jules Fischer : 
- Email pro : [jules.fischer@epitech.eu](jules.fischer@epitech.eu)
- Github : [github.com/Jules-Epitech](https://github.com/Jules-Epitech)

Simon SLACK : 
- Email pro : [simonjspslack@gmail.com](simonjspslack@gmail.com)
- LinkedIn : [linkedin.com/in/simon-slack](https://linkedin.com/in/simon-slack)
- Github : [github.com/Slacknsss](https://github.com/Slacknsss)

## ▶️ Run Locally

### 1. Clone the repo and go into the folder : 
```bash
git clone https://github.com/Slacknsss/AliceInWonderland-NLP.git
cd AliceInWonderland-NLP
```

### 2. Set up venv with python :
```bash
python3.14 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run cli :

Show **book card**
```bash
python3 bookworm.py --card <book_id>
```

Book **summarization**
```bash
python3 bookworm.py --summarize <book_id>
```

Show **books similarity**
```bash
python3 bookworm.py --similar <book_id>
```

Download books \
By author :
```bash
python3 bookworm.py --download --author <author_name>
```

By category :
```bash
python3 bookworm.py --download --category <category_name>
```

Show book lexical diversity
```bash
python3 bookworm.py --lexdiv <book_id>
```

Show book top 10 topics
```bash
python3 bookworm.py --topics <book_id>
```

Show book characters name and locations name
```bash
python3 bookworm.py --entities <book_id>
```

### 4. Run dashboard : 
```bash
streamlit run dashboard.py
```

### 5. Run unit tests :
```bash
bash start_unittests.sh
```