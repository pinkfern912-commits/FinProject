import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("budget.csv", delimiter=",", encoding="cp1251")
df['Summ'] = df['Summ'].astype(str).str.replace(",", ".").astype(float)

def get_balance():
    income = df[df['Type'] == 'Дохід']['Summ'].sum()
    expense = df[df['Type'] == 'Витрата']['Summ'].sum()
    return income - expense

def get_top_expenses():
    return (
        df[df['Type'] == 'Витрата']
        .groupby('Kategory')['Summ']
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )

def show_expenses_chart():
    df[df['Type'] == 'Витрата'].groupby('Kategory')['Summ'].sum().plot(kind='bar')
    plt.title("Витрати по категоріях")
    plt.show()

def get_expenses_by_category():
    return df[df['Type'] == 'Витрата'].groupby('Kategory')['Summ'].sum()
