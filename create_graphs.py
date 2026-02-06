import database
import matplotlib.pyplot as plt
import numpy as np

def main(
    datapoint_comparator: str = "Neto_preb",
    datapoints_to_compare: list[str] = ["Ocena_življ", "Ocena_odnos", "Zdravje_1"],
    save_location = 'data/graphs'
) -> None:
    
    for datapoint in datapoints_to_compare:
        datapoint_map = []

        for i in range(1, 13):
            to_compare_stats = [float(n) for n in database.get_stat_for_all_years("osebe", i, datapoint)]
            comparator_stats = [float(n) for n in database.get_stat_for_all_years("osebe", i, datapoint_comparator)]

            datapoint_map.append([
                sum(comparator_stats)/len(comparator_stats), 
                sum(to_compare_stats)/len(to_compare_stats)
            ])

        datapoint_map.sort(key=lambda x: x[0])
        x_values = [point[0] for point in datapoint_map]
        y_values = [point[1] for point in datapoint_map]

        # Calculate the trend line
        z = np.polyfit(x_values, y_values, 1)
        p = np.poly1d(z)

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(x_values, y_values, 'o', label='Data Points')
        ax.plot(x_values, y_values, '-', alpha=0.3)
        ax.plot(x_values, p(x_values), "r--", 
                label=f"Trend Line (y={z[0]:.2f}x + {z[1]:.2f})", 
                alpha=0.7)

        ax.set_xlabel(datapoint_comparator)
        ax.set_ylabel(datapoint)
        ax.set_title(f"Korelacija: {datapoint} proti {datapoint_comparator}")
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)

        fig.tight_layout()
        fig.savefig(f"{save_location}/{datapoint}_proti_{datapoint_comparator}.png")

        plt.close(fig) 

if __name__ == "__main__":
    main()