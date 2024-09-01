import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV files
file_path1 = 'AsyncSlowdownComparisonVectorAOTFNOPS.csv'
file_path2 = 'AsyncSlowdownComparisonVectorAOT.csv'
df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

# List of 14 benchmarks from the Are We Fast Yet (AWFY) benchmark suite
awfy_benchmarks = [
    "Bounce", "CD", "DeltaBlue", "Havlak", "Json", "List",
    "Mandelbrot", "NBody", "Permute", "Queens", "Richards",
    "Sieve", "Storage", "Towers"
]

# Filter the dataframes to only include the benchmarks from AWFY
df1_filtered = df1[df1['Benchmark'].isin(awfy_benchmarks)]
df2_filtered = df2[df2['Benchmark'].isin(awfy_benchmarks)]

# Create a dictionary to store the top 5 methods per benchmark variant (_NoSlowdown) for both files
benchmark_variant_methods1 = {}
benchmark_variant_methods2 = {}

for (benchmark, variant), group in df1_filtered.groupby(['Benchmark', 'Variant']):
    if variant == '_NoSlowdown':
        methods = group['Method'].unique()[:5]  # Get the first five methods
        benchmark_variant_methods1[benchmark] = methods

for (benchmark, variant), group in df2_filtered.groupby(['Benchmark', 'Variant']):
    if variant == '_NoSlowdown':
        methods = group['Method'].unique()[:5]  # Get the first five methods
        benchmark_variant_methods2[benchmark] = methods

# Create lists to store whether they agree on the 1st to 5th methods between the two files
method_agreements = {i: [] for i in range(1, 6)}

for benchmark in awfy_benchmarks:
    methods1 = benchmark_variant_methods1.get(benchmark, [])
    methods2 = benchmark_variant_methods2.get(benchmark, [])
    
    for i in range(1, 6):
        if len(methods1) >= i and len(methods2) >= i:
            method_agreements[i].append(1 if methods1[i-1] == methods2[i-1] else 0)
        else:
            method_agreements[i].append(0)  # No agreement if one of the variants is missing

# Create a DataFrame to hold the results for the 1st to 5th methods
agreement_df = pd.DataFrame({
    f'{i}th Method Agreement': method_agreements[i] for i in range(1, 6)
}, index=awfy_benchmarks)

# Create a heatmap to visualize the agreement matrix
plt.figure(figsize=(12, 8))
cmap = sns.color_palette("coolwarm", as_cmap=True)

sns.heatmap(agreement_df, annot=True, cmap=cmap, linewidths=.5, vmin=0, vmax=1, cbar=False, square=True)
plt.title('Agreement on Top 5 Methods between Two Files (_NoSlowdown)')
plt.xlabel('Method Agreement')
plt.ylabel('Benchmark')
plt.tight_layout()

plt.savefig("AsyncSlowdownComparisonMatrix_NoSlowdown.pdf")

plt.show()

import ace_tools as tools
tools.display_dataframe_to_user(name="Top 5 Method Agreement Matrix", dataframe=agreement_df)