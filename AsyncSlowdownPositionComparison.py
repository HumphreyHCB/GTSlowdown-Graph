import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
file_path = 'AsyncCompareData\AsyncSlowdownComparisonVector6.csv'  # Update with the correct path to your CSV file
df = pd.read_csv(file_path)

# List of 14 benchmarks from the Are We Fast Yet (AWFY) benchmark suite
awfy_benchmarks = [
    "Bounce", "CD", "DeltaBlue", "Havlak", "Json", "List",
    "Mandelbrot", "NBody", "Permute", "Queens", "Richards",
    "Sieve", "Storage", "Towers"
]

# Filter the dataframe to only include the benchmarks from AWFY
df_filtered = df[df['Benchmark'].isin(awfy_benchmarks)]

# Create a dictionary to store the top 5 methods per benchmark variant (Slowdown and NoSlowdown)
benchmark_variant_methods = {}

for (benchmark, variant), group in df_filtered.groupby(['Benchmark', 'Variant']):
    methods = group['Method'].unique()[:5]  # Get the first five methods
    if benchmark not in benchmark_variant_methods:
        benchmark_variant_methods[benchmark] = {}
    benchmark_variant_methods[benchmark][variant] = methods

# Define the variants for comparison
variants = ['_Slowdown', '_NoSlowdown']

# Create lists to store whether they agree on the 1st to 5th methods
method_agreements = {i: [] for i in range(1, 6)}

for benchmark in awfy_benchmarks:
    slowdown_methods = benchmark_variant_methods.get(benchmark, {}).get('_Slowdown', [])
    noslowdown_methods = benchmark_variant_methods.get(benchmark, {}).get('_NoSlowdown', [])
    
    for i in range(1, 6):
        if len(slowdown_methods) >= i and len(noslowdown_methods) >= i:
            method_agreements[i].append(1 if slowdown_methods[i-1] == noslowdown_methods[i-1] else 0)
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
plt.title('Agreement on Top 5 Methods between Slowdown and NoSlowdown')
plt.xlabel('Method Agreement')
plt.ylabel('Benchmark')
plt.tight_layout()

plt.savefig(file_path + ".pdf")

plt.show()

import ace_tools as tools
tools.display_dataframe_to_user(name="Top 5 Method Agreement Matrix", dataframe=agreement_df)
