import numpy as np
import matplotlib.pyplot as plt




filename = 'folder/2024.03.06_Taxol_1/1.5uM_Taxol__to_-4C001.nd2 - 1.5uM_Taxol__to_-4C001.nd2 (series 1)_/Results.csv'
with open(filename, 'r') as f:
    data = np.loadtxt(filename, delimiter=',', skiprows=1)

print(data)
data = data.transpose()
print(data.shape)

mean = np.array((data[1, :]))
angle = np.array((data[2, :]))
lenght = np.array((data[3, :]))
print(mean.shape)
print(angle)
angle[angle<-90] = -180-angle[angle<-90]
print(angle)
print(lenght.shape)

x = np.linspace(0, data.shape[1], data.shape[1])

fig, ax = plt.subplots()

ax.scatter(x, angle, linewidth=2.0)

plt.show()