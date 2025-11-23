from config import Config
from simulator import Simulator
from plotting import plot_time_space_diagram

def main():
    
    config = Config()
    sim = Simulator(config)
    sim.run()
    
    plot_time_space_diagram(sim, config)

if __name__ == "__main__":
    main()