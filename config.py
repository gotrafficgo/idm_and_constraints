import random
import numpy as np

class Config:
    def __init__(self, which_experiment, seed=1):
        
        if which_experiment == 1:
            ### Fig1 = Original IDM (Page 254, Traffic Flow Dynamics (2nd Edition))
            self.which_IDM = "Original"            
            self.with_additional_constraint_1 = False
            self.with_additional_constraint_2 = False
            self.with_additional_constraint_3 = False
            self.with_additional_constraint_4 = False            
            self.with_additional_constraint_5 = False  
        
        elif which_experiment == 2:
            ### Fig2            
            self.which_IDM = "Original"
            self.with_additional_constraint_1 = True
            self.with_additional_constraint_2 = True
            self.with_additional_constraint_3 = True
            self.with_additional_constraint_4 = True             
            self.with_additional_constraint_5 = True  
        
        elif which_experiment == 3:
            ### Fig3
            self.which_IDM = "Original"
            self.with_additional_constraint_1 = True
            self.with_additional_constraint_2 = False
            self.with_additional_constraint_3 = True
            self.with_additional_constraint_4 = True             
            self.with_additional_constraint_5 = True        

        elif which_experiment == 4:
            ### Fig4 = Original IDM Plus (Page 265, Traffic Flow Dynamics (2nd Edition))
            self.which_IDM = "Plus"            
            self.with_additional_constraint_1 = False
            self.with_additional_constraint_2 = False
            self.with_additional_constraint_3 = False
            self.with_additional_constraint_4 = False            
            self.with_additional_constraint_5 = False  


        # === Inflow ===
        self.vehicle_min_interval   = 2      # minimum generation interval t_min (s)
        self.vehicle_extra_interval = 0      # expected value of exponential interval extra_interval (s)

        # === Initialize random seeds ===
        self.seed = seed
        random.seed(self.seed)
        np.random.seed(self.seed)

        # === Road Configuration ===
        self.speed_limit = 30                # speed limit (m/s)
        self.road_length = 2000              # total road length (m)            

        # === Simulation Settings ===
        self.simulation_time_step = 0.1     # simulation time step Δt (s)
        self.time_max = 600                 # total simulation time (s)               

        # === IDM Parameters ===
        self.idm_minimum_spacing = 2         # minimum spacing s0 (m) [recommended: 1.5 ~ 2.5]
        self.idm_safety_time_headway = 1.2   # safety time headway T (s) [recommended: 1.2 ~ 1.5]
        self.idm_acceleration = 2            # maximum acceleration a (m/s^2) [recommended: 1.0 ~ 1.2]
        self.idm_desired_deceleration = 1.2  # comfortable deceleration b (m/s^2) [recommended: 1.2 ~ 1.5]

        self.vehicle_length = 5                # vehicle length L (m)
        self.initial_speed = self.speed_limit  # initial speed (m/s)
        self.initial_acceleration = 0          # initial acceleration (m/s^2)
        self.relative_speed_noise = 0          # STD of speed perception noise (m/s)


