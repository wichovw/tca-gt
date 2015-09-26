from example_maps import simple_street, Automaton
import random
import cells
import cars
import rules

if __name__ == "__main__":
    tca = Automaton()
    topo = simple_street()
    tca.topology = topo
    print(topo.text_view())
    
    for _ in range(10):
        tca.update()
        print(topo.text_view())