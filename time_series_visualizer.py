import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Cargar datos. La columna de fechas queda como índice datetime. Esto facilita los filtros y agrupaciones por mes o año.
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Limpiar los datos. Filtrar 2.5% superior e inferior para eliminar outliers
lower = df['value'].quantile(0.025)
upper = df['value'].quantile(0.975)

# Eliminar valores atípicos.
df_clean = df[(df['value'] <= upper) & (df['value'] >= lower)]

# Crear plot de línea con Matplotlib
def draw_line_plot():
    # Crear figura y conjunto de ejes
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_clean.index, df_clean['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig

# Crear plot de barras. Copiar para modificar.
def draw_bar_plot():
    df_bar = df_clean.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Asegurar orden de los meses
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    df_grouped = df_grouped[month_order]

    # Crear Bar Chart
    fig = df_grouped.plot(kind='bar', figsize=(15,5)).figure
    plt.xlabel = 'Years'
    plt.ylabel = 'Average Page Views'
    plt.legend(title='Months')

    fig.savefig('bar_plot.png')
    return fig

# Crear Box Plot con Seaborn
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    # %b hace que 6 sea Jun, en vez de June (%B)
    df_box['month'] = df_box['date'].dt.strftime('%b')
    # Crear month_num para que haya un número del mes ordenable. Sino se ordena alfabeticamente
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    # Creación de una fig con dos axes. 1 row, 2 col   
    fig, axes = plt.subplots(1,2, figsize=(20,7))

    # Gráfico por año, tendencia
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0], palette='Set3', showfliers=False)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_ylim([0,300000]) # Ajustar según datos

    # Gráfico por mes, tendencia
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], palette='pastel', showfliers=False)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_ylim([0,300000])

    fig.savefig('box_plot.png')
    return fig
