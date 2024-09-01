import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = 'AsyncSlowdownComparisonVector4.csv'  # Update with the correct path to your CSV file
df = pd.read_csv(file_path)

# Remove the '%' sign and convert the 'Cost' column to numeric values
df['Cost'] = df['Cost'].str.rstrip('%').astype(float)

# List of 14 benchmarks from the Are We Fast Yet (AWFY) benchmark suite
awfy_benchmarks = [
    "Bounce", "CD", "DeltaBlue", "Havlak", "Json", "List",
    "Mandelbrot", "NBody", "Permute", "Queens", "Richards",
    "Sieve", "Storage", "Towers"
]

# Filter the dataframe to only include the benchmarks from AWFY
df_filtered = df[df['Benchmark'].isin(awfy_benchmarks)]

# Add a unique identifier to each method within the same benchmark and variant
df_filtered['UniqueMethod'] = df_filtered.groupby(['Benchmark', 'Method', 'Variant']).cumcount() + 1
df_filtered['UniqueMethod'] = df_filtered['Method'] + ' (' + df_filtered['UniqueMethod'].astype(str) + ')'

# Escape $ symbols in method names
df_filtered['UniqueMethod'] = df_filtered['UniqueMethod'].str.replace('$', r'\$', regex=False)

# Pivot the data to get Slowdown and NoSlowdown side by side
df_pivot = df_filtered.pivot_table(index='UniqueMethod', columns='Variant', values='Cost', aggfunc='first')

# Calculate the absolute difference
df_pivot['Difference'] = (df_pivot['_Slowdown'] - df_pivot['_NoSlowdown']).abs()

# Plot setup
plt.figure(figsize=(14, 10))

# Plot bars with differences
bars = plt.bar(df_pivot.index, df_pivot['Difference'].fillna(0), color='blue', edgecolor='black')

# Highlight bars where one variant is missing in red with a more prominent pattern
for i, diff in enumerate(df_pivot['Difference']):
    if pd.isna(df_pivot['_Slowdown'].iloc[i]) or pd.isna(df_pivot['_NoSlowdown'].iloc[i]):
        bars[i].set_color('red')
        bars[i].set_hatch('xx')  # Use a more visible hatch pattern

# Adjust the plot aesthetics
plt.title('Absolute Difference between Slowdown and NoSlowdown Costs for Each Method')
plt.ylabel('Difference (%)')
plt.xlabel('Method')
plt.xticks(rotation=90)
plt.tight_layout()

# Save the plot
plt.savefig("AsyncSlowdownPercentageComparisonBarChart.pdf")

# Show the plot
plt.show()
