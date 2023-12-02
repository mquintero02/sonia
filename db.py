import pickle
def save_customer(data):
    with open('data/customerData.pkl','wb') as f:
        pickle.dump(data, f)

def read_customer():
    try:
        with open('data/customerData.pkl','rb') as f:
            return pickle.load(f)
    except:
        return []

def save_product(data):
    with open('data/productData.pkl','wb') as f:
        pickle.dump(data, f)

def read_product():
    try:
        with open('data/productData.pkl','rb') as f:
            return pickle.load(f)
    except:
        return []

def save_history(data):
    with open('data/historyData.pkl','wb') as f:
        pickle.dump(data, f)

def read_history():
    try:
        with open('data/historyData.pkl','rb') as f:
            return pickle.load(f)
    except:
        return {}
    
def read_last_index():
    try:
        with open('data/lastIndex.pkl','rb') as f:
            return pickle.load(f)
    except:
        return 0

def save_last_index(index):
    with open('data/lastIndex.pkl','wb') as f:
        pickle.dump(index, f)