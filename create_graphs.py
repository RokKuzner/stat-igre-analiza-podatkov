import database
import matplotlib.pyplot as plt
import numpy as np

def is_float(s:str) -> bool:
    try:
        float(s)
        return True
    except Exception as e:
        return False
    
def plot(x_values, y_values, x_label, y_label, title, fig=None, ax=None, show_trend=True, show_legend=True):
    if fig == None or ax == None:
        fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x_values, y_values, 'o', label='Data Points')
    ax.plot(x_values, y_values, '-', alpha=0.3)
    # Calculate the trend line
    if show_trend:
        z = np.polyfit(x_values, y_values, 1)
        p = np.poly1d(z)
        ax.plot(x_values, p(x_values), "r--", 
            label=f"Trend Line (y={z[0]:.2f}x + {z[1]:.2f})", 
            alpha=0.7
            )
        
    if show_legend:
        ax.legend()

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(True, linestyle=':', alpha=0.6)

    fig.tight_layout()

    return fig, ax

def bar(values, names, y_label=None, x_label=None, title=None, fig=None, ax=None, labelrotation:int=None):
    if fig == None or ax == None:
        fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(names, values)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.grid(True, linestyle=':', alpha=0.6)

    if not labelrotation:fig.tight_layout()
    else:
        ax.tick_params(axis='x', labelrotation=labelrotation)
        plt.setp(ax.get_xticklabels(), ha='right', rotation_mode='anchor')
        fig.subplots_adjust(bottom=0.25)

    return fig, ax

def primerjalni_grafi(
    datapoint_comparator: str = "Neto_preb",
    datapoints_to_compare: list[str] = ["Ocena_življ", "Ocena_odnos", "Zdravje_1", "Stpn_socizklj", "Ocena_čas"],
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

def casovni_grafi(
        comparator:str = "Neto_preb",
        save_location = 'data/graphs'
):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(1, 13):
        y_values, x_values = database.get_stat_for_all_years("osebe", i, comparator)
        plot(x_values, y_values, "Čas", comparator, f"Korelacija: {comparator} proti čas za regijo vse regije", fig=fig, ax=ax, show_trend=False, show_legend=False)

    fig.savefig(f"{save_location}/{comparator}_proti_cas_za_vse_regije.png")

    plt.close(fig)

def main() -> None:
    primerjalni_grafi()
    casovni_grafi()

    names = [database.region_id_to_name(i) for i in range(1, 13)]
    values = [database.get_stat_info("osebe", 2024, i, "Neto_preb") for i in range(1, 13)]
    fig, _ = bar(values, names, "Neto dohodek na prebivalca", labelrotation=50)
    fig.savefig("test2.png")

def primerjava_zdravje(save_location = 'data/graphs'):
    datapoint_map = []

    for i in range(1, 13):
        zdravje_1 = database.get_stat_info("osebe", 2024, i, "zdravje_1")
        zdravje_2 = database.get_stat_info("osebe", 2024, i, "zdravje_2")
        zdravje_3 = database.get_stat_info("osebe", 2024, i, "zdravje_3")
        zdravje_4 = database.get_stat_info("osebe", 2024, i, "zdravje_4")
        zdravje_5 = database.get_stat_info("osebe", 2024, i, "zdravje_5")
        zdravje_score = (5*zdravje_1 + 4*zdravje_2 + 3*zdravje_3 + 2*zdravje_4 + 1*zdravje_5) / (zdravje_1 + zdravje_2 + zdravje_3 + zdravje_4 + zdravje_5)
        comparator_stat = database.get_stat_info("osebe", 2024, i, "Neto_preb")

        datapoint_map.append([
                zdravje_score, 
                comparator_stat
            ])
        
    datapoint_map.sort(key=lambda x: x[1])
    x_values = [point[1] for point in datapoint_map]
    y_values = [point[0] for point in datapoint_map]

    fig, ax = plot(x_values, y_values, "neto dohodek na prebivalca v €", "ocena zdravja (1-5)", f"Korelacija: neto dohodek na prebivalca proti ocena zdravja")

    fig.savefig(f"{save_location}/denar_proti_zdravje.png")

    plt.close(fig)

def zdravje_po_regijah(save_location = 'data/graphs'):
    datapoint_map = []

    for i in range(1, 13):
        zdravje_1 = database.get_stat_info("osebe", 2024, i, "zdravje_1")
        zdravje_2 = database.get_stat_info("osebe", 2024, i, "zdravje_2")
        zdravje_3 = database.get_stat_info("osebe", 2024, i, "zdravje_3")
        zdravje_4 = database.get_stat_info("osebe", 2024, i, "zdravje_4")
        zdravje_5 = database.get_stat_info("osebe", 2024, i, "zdravje_5")
        zdravje_score = (5*zdravje_1 + 4*zdravje_2 + 3*zdravje_3 + 2*zdravje_4 + 1*zdravje_5) / (zdravje_1 + zdravje_2 + zdravje_3 + zdravje_4 + zdravje_5)

        datapoint_map.append([
                zdravje_score, 
                database.region_id_to_name(i)
            ])
        
    datapoint_map.sort(key=lambda x: x[0])
    x_values = [point[1] for point in datapoint_map]
    y_values = [point[0] for point in datapoint_map]

    fig, _ = bar(y_values, x_values, title="Ocena zdravja po regijah", labelrotation=50)

    ax = fig.gca()
    y_min = min(y_values)
    y_max = max(y_values)
    padding = (y_max - y_min) * 0.1 
    ax.set_ylim(y_min - padding, y_max + padding)

    fig.savefig(f"{save_location}/zdravje_po_regijah.png")

    plt.close(fig)

if __name__ == "__main__":
    primerjava_zdravje()
    zdravje_po_regijah()