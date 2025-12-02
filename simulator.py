import random
from config import Config
from vehicle import Vehicle

class Simulator:

    def __init__(self, config: Config):
        self.config = config
        self.vehicles = []

    def run(self):
        number_of_vehicles = 0
        time_generation_last = 0

        dt = self.config.simulation_time_step  # 0.1
        num_steps = int((self.config.time_max - 1) / dt) + 1

        for i in range(num_steps):
            t = 1 + i * dt

            if abs(t % 100) < 1e-6: 
                print(f"step:{i}, time:{int(t)}")     

            # Vehicle Generation
            number_of_vehicles, time_generation_last, self.vehicles = self._generate_vehicles(number_of_vehicles, t, time_generation_last, self.vehicles)
            
            # Car-following
            self._update_all_acceleration(t)
            self._update_all_speed() 
            self._update_all_position()

            # Record state
            self._record_all_state(t)

        print("\nSimulation completed: ", len(self.vehicles), " vehicles generated.")
        print("Inflow Rate = ", int(len(self.vehicles) / (self.config.time_max - 1) * 3600), " veh/h\n" )


    def _check_road(self, current_time):
        for vehicle in self.vehicles:
            vehicle.check_road(current_time)


    def _update_all_acceleration(self, t):
        for vehicle in self.vehicles:
            if self.config.which_IDM == "Plus":
                vehicle.update_acceleration_plus(t)
            elif self.config.which_IDM == "Original":
                vehicle.update_acceleration(t)


    def _update_all_speed(self):
        for vehicle in self.vehicles:
            vehicle.update_speed()


    def _update_all_position(self):
        for vehicle in self.vehicles:
            vehicle.update_position()


    def _record_all_state(self, t):
        for vehicle in self.vehicles:
            vehicle.record_state(t)


    def _generate_vehicles(self, number_of_vehicles, t_current, time_generation_last, vehicles):
        if vehicles:
            v_front = vehicles[-1]
        else:
            v_front = None

        t_min = self.config.vehicle_min_interval
        extra_interval = self.config.vehicle_extra_interval

        # Initialize next generation time
        if not hasattr(self, 'next_generation_time') or self.next_generation_time is None:
            if extra_interval > 0:
                self.next_generation_time = t_current + t_min + random.expovariate(1.0 / extra_interval)
            else:
                self.next_generation_time = t_current + t_min

        last_generation_time = time_generation_last

        # --- Loop to generate vehicles ---
        while self.next_generation_time <= t_current:
            # Create vehicle
            number_of_vehicles += 1
            v = Vehicle(self.config, number_of_vehicles, v_front)

            vehicles.append(v)
            last_generation_time = self.next_generation_time
            v_front = vehicles[-1]

            # Compute next generation time
            if extra_interval > 0:
                interval = t_min + random.expovariate(1.0 / extra_interval)
            else:
                interval = t_min
            self.next_generation_time = last_generation_time + interval

        return number_of_vehicles, last_generation_time, vehicles
    

