import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection


def plot_time_space_diagram(sim, config):
    fig, ax = plt.subplots(figsize=(9, 6))

    cmap = plt.get_cmap('jet_r')
    norm = plt.Normalize(vmin=0, vmax=getattr(config, 'speed_limit', None) or 1)

    any_segments = False
    for vehicle in sim.vehicles:
        history = getattr(vehicle, 'history', None)
        if not history or len(history) < 2:
            continue

        times = np.array([record['t'] for record in history], dtype=float)
        positions = np.array([record['position'] for record in history], dtype=float)
        speeds = np.array([record['speed'] for record in history], dtype=float)

        points = np.vstack([times, positions]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        seg_speeds = 0.5 * (speeds[:-1] + speeds[1:])

        lc = LineCollection(segments, cmap=cmap, norm=norm, linewidths=1.5)
        lc.set_array(seg_speeds)
        ax.add_collection(lc)
        any_segments = True

    # Colorbar
    if any_segments:
        mappable = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        mappable.set_array([])
        cbar = fig.colorbar(mappable, ax=ax, label='Speed (m/s)')
        cbar.ax.tick_params(labelsize=12)  
        cbar.set_label('Speed (m/s)', fontsize=14) 

    # Reference line
    slope = -16 * 1000 / 3600
    x0, y0 = 0, 1000
    x_vals = np.array([0, getattr(config, 'time_max', 100)])  
    y_vals = y0 + slope * (x_vals - x0)
    ax.plot(x_vals, y_vals, color='white', linestyle='--', linewidth=2)

    x_text = 100
    y_text = y0 + slope * (x_text - x0)
    ax.text(x_text, y_text, '-16 km/h', color='white', fontsize=12, va='bottom', ha='left')

    ax.set_xlim(0, getattr(config, 'time_max', max((rec['t'] for v in sim.vehicles for rec in getattr(v, 'history', [{'t':0}]))) ))
    ax.set_ylim(0, getattr(config, 'road_length', max((rec['position'] for v in sim.vehicles for rec in getattr(v, 'history', [{'position':0}]))) ))

    ax.set_xlabel('Time (s)', fontsize=14)     
    ax.set_ylabel('Position (m)', fontsize=14) 

    ax.tick_params(axis='both', labelsize=12)  

    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()



def plot_speed_time_series(sim, vehicle_ids=[1,2,3,4,5,6,7,8,9,10], config=None):
    fig, ax = plt.subplots(figsize=(9, 6))
    
    colors = plt.cm.get_cmap('tab10', len(vehicle_ids))
    
    max_times = []  
    for idx, vid in enumerate(vehicle_ids):
        vehicle = next((v for v in sim.vehicles if v.id == vid), None)
        if vehicle is None or not hasattr(vehicle, 'history') or len(vehicle.history) == 0:
            continue
        
        times = np.array([rec['t'] for rec in vehicle.history], dtype=float)
        speeds = np.array([rec['speed'] for rec in vehicle.history], dtype=float)
        
        ax.plot(times, speeds, color=colors(idx), label=f'Vehicle {vid}', linewidth=1.5)
        
        max_times.append(times[-1])  

    ax.set_xlabel('Time (s)', fontsize=14)     
    ax.set_ylabel('Speed (m/s)', fontsize=14)  

    if config and hasattr(config, 'speed_limit'):
        ax.set_ylim(0, config.speed_limit*1.05)
    else:
        max_speed = max([max([rec['speed'] for rec in v.history]) 
                         for v in sim.vehicles if hasattr(v, 'history') and len(v.history)>0] + [1])
        ax.set_ylim(-2, max_speed*1.05)
    
    if len(max_times) > 0:
        ax.set_xlim(0, max(max_times))
    elif config and hasattr(config, 'time_max'):
        ax.set_xlim(0, config.time_max)

    ax.tick_params(axis='both', labelsize=12)   

    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(fontsize=12)                      

    plt.tight_layout()
    plt.show()