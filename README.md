# ScribWord
> 6.835: Intelligent Multimodal User Interfaces - Final Project

### File structure
```bash
├── public                      # Folder with publicly available resources
│   ├── css                     # Folder containing .css files
│   |    ├── style.css              # Stylizes all .html files in the application
│   ├── img                     # Folder containing .gif files
│   |    ├── mic-animate.gif        # .gif for when mic is recording
│   |    ├── mic-slash.gif          # .gif for when mic is not available
│   |    ├── mic.gif                # .gif for when mic is available
│   ├── js                      # Folder containing .js files
│   |    ├── history.js             # .js file for history.html
│   |    ├── index.js               # .js file for index.html
│   |    ├── setupSpeech.js         # .js file for continuous speech recognition used in history.html
├── topic_modelling             # Folder containing topic modeling files
│   |    ├── venv               # Virtual environment for Python3
│   |    ├── compute_input.py   # Interfaces between topic modeling backend and app.js for frontend
│   |    ├── guided_lda.py      # One of the approaches to topic modeling. --Unused
│   |    ├── guidedlda_model.pkl  # Pickled model of guided lda topic model --Unused
│   |    ├── lda.py             # One of the approaches to topic modeling. --Used
│   |    ├── requirements.txt   # Requirements for Python3
│   |    ├── test_we.py         # Tests word embedding implementation
│   |    ├── topic_modelling.py # Uses pretrained models to categorize input text with topics
│   |    ├── vectorize.py       # Converts words to vectors based on training corpus
│   |    ├── vectorize_on_brown.pkl # Pickled model of vectorizer trained on brown corpus
│   |    ├── vectorizer.pkl     # Pickled model of vectorizer
│   |    ├── word_embedding.py  # Attempt at using neural network for topic modeling --Unused
├── .gitignore                  # Lists files or types of files to ignore when committing via git
├── README.md             
├── app.js                      # Holds node.js server
├── data.json                   # .json file to store conversations in memory
├── history.html                # Holds html for Past Conversations tab
├── index.html                  # Holds html for Create Conversations tab
├── package-lock.json           # Automatically generated when npm modifies either the node_modules or package.json
├── package.json                # File containing all dependencies for node.js app
└── vectorize_on_brown.pkl      # Pickled model of vectorization model trained on brown corpus
```

### Instructions to run code

1. Clone the repository.
2. Install [node.js version recommended for most users](https://nodejs.org/en/)
3. Run ```npm install``` to install dependencies. This will create a `node_modules` file at the root.
4. Install [Python 3.6](https://www.python.org/downloads/release/python-365/)
5. Run ```pip3 install -r requirements.txt``` in ```/topic_modelling/``` to install required dependencies for topic modeling.
6. Run ```npm start``` to start Express server.

### Other notes
No need to train ```lda.py``` or ```guided_lda.py```. Simply run either of them using ```python3```.
Test ```lda.py``` by changing ```text``` on line 42 to a string passage of your choice.
Test ```guided_lda.py``` by changing ```text``` on line 66 to a string passage of your choice.
