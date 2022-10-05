import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    sns.set_context('talk')
    population = pd.read_csv("CSV_Files/world_pop_data.csv")
    meta = pd.read_csv('CSV_Files/metadata_country.csv')

    population_simple = population[['Country Code'] + list(population.loc[:, '1960' : '2020'])]
    population.iloc[:10]

# **Population Growth:** Let's calulculate the Top Five Most Countries by population Growth Rate in the world.

    pop_table = pd.melt(population_simple, id_vars=['Country Code'], var_name='Date', value_name='Population', ignore_index=False)
    pop_table_sorted = sort_columns(pop_table, ['Country Code' , 'Date']).set_index('Country Code').fillna(method='ffill').fillna(0)

# **Top Five Coutries by Growth Rate (2019 - 2020):** The following five countries' names listed in descending order who have highest population growth rate from 2019 to 2020.
    # code to check the population from 1960 to 2020 to ensure the max initially although the population growth of each country should be max at 2020

    growth_rate =  pop_table_sorted.groupby('Country Code')[['Population']].agg(cal_growth).rename(columns={'Population' : 'Population Rate'})
    top_growth_rate_sorted = sort_columns(growth_rate, 'Population Rate', ascending=False).iloc[: 5]
    print(top_growth_rate_sorted)

    # merge pop_table_sorted with meta on the basis of country code with inner join

    pop_table_sorted_meta_merged = pop_table_sorted.merge(meta, on='Country Code')

# **Visualzation:** The visualization of top five countries by Growth Rate will be displayed according to the region:

    countries_top_pop_by_region = pop_table_sorted_meta_merged[pop_table_sorted_meta_merged['Country Code'].isin(top_growth_rate_sorted.index)].rename(columns={'TableName' : 'Country Name'})
    f = sns.relplot(y='Population', x='Date', data=countries_top_pop_by_region, kind='line', hue='Country Name', col='Region', col_wrap=1 , aspect=2.8)
    plt.yscale('log')
    f.set_xticklabels(rotation = 90)
    f.fig.supxlabel('Date from 1960 to 2020', y=-0.04, x=0.43, fontsize=19)
    f.set_xlabels('')
    f.fig.suptitle('Population Figure of top five countries by growth rate of World in respective Regions', y=1.03)
    countries_top_pop_by_region
    plt.show()

# It seems that the highest population growth rate countries are those who have lower and lower-middle income, lets take a look at relation of Population rate with income group to have a idea.

    growth_rate_income = pop_table_sorted_meta_merged.merge(growth_rate, on='Country Code')
    growth_rate_income_model = growth_rate_income[['Country Code', 'IncomeGroup' , 'Population Rate']].set_index('Country Code').drop_duplicates().dropna().rename(columns={'Population Rate' : 'Population_Rate'})
    fig = sns.boxplot(x='IncomeGroup', y='Population_Rate', data=growth_rate_income_model, order=['Low income' , 'Lower middle income' , 'Upper middle income' , 'High income'])
    plt.xticks(rotation=25, fontsize=14)
    plt.show()
    fig.set(ylabel='Population Rate', xlabel ='Income Group')
    plt.clf()

# **Population vs Income Group:** The upper box plot shows that at average the High income have low Population rate, as well as outliers of countries' population. But in general the box plot tells that at most cases the higher the income , the lower the population rate. The outliers in this case are exceptional. The inter quantile range of the income categories tell us that the most high income countries have lower population rate. The downward outliers in low income show less population due to extreme low income, while the upward outliers in High income show of the countries where people have higher income at genral and they are fond of growing population. But generally, this is exception, not a rule. 

# **Visualization of Population rate (1960 - 2020):** Let's Visualize the population rate of each region from 1960 - 2020.

    table =  pop_table_sorted_meta_merged.dropna().groupby(['Region', 'Date'], as_index=False)[['Population']].agg(cal_growth_rate_mean).rename(columns={'Population' : 'Population Rate'})
    fig = sns.relplot(x='Date', y='Population Rate', data=table, hue='Region', kind='line', aspect=2.8)
    plt.yscale('linear')
    plt.xticks(rotation=90)
    plt.xlabel('Date from 1990 to 2020')
    plt.show()

# **Teriible:** Oh It seems that the East Asia and Pacific region has the such highest popualtion growth over the time that we cannnot conclude the insights of other regions. Lets visualize by removing the East Asia and Pacific.

# Although the population growth decreased from 1960 to 1990, but after that it managed to somehow increase the population growth.

    table_outside_asia = table[table['Region'] != 'East Asia & Pacific']
    fig = sns.relplot(x='Date', y='Population Rate', data=table_outside_asia, hue='Region', kind='line', aspect=2.8)
    fig.set_xticklabels(rotation=90)
    plt.show()

    ## Warning!!
#  The visualization of the other regions tells nothing special except the three ones. North America, Middle East & North Africa, Latin America and Central Asia. These three regions'countries are warned to increase their population growth rate, except Malta and Bahrain from Middle East and North Africa, who have higher growth Rate and managed to increase their population Rate. If these regions want man power and population growth upon their own country men, not from outsiders, they must find ways to increase population growth. 

    ## The finally Markdown on East Asia and Pacific

# The East Asia and Pacific region, which has highest growth rate over the period of time, must have the higher or middle income coutries at most. We can verify the results

    table = growth_rate_income.drop_duplicates('Country Code')
    print(table.value_counts(['Region' , 'IncomeGroup'])) 

# **Verification:** The East Asia and Pacific region has the most countries. It managed to upgrade the the population growth rate due to more than 50 % of 14 lower middle income countries. So, the credits goes to these 14 lower middle countries group.

    growth_rate_income = growth_rate_income.drop_duplicates('Country Code')
    growth_rate_income_by_region = growth_rate_income.groupby(['Region', 'Country Code', 'IncomeGroup'], as_index=False)[['Population Rate']].mean()
    growth_rate_income_by_region_sorted = growth_rate_income_by_region.sort_values('Population Rate', ascending=False).reset_index(drop=True)
    growth_rate_income_by_region_sorted_by_east_asia = growth_rate_income_by_region_sorted[growth_rate_income_by_region_sorted['Region'] == 'East Asia & Pacific']
    print(growth_rate_income_by_region_sorted_by_east_asia)


# **Verification More:** Hurray! It's glad to know that the most mainting the growth rate countries in East Asia & Pacific belong to lower middle Income. 

# Note: The population Growth is as per 2020.

# Hope you like the Presentation.




def sort_columns(table_name, column_names : list, ascending=True):
    return table_name.sort_values(by=column_names, ascending=ascending)

def cal_growth(column):
    return ((column[-1] - column[-2]) / column[-2]) * 100

def cal_growth_rate_mean(column):
    column = list(column)
    rate = column[0]
    growth = [0]
    for index, value in enumerate(column):
        if (index != 0):
            rate = ((value - column[index-1]) / column[index-1]) * 100
            growth.append(rate)
    return np.mean(growth)

if __name__ == '__main__':
    main()


table = {
         'Age' : [34, 12, 24]
            }

table = pd.DataFrame(table)
test_table = sort_columns(table, ['Age'], ascending=[True])
print(test_table)