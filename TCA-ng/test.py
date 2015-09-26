from example_maps import generate_street, Automaton
import random
import cells
import cars
import rules

if __name__ == "__main__":
    tca = Automaton()
    topo = generate_street(5)
    tca.topology = topo
    print(topo.text_view())
    
    for _ in range(10):
        tca.update()
        print(topo.text_view())