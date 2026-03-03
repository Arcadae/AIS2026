import matplotlib.pyplot as plt
from typing import Callable, Any
from time import perf_counter, time
from City import City
import random
from CustomKMeans import CustomKMeans
from JarvisMarch import JarvisMarch
from Clusterizer import Clusterizer
from sklearn.cluster import KMeans

def main():
    clusterizer = Clusterizer()

    experimental_data = [City(random.randint(1, 100), random.randint(1, 100)) for _ in range(300)]
    experimental_data_for_KMeans = [(city.x, city.y) for city in experimental_data]

    X_plot = [5,10,15,20,25,30]
    Y_plot_alg = [0,0,0,0,0,0]
    Y_plot_CKmeans = [0,0,0,0,0,0]
    Y_plot_Kmeans = [0,0,0,0,0,0]

    for _ in range(6):
        start_time = perf_counter()
        clusterizer.set_points(experimental_data)
        hull_points = JarvisMarch.jarvis_march(experimental_data)
        clusterizer.select_centers_from_hull(hull_points, X_plot[_])
        clusterizer.assign_points_to_clusters()
        end_time = perf_counter()
        Y_plot_alg[_] = end_time - start_time

    for _ in range(6):
        start_time = perf_counter()
        CKmeans = CustomKMeans(k=X_plot[_],random_seed=42)
        CKmeans.fit(experimental_data)
        end_time = perf_counter()
        Y_plot_CKmeans[_] = end_time - start_time
    
    for _ in range(6):
        start_time = perf_counter()
        Kmeans = KMeans(n_clusters=X_plot[_], random_state=0, n_init="auto")
        Kmeans.fit(experimental_data_for_KMeans)
        end_time = perf_counter()
        Y_plot_Kmeans[_] = end_time - start_time

    print(f"Значение || Алг. || CKMeans || KMeans")
    for x,i,j,k in zip(X_plot,Y_plot_alg,Y_plot_CKmeans,Y_plot_Kmeans):
        print(f"{x} || {i} || {j} || {k}")

    plt.plot(X_plot, Y_plot_alg, label='Алгоритм')
    plt.plot(X_plot, Y_plot_CKmeans, label='Кастомный KMeans')
    plt.plot(X_plot, Y_plot_Kmeans, label='KMeans')

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Реализации')
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()