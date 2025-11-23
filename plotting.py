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

        # Build segments between consecutive points
        points = np.vstack([times, positions]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Color each segment by the mean speed on that segment
        seg_speeds = 0.5 * (speeds[:-1] + speeds[1:])

        lc = LineCollection(segments, cmap=cmap, norm=norm, linewidths=1.5)
        lc.set_array(seg_speeds)
        ax.add_collection(lc)
        any_segments = True

    # Colorbar (only if we drew at least one vehicle)
    if any_segments:
        mappable = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        mappable.set_array([])
        fig.colorbar(mappable, ax=ax, label='Speed (m/s)')

    ax.set_xlim(0, getattr(config, 'time_max', max((rec['t'] for v in sim.vehicles for rec in getattr(v, 'history', [{'t':0}]))) ))
    ax.set_ylim(0, getattr(config, 'road_length', max((rec['position'] for v in sim.vehicles for rec in getattr(v, 'history', [{'position':0}]))) ))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()