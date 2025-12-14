import matplotlib.pyplot as plt



def generate_time_plot(results):
    names = [r[0] for r in results]
    times = [r[3] for r in results]
    plt.figure()
    plt.bar(names, times)
    plt.ylabel("Time (seconds)")
    plt.title("Algorithms Time Comparison")
    plt.tight_layout()
    path = "time_comparison.png"
    plt.savefig(path)
    plt.close()
    return path