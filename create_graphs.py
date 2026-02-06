import database
import matplotlib.pyplot as plt
import numpy as np

def is_float(s:str) -> bool:
    try:
        float(s)
        return True
    except Exception as e:
        return False
    
def plot(x_values, y_values, x_label, y_label, title):
    # Calculate the trend line
    z = np.polyfit(x_values, y_values, 1)
    p = np.poly1d(z)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x_values, y_values, 'o', label='Data Points')
    ax.plot(x_values, y_values, '-', alpha=0.3)
    ax.plot(x_values, p(x_values), "r--", 
            label=f"Trend Line (y={z[0]:.2f}x + {z[1]:.2f})", 
            alpha=0.7)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)

    fig.tight_layout()

    return fig, ax

def primerjalni_grafi(
    datapoint_comparator: str = "Neto_preb",
    datapoints_to_compare: list[str] = ["Ocena_življ", "Ocena_odnos", "Zdravje_1", "Stpn_socizklj"],
    save_location = 'data/graphs'
) -> None:
    
    for datapoint in datapoints_to_compare:
        datapoint_map = []

        for i in range(1, 13):
            to_compare_stats = [float(n) for n in database.get_stat_for_all_years("osebe", i, datapoint)[0] if is_float(n)]
            comparator_stats = [float(n) for n in database.get_stat_for_all_years("osebe", i, datapoint_comparator)[0] if is_float(n)]

            datapoint_map.append([
                sum(comparator_stats)/len(comparator_stats), 
                sum(to_compare_stats)/len(to_compare_stats)
            ])

        datapoint_map.sort(key=lambda x: x[0])
        x_values = [point[0] for point in datapoint_map]
        y_values = [point[1] for point in datapoint_map]

        fig, ax = plot(x_values, y_values, datapoint_comparator, datapoint, f"Korelacija: {datapoint} proti {datapoint_comparator}")

        fig.savefig(f"{save_location}/{datapoint}_proti_{datapoint_comparator}.png")

        plt.close(fig)

if __name__ == "__main__":
    primerjalni_grafi()