import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataAnalyzer:
    """
    A utility class for analyzing data and plotting survival information.
    """

    @staticmethod
    def calculate_survival_percentage(df, feature_to_group):
        """
        Calculate the survival percentage based on the grouped data.

        Parameters:
            df (DataFrame): The DataFrame containing the data.
            feature_to_group (str): The feature used for grouping.

        Returns:
            DataFrame: The input DataFrame with an additional column 'survival_percentage' showing the percentage of
                    passengers who survived for each category of the feature.
        """
        try:
            grouped = df.groupby([feature_to_group, 'survived']).size().reset_index(name='count')
            total_passengers = grouped.groupby(feature_to_group)['count'].sum().reset_index()
            grouped = grouped.merge(total_passengers, on=feature_to_group, suffixes=('', '_total'))
            grouped['survival_percentage'] = grouped['count'] / grouped['count_total'] * 100
            return grouped
        except ValueError as e:
            raise ValueError("Error calculating survival percentage: " + str(e))

    @staticmethod
    def plot_survival_by_feature(grouped_data, feature_x, x_title, y_title, title):
        """
        Plot the survival percentage by a specific feature.

        Parameters:
            grouped_data (DataFrame): The grouped data containing survival percentages for each category of the feature.
            feature_x (str): The feature to plot on the x-axis.
            x_title (str): The title for the x-axis.
            y_title (str): The title for the y-axis.
            title (str): The title for the plot.

        Returns:
            None
        """
        try:
            ax = sns.barplot(x=feature_x, y='survival_percentage', hue='survived', data=grouped_data)
            plt.xlabel(x_title)
            plt.ylabel(y_title)
            plt.title(title, fontsize=16)

            ax.legend(title='Survived', loc='upper left', facecolor='white', framealpha=1)
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), 
                            textcoords='offset points')

            plt.show()
        except ValueError as e:
            raise ValueError("Error plotting survival by feature: " + str(e))

    @staticmethod
    def get_missing_values(df):
        """
        Get information about missing values in the DataFrame.

        Parameters:
            df (DataFrame): The DataFrame containing the data.

        Returns:
            pandas.io.formats.style.Styler: Styler object representing the table with missing value information.
        """
        try:
            null_per_column = df.isnull().sum()
            nulls_grt_zero = null_per_column[null_per_column > 0].sort_values(ascending=False)
            total_datos = df.shape[0]
            perc_nulls = nulls_grt_zero / total_datos * 100
            nulls_table = pd.concat([nulls_grt_zero, perc_nulls], axis=1)
            nulls_table.columns = ['Total Nulos', '% Nulos']
            nulls_result = nulls_table.style.background_gradient(cmap='Oranges', low=0, high=1)
            return nulls_result
        except ValueError as e:
            raise ValueError("Error getting missing values: " + str(e))
