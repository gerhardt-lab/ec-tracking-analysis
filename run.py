import argparse
import os
import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from utils.io import read_parameters
from src.compute_speeds import prepare_tracking_data
from src.compute_speeds import plot_quality_control
from src.plot_trajectories import plot_trajectories_per_file
from src.plot_trajectories import plot_trajectories_from_origin_per_file


#########################
# read parameters
#########################

parser = argparse.ArgumentParser(description='Run ec movement trajectory analysis ')
parser.add_argument('param', type=str, help='Path to the parameter file.')

args = parser.parse_args()
print("-------")
print("reading parameters from: ", args.param)
print("-------")

parameter_file  = args.param
parameters = read_parameters(parameter_file)               

print("-------")
print("used parameter values: ")
print(parameters)
print("-------")

output_folder = parameters["output_folder"]
# save parameter file to output
with open(output_folder + "/parameters.yml", 'w') as outfile:
    yaml.dump(parameters, outfile)

#########################
# read key file
#########################

key_file_path = parameters["key_file"]
key_file = pd.read_csv(key_file_path)
print(key_file.head())

key_file.to_csv(output_folder + "/key_file.csv", index=False)


#########################
# create subfolders
#########################

# create a subfolder for each subject
subjects = ["tracking_data", "trajectory_plots","velocity_plots","quality_control"]

for subject in subjects:
    if not os.path.exists(output_folder + "/" + subject):
        os.mkdir(output_folder + "/" + subject)

#########################
# read data
#########################

tracking_data = prepare_tracking_data(parameters, key_file)
# tracking_data.to_csv(output_folder + "tracking_data/tracking_data.csv", index=False)

#print(tracking_data.head())

#########################
# quality control
#########################

plot_quality_control(parameters, key_file, subfolder = "tracking_data")

#########################
# plot trajectories
#########################

plot_trajectories_per_file(parameters, key_file, subfolder = "tracking_data")
plot_trajectories_from_origin_per_file(parameters, key_file, subfolder = "tracking_data")


#########################
# run analysis - velocity plots
#########################

# grouped by condition and filename

plt.rcParams.update({'font.size': 14})

plot_migration_speeds = migration_speed_df.dropna()
#plot_migration_speeds = plot_migration_speeds.iloc[::subsampling_n, :]
#plot_migration_speeds = plot_migration_speeds.sample(frac=subsample_frac, replace=True, random_state=1)
plot_migration_speeds = plot_migration_speeds[plot_migration_speeds["FRAME"] >= interval]


#fig, ax = plt.subplots(len(intervals),figsize=(15,30))
fig, ax = plt.subplots(1, figsize=(16,8))

sns.lineplot(x = "time_in_h", y = "vel_x_mu_per_h", hue = "condition", hue_order = hue_order,
             data = plot_migration_speeds, style="filename", ax=ax, ci = 90)# , errorbar = errorbar)

#sns.lineplot(x = "FRAME", y = "vel_x", hue = "condition", data = plot_migration_speeds, ax=ax, ci = 90)
#interval_length_min = 5*intervals[i]
#ax.set_title("time interval %s min" % interval_length_min)
ax.set_ylabel("velocity parallel to flow in microns/h")
ax.set_ylim(-7.0,7.0)
ax.axhline(y = 0.0, color = 'r', linestyle = 'dashed')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
plt.savefig(output_folder + "velocity_parallel_to_flow_filename_all.pdf")
plt.savefig(output_folder + "velocity_parallel_to_flow_filename_all.png")
