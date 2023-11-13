
import pickle
def pruebapck():

    ar = [12, 15, "15"]

    with open('data.pickle', 'rb') as f:
        hola = pickle.load(f)

    print(hola)

pruebapck()