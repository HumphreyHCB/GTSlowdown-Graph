import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data from the CSV file
file_path = 'AsyncSlowdownComparison.csv'  # Update with the correct path to your CSV file
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
    top_methods = group['Method'].unique()[:5]  # Take the first 5 unique methods
    if benchmark not in benchmark_variant_methods:
        benchmark_variant_methods[benchmark] = {}
    benchmark_variant_methods[benchmark][variant] = set(top_methods)

# Define the variants for comparison
variants = ['_Slowdown', '_NoSlowdown']

# Create a matrix to show the agreement between the variants
# Create a matrix to show the agreement between the "_Slowdown" and "_NoSlowdown" variants
agreement_matrix = []

for benchmark in awfy_benchmarks:
    if '_Slowdown' in benchmark_variant_methods.get(benchmark, {}) and '_NoSlowdown' in benchmark_variant_methods.get(benchmark, {}):
        agreement_count = len(benchmark_variant_methods[benchmark]['_Slowdown'].intersection(benchmark_variant_methods[benchmark]['_NoSlowdown']))
        agreement_matrix.append([agreement_count])
    else:
        # No agreement if one of the variants is missing
        agreement_matrix.append([0])

# Convert to a DataFrame for easier handling
agreement_df = pd.DataFrame(agreement_matrix, index=awfy_benchmarks, columns=['_Slowdown vs _NoSlowdown'])

# Create a heatmap to visualize the agreement matrix
plt.figure(figsize=(10, 8))
cmap = sns.color_palette("coolwarm", as_cmap=True)

sns.heatmap(agreement_df, annot=True, cmap=cmap, linewidths=.5, vmin=0, vmax=5, square=True)
plt.title('Agreement Matrix of Top 5 Methods between Slowdown and NoSlowdown')
plt.xlabel('Comparison')
plt.ylabel('Benchmark')
plt.tight_layout()

plt.savefig("BenchmarkAgreementMatrix.pdf")

plt.show()

import ace_tools as tools
tools.display_dataframe_to_user(name="Agreement Matrix", dataframe=agreement_df)

