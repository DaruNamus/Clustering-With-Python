import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from tkinter import *

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

def show_borrower_data():
    # Read data
    data = pd.read_csv("clustering.csv")
    
    # Visualize data point
    plt.scatter(data["ApplicantIncome"], data["LoanAmount"], c="blue")
    plt.xlabel("Applicant Income")
    plt.ylabel("Loan Amount (In Thousands)")
    plt.title("Data Peminjam")
    plt.show()

def show_initial_centroids():
    # Read data
    data = pd.read_csv("clustering.csv")
    
    X = data[["ApplicantIncome", "LoanAmount"]]
    # Initialize centroids
    K = 3
    Centroids = X.sample(n=K)
    
    # Plot initial centroids
    plt.scatter(X["ApplicantIncome"], X["LoanAmount"], c="blue")
    plt.scatter(Centroids["ApplicantIncome"], Centroids["LoanAmount"], c="red")
    plt.xlabel("Annual Income")
    plt.ylabel("Loan Amount (In Thousand)")
    plt.title("Titik Awal Centroid")
    plt.show()

def show_clustering_result():
    # Read data
    data = pd.read_csv("clustering.csv")
    
    X = data[["ApplicantIncome", "LoanAmount"]]
    # Initialize centroids
    K = 3
    Centroids = X.sample(n=K)
    
    # K-means algorithm
    diff = 1
    j = 0
    while diff != 0:
        XD = X
        i = 1
        for index1, row_c in Centroids.iterrows():
            ED = []
            for index2, row_d in XD.iterrows():
                d1 = (row_c["ApplicantIncome"] - row_d["ApplicantIncome"]) ** 2
                d2 = (row_c["LoanAmount"] - row_d["LoanAmount"]) ** 2
                d = sqrt(d1 + d2)
                ED.append(d)
            X[i] = ED
            i = i + 1

        C = []
        for index, row in X.iterrows():
            min_dist = row[1]
            pos = 1
            for i in range(K):
                if row[i + 1] < min_dist:
                    min_dist = row[i + 1]
                    pos = i + 1
            C.append(pos)
        X["Cluster"] = C
        Centroids_new = X.groupby(["Cluster"]).mean()[["LoanAmount", "ApplicantIncome"]]
        if j == 0:
            diff = 1
            j = j + 1
        else:
            diff = (Centroids_new['LoanAmount'] - Centroids['LoanAmount']).sum() + \
                   (Centroids_new['ApplicantIncome'] - Centroids['ApplicantIncome']).sum()
            print(diff.sum())
        Centroids = X.groupby(["Cluster"]).mean()[["LoanAmount", "ApplicantIncome"]]

    # Plot the final clusters
    color = ['blue', 'green', 'cyan']
    for k in range(K):
        data = X[X["Cluster"] == k + 1]
        plt.scatter(data["ApplicantIncome"], data["LoanAmount"], c=color[k])
    plt.scatter(Centroids["ApplicantIncome"], Centroids["LoanAmount"], c='red')
    plt.xlabel('Income')
    plt.ylabel('Loan Amount (In Thousands)')
    plt.title("Hasil Klustering")
    plt.show()

# Create main window
root = Tk()
root.title("K-means Clustering Menu")

# Create menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

k_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=k_menu)

# Add menu items for different actions
k_menu.add_command(label="Data Peminjam", command=show_borrower_data)
k_menu.add_command(label="Titik Awal Centroid", command=show_initial_centroids)
k_menu.add_command(label="Hasil Klustering", command=show_clustering_result)

# Add Quit option
k_menu.add_separator()
k_menu.add_command(label="Quit", command=root.quit)

# Display main window
root.mainloop()

