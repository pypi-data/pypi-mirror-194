# Here we test the BumpHunter2D class.
# This is an extension of the BumpHunter algorithm to 2D histograms.
# We will use 2D histograms ranging between 0 and 25 (both axis) with 20*20 even bins.

import matplotlib
import numpy as np

matplotlib.use("Agg")
from datetime import datetime  # # Used to compute the execution time

import matplotlib.pyplot as plt

import pyBumpHunter as BH

# Generate the background
np.random.seed(42)
bkg = np.random.exponential(scale=[4, 4], size=(1_000_000, 2)) # Need more stat to have a smoother reference

# Generate the data
Nsig = 700
data = np.empty(shape=(100_000 + Nsig, 2))
data[:100_000] = np.random.exponential(scale=[4, 4], size=(100_000, 2))
data[100_000:] = np.random.multivariate_normal(
    mean=[6.0, 7.0], cov=[[3, 0.5], [0.5, 3]], size=(Nsig)
)

# Expected position of the bump in the data
Lth = [6.0, 7.0]

# Range of the histograms (used in the scans)
rang = [[0, 25], [0, 25]]

# Plot the 2 distributions (data and background) as 2D histograms
F = plt.figure(figsize=(11, 10))
plt.title("Test distribution (background)")
_, binx, biny, _ = plt.hist2d(
    bkg[:, 0], bkg[:, 1], bins=[20, 20], range=rang, norm=matplotlib.colors.LogNorm()
)
plt.xticks(fontsize="xx-large")
plt.yticks(fontsize="xx-large")
plt.colorbar()
plt.savefig("results/2D/hist_bkg.png", bbox_inches="tight")
plt.close(F)

# The red dashed lines show the true posision of the signal
F = plt.figure(figsize=(11, 10))
plt.title("Test distribution (data)")
plt.hist2d(
    data[:, 0], data[:, 1], bins=[20, 20], range=rang, norm=matplotlib.colors.LogNorm()
)
plt.hlines([5.0, 9.0], binx[0], binx[-1], linestyles="dashed", color="r")
plt.vlines([4.0, 8.0], biny[0], biny[-1], linestyles="dashed", color="r")
plt.colorbar()
plt.savefig("results/2D/hist_data.png", bbox_inches="tight")
plt.close(F)

# Create a BumpHunter2D class instance
hunter = BH.BumpHunter2D(
    rang=rang,
    width_min=[2, 2],
    width_max=[3, 3],
    width_step=[1, 1],
    scan_step=[1, 1],
    bins=[20, 20],
    npe=8000,
    nworker=1,
    seed=666,
    use_sideband=True # Activate side-band normalization
)

# Call the bump_scan method
print("####bump_scan call####")
begin = datetime.now()
hunter.bump_scan(data, bkg)
end = datetime.now()
print(f"time={end - begin}")
print("")

# Print bump
print(hunter.bump_info(data))
print(f"   mean (true) = {Lth}")
print("")


# Get and save bump plot
hunter.plot_bump(data, bkg, filename="results/2D/bump.png")

# Get and save statistics plot
hunter.plot_stat(show_Pval=True, filename="results/2D/BH_statistics.png")

