import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def real_data():
    """Plots real data using Seaborn."""
    data = {
        'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        '2001': [414, 272, 137, 22, 17, 2, 0, 1, 17, 1, 9, 127],
        '2002': [454, 301, 160, 55, 25, 11, 7, 1, 17, 32, 86, 417],
        '2003': [382, 138, 120, 50, 2, 10, 4, 4, 31, 64, 284, 607],
        '2004': [348, 145, 129, 9, 6, 4, 0, 0, 15, 28, 88, 373]
    }

    Empirical_data = pd.DataFrame(data)

    # Transpose the DataFrame before grouping
    grouped_data = Empirical_data.set_index('Month').T.groupby(level=0, axis=1).sum().T

    # Seaborn Line Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=grouped_data, markers=True, dashes=False)
    plt.title('Infected Over the Months for Each Year')
    plt.xlabel('Year')
    plt.ylabel('Sum')
    plt.tight_layout()
    plt.show()

real_data()
