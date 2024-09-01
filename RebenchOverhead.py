import pandas as pd

# Define correct column names
column_names = ["invocation", "iteration", "value", "unit", "criterion", "benchmark", 
                "executor", "suite", "extraArgs", "cores", "inputSize", "varValue", "machine"]

# Load the dataset
df = pd.read_csv("/home/hburchell/Repos/graal-dev/graal-instrumentation/compiler/GTSlowdownRunOpcodeCost6.data", sep="\t", comment='#', names=column_names)

# Convert the 'value' column to numeric, coercing errors to NaN
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Drop rows where 'value' could not be converted to numeric (i.e., NaN values)
df = df.dropna(subset=['value'])

# Filter only the "Instrumentation" and "NoInstrumentation" experiments
filtered_df = df[df['suite'].isin(['Instrumentation', 'NoInstrumentation'])]

# Group by benchmark name and experiment, then calculate mean runtime for each
grouped = filtered_df.groupby(['benchmark', 'suite'])['value'].mean().unstack()

# Calculate overhead as the percentage increase from "NoInstrumentation" to "Instrumentation"
grouped['Overhead (%)'] = (grouped['Instrumentation'] / grouped['NoInstrumentation'] - 1) * 100

# Display the results in a table format
print(grouped[['NoInstrumentation', 'Instrumentation', 'Overhead (%)']])