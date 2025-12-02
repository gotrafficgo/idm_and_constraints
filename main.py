from config import Config
from simulator import Simulator
from plotting import plot_time_space_diagram
from plotting import plot_speed_time_series

def main():
    
    # which_experiment = 1 
    # which_experiment = 2 
    # which_experiment = 3 
    which_experiment = 4

    config = Config(which_experiment)
    sim = Simulator(config)
    sim.run()
    
    plot_time_space_diagram(sim, config)
    plot_speed_time_series(sim)

if __name__ == "__main__":
    main()