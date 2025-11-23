import random
import numpy as np

class Vehicle:

    def __init__(self, config, id, vehicle_front=None):

        self.with_additional_constraint_1 = config.with_additional_constraint_1
        self.with_additional_constraint_2 = config.with_additional_constraint_2
        self.with_additional_constraint_3 = config.with_additional_constraint_3
        self.with_additional_constraint_4 = config.with_additional_constraint_4
        self.with_additional_constraint_5 = config.with_additional_constraint_5

        self.id = id        
        self.position = 0
        self.vehicle_front = vehicle_front
        self.road_length = config.road_length
        self.speed_limit = config.speed_limit
        self.speed = config.initial_speed
        
        self.history = []

        # IDM Parameters
        self.v0         = self.speed
        self.s0         = config.idm_minimum_spacing
        self.T          = config.idm_safety_time_headway
        self.a_max      = config.idm_acceleration
        self.b_desired  = config.idm_desired_deceleration
        self.L          = config.vehicle_length
        self.delta_t    = config.simulation_time_step
        self.a          = config.initial_acceleration
        self.d          = 0 # moving distance in current step

        # noise in driving
        self.relative_speed_noise = config.relative_speed_noise


    ##### Update-1
    def update_acceleration(self, current_time):
        ### Initalization
        if self.vehicle_front is None:
            v_front_speed, v_front_position = self._generate_boundary_for_first_vehicle(current_time)
        else:
            v_front_speed = self.vehicle_front.speed
            v_front_position = self.vehicle_front.position

        v         = self.speed
        v_delta   = v - v_front_speed
        v_delta_perceived   = self._perceptive_relative_speed(v_delta)
        s         = v_front_position - self.position - self.L                
        s0        = self.s0
        a_max     = self.a_max
        b_desired = self.b_desired

        # -------------------------------        
        ### Additional Constraint 3
        if self.with_additional_constraint_3 is True:
            s = max(s, 0.1) 
        # -------------------------------

        ### s_star
        term1 = self.T * v
        term2 = v * v_delta_perceived / (2 * (a_max * b_desired) ** 0.5)
        s_star = s0 + max(0, term1 + term2)

        ### acceleration update
        term1 = (v/self.v0) ** 4 # positive number
        term2 = (s_star/s) ** 2  # positive number   
        a = a_max * (1 - term1 - term2)    

        # -------------------------------        
        ### Additional Constraint 1
        if self.with_additional_constraint_1 is True:
            if a < -b_desired:
                a = -b_desired
            if a > a_max:
                a = a_max
        # -------------------------------        

        ###
        self.a = a
        


    def update_speed(self):
        # Has left the road
        if self.position >= self.road_length:
            v_new = 30  

        else:
            a = self.a
            delta_t = self.delta_t
            v = self.speed

            # Original IDM update
            v_new = v + a * delta_t

            # -------------------------------        
            ### Additional Constraint 2
            if self.with_additional_constraint_2 is True:            
                if self.vehicle_front is not None:
                    s = self.vehicle_front.position - self.position - self.L
                    s = max(s, 0.01)  # prevent division by zero
                    v_max_allowed = s / delta_t
                    v_new = min(v_new, v_max_allowed)
            # -------------------------------      

            # -------------------------------        
            ### Additional Constraint 4
            if self.with_additional_constraint_4 is True:
                v_new = max(v_new, 0)
            # -------------------------------

        self.speed = v_new  


    
    ##### Update-3
    def update_position(self):
        ### Initalization
        a = self.a
        v = self.speed
        delta_t = self.delta_t
        
        ### position update
        d = v * delta_t + 0.5 * a * delta_t ** 2

        # -------------------------------   
        ### Additional Constraint 5
        if self.with_additional_constraint_5 is True:
            d = max(d, 0)
        # -------------------------------

        self.d = d
        
        self.position = self.position + self.d


    
    def record_state(self, t):
        self.history.append({
            "t": t,
            "position": self.position,
            "speed": self.speed,
            "acceleration": self.a,
            "moving_distance": self.d
        })



    def _perceptive_relative_speed(self, v_delta):
        noise = np.random.normal(0, self.relative_speed_noise)
        return v_delta + noise




    def _generate_boundary_for_first_vehicle(self, current_time):
        if current_time < 100:
            boundary_speed  = 0 
            boundary_position = self.road_length - 500
        else:
            boundary_speed  = self.speed_limit
            boundary_position = self.position + 1e6  # A large distance ahead                  
        
        return boundary_speed, boundary_position