import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def real_data_series():
    """Transforms DataFrame to Series with ordered months based on years."""
    data = {
        'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        '2001': [414, 272, 137, 22, 17, 2, 0, 1, 17, 1, 9, 127],
        '2002': [454, 301, 160, 55, 25, 11, 7, 1, 17, 32, 86, 417],
        '2003': [382, 138, 120, 50, 2, 10, 4, 4, 31, 64, 284, 607],
        '2004': [348, 145, 129, 9, 6, 4, 0, 0, 15, 28, 88, 373]
    }

    Empirical_data = pd.DataFrame(data)

    # Melt the DataFrame to have 'Year', 'Month', and 'Value' as separate columns
    melted_data = pd.melt(Empirical_data, id_vars='Month', var_name='Year', value_name='Value')

    # Sort the melted data by 'Year' and 'Month'
    sorted_data = melted_data.sort_values(['Year', 'Month'])

    # Create a Series using 'Value' as data and a MultiIndex with 'Year' and 'Month'
    series_data = pd.Series(sorted_data['Value'].values, index=pd.MultiIndex.from_frame(sorted_data[['Year', 'Month']]))

    return series_data

result_series = real_data_series()

# Reshape the data for plotting
plot_data = result_series.unstack(level=0)

# Plotting using Seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=plot_data, markers=True, dashes=False)
plt.title('Infected Over the Months for Each Year')
plt.xlabel('Month')
plt.ylabel('Value')
plt.tight_layout()
plt.show()
