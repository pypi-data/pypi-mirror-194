import pickle
import os

# VOCABULARY OF THE MODEL
def get_VOCAB_model():
    
    data_path = os.path.join(os.path.dirname(__file__), 'models', 'vocab_model3.pkl')

    with open(data_path, 'rb') as data_file:
        vocab_model = pickle.load(data_file)
    
    return vocab_model

voc = get_VOCAB_model()
print(voc)
