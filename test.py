from Map import Map
import random
from CustomKMeans import CustomKMeans
from sklearn.cluster import KMeans
import math

def main():

        N: int = 100
        experimental_data = [City(random.randint(1,N),random.randint(1,N)) for i in range(N)]
        experimental_data_for_Kmeans = [(city.x,city.y) for city in experimental_data]
        CKmeans = CustomKMeans(k=3,random_seed=42)
        Kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto").fit(experimental_data_for_Kmeans)
        centers_KMeans = Kmeans.cluster_centers_
        wcss_KMeans = 0
        distance_KMeans = 0
        for city,center in zip(experimental_data_for_Kmeans,Kmeans.labels_):
            distance_KMeans = (math.pow((centers_KMeans[center][0] - city[0]), 2) + math.pow((centers_KMeans[center][1] - city[1]), 2))
            wcss_KMeans += math.sqrt(distance_KMeans)

        wcss_CKMeans = 0
        clusters_CKMeans = CKmeans.fit(experimental_data)
        centers_CKMeans = CKmeans.get_cluster_centers()
        for cluster,center in zip(clusters_CKMeans,centers_CKMeans):
              distance_CKMeans = 0
              for city in cluster:
                    distance_CKMeans = (math.pow((center[0] - city.x), 2) + math.pow((center[1] - city.y), 2))
                    wcss_CKMeans += math.sqrt(distance_CKMeans)

        print(f"WCSS CKMeans: {round(wcss_CKMeans, 5)}\t ||\t WCSS KMeans: {round(wcss_KMeans, 5)}")
if __name__ == "__main__":
    main()
