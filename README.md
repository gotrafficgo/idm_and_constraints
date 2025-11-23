# Intelligent Driver Model and its Constrants in Coding

## Abstract
I found the additional constraints large influence the results of IDM-based simulation. I report some of them here. 

**Note 1:** The well-known **Intelligent Driver Model (IDM)** proposed by Martin Treiber et al (https://arxiv.org/abs/cond-mat/0002177). 
**Note 2:** I’m fairly confident that there are no errors in the code. If you found one, please kindly reach out to me (he.zb@hotmail.com), which will be very helpful!



## Scenario
* Straight road (open boundary)
* Entering the road with fixed time interval
* Simulation time step = 0.1 second
* **Bottleneck:** Before the very first vehicle, we set up a virual standstill obstacle (speed = 0), effective before a given time (100 seconds); after the given time, no such limitation, i.e., infinite distance with maximum speed
* ```python
    def _generate_boundary_for_first_vehicle(self, current_time):
        ...   
  ```

## Issues (Possible)

**Experiment 1:** Original IDM: No constraints taking effect. We observe:
* The stop-and-go wave does not continously propagate upstream
* After escaping the stop-and-go wave, the vehicle’s speed cannot return to high speed

<img src="Figure_1.png" alt="Diagram" width="600">




**Experiment 2:** Original IDM: All constraints taking effect. We observe:
* The stop-and-go wave does continously propagate upstream
* The decelerating process is too sharp
  
<img src="Figure_2.png" alt="Diagram" width="600">




**Experiment 3:** Original IDM: Only Constraint 2 not taking effect. We observe:
* Collision occurs

<img src="Figure_3.png" alt="Diagram" width="600">





## Constraints
Constraint 1: in _vehicle.update_acceleration()_
```python
# -------------------------------        
### Additional Constraint 1
if self.with_additional_constraint_1 is True:
    if a < -b_desired:
        a = -b_desired
    if a > a_max:
        a = a_max
# -------------------------------    
```



Constraint 2: in _vehicle.update_speed()_
```python
# -------------------------------        
### Additional Constraint 2
if self.with_additional_constraint_2 is True:            
    if self.vehicle_front is not None:
        s = self.vehicle_front.position - self.position - self.L
        s = max(s, 0.01)  # prevent division by zero
        v_max_allowed = s / delta_t
        v_new = min(v_new, v_max_allowed)
# -------------------------------      
```




Constraint 3: in _vehicle.update_acceleration()_
```python
# -------------------------------        
### Additional Constraint 3
if self.with_additional_constraint_3 is True:
    s = max(s, 0.1) 
# -------------------------------
```



Constraint 4: in  _vehicle.update_speed()_
```python
# -------------------------------        
### Additional Constraint 4
if self.with_additional_constraint_4 is True:
    v_new = max(v_new, 0)
# -------------------------------
```



Constraint 5: in  _vehicle.update_position()_
```python
# -------------------------------   
### Additional Constraint 5
if self.with_additional_constraint_5 is True:
    d = max(d, 0)
# -------------------------------
```
