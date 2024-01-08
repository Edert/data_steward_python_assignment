#!/usr/bin/env python
# coding=utf8

"""
%prog <PATH>

All files in <PATH> ending with .tsv will be processed. Per file a volcano plot with log2-fold change and -log10(padj) will be plotted.

@author: ChatGPT ;)
"""

import argparse
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def read_data(file_path):
    #Read the TSV file into a DataFrame with header in the first row
    df = pd.read_csv(file_path, sep="\t", header=0)

    #Extract the relevant columns and convert to NumPy arrays
    log2_fold_change = np.array(df['log2FoldChange'])
    padj = np.array(df['padj'])

    return log2_fold_change, padj

def plot_volcano(log2_fold_change, padj, filename):
    #Define colors and labels based on conditions
    colors = np.where(log2_fold_change > 1, 'red', np.where(log2_fold_change < -1, 'blue', 'grey'))

    #Volcano plot
    scatter = plt.scatter(log2_fold_change, -np.log10(padj), c=colors, label='')

    # Customize plot
    plt.title(f'Scatter Plot - {os.path.splitext(filename)[0]}')
    plt.xlabel('log2FoldChange')
    plt.ylabel('-log10(padj)')

    # Create a custom legend
    legend_labels = ['Up-regulated', 'Down-regulated', 'Non-regulated']
    custom_legend = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label) for color, label in zip(['red', 'blue', 'grey'], legend_labels)]
    
    plt.legend(handles=custom_legend, loc='upper right')

    plt.show()


def process_files_in_path(path):
    for filename in os.listdir(path):
        if filename.endswith(".tsv"):
            file_path = os.path.join(path, filename)
            print("Reading data from:",file_path)
            # Read data from each file
            log2_fold_change, padj = read_data(file_path)
            print("Plotting...")
            # Display a scatter plot for each file with filename in the title
            plot_volcano(log2_fold_change, padj, filename)

def main():
    parser = argparse.ArgumentParser(description="Process files in the specified path.")
    parser.add_argument("files_path", help="Path to the directory containing .tsv files")
    args = parser.parse_args()

    # Process files in the specified path
    process_files_in_path(args.files_path)

if __name__ == "__main__":
    main()
