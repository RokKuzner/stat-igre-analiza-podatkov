import database
import matplotlib.pyplot as plt
import numpy as np

def main(
        datapoint_comparator:str = "Neto_preb",
        datapoints_to_compare:list[str] = ["Ocena_življ", "Ocena_odnos", "Zdravje_1"],
        save_location = 'data/graphs'
) -> None:
    datapoint_map = []

    for datapoint in datapoints_to_compare:
        for i in range(1, 13):
            to_compare_stats = [float(n) for n in database.get_stat_for_all_years("osebe", i, datapoint)]
            comparator_stats = [float(n) for n in database.get_stat_for_all_years("osebe", i, datapoint_comparator)]

            datapoint_map.append([sum(comparator_stats)/len(comparator_stats), sum(to_compare_stats)/len(to_compare_stats)])

        datapoint_map.sort(key=lambda x: x[0])
        x_values = [point[0] for point in datapoint_map]
        y_values = [point[1] for point in datapoint_map]

        # Calculate the trend line (linear regression)
        z = np.polyfit(x_values, y_values, 1)
        p = np.poly1d(z)

        plt.plot(x_values, y_values, 'o', label='Data Points') # 'o' means points only
        plt.plot(x_values, y_values, '-', alpha=0.5)
        plt.plot(x_values, p(x_values), "r--", label=f"Trend Line (y={z[0]:.2f}x + {z[1]:.2f})", alpha=0.5)

        plt.xlabel(datapoint_comparator)
        plt.ylabel(datapoint)
        plt.title(datapoint)

        plt.savefig(save_location+f"/{datapoint}_proti_{datapoint_comparator}.png")

main()