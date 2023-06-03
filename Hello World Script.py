
# Answer to the first question

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

webdriver_path = r'E:\Downloads\chromedriver_win32\chromedriver.exe'

driver = webdriver.Chrome(executable_path=webdriver_path)


url = 'https://jobs.homesteadstudio.co/data-engineer/assessment/download/'
driver.get(url)


download_button = driver.find_element("class name", "wp-block-button__link")
download_button.click()

time.sleep(5)

driver.quit()

#Answer to number 2

excel_file = r'C:\Users\roque\Downloads\skill_test_data.xlsx'  
df = pd.read_excel(excel_file, sheet_name='data')


pivot_table = pd.pivot_table(df, values=['Spend', 'Attributed Rev (1d)', 'Imprs', 'Visits', 'New Visits', 'Transactions (1d)', 'Email Signups (1d)'],
                             index='Platform (Northbeam)', aggfunc='sum')


pivot_table = pivot_table.sort_values(by='Attributed Rev (1d)', ascending=False)

columns_order = ['Spend', 'Attributed Rev (1d)', 'Imprs', 'Visits', 'New Visits', 'Transactions (1d)', 'Email Signups (1d)']
pivot_table = pivot_table[columns_order]


pivot_table['Attributed Rev (1d)'] = pivot_table['Attributed Rev (1d)'].apply(lambda x: '${:,.2f}'.format(round(x, 2)) if pd.notnull(x) else '$-')
pivot_table['Spend'] = pivot_table['Spend'].apply(lambda x: '{:,.2f}'.format(round(x, 2)) if pd.notnull(x) else '')
pivot_table['Imprs'] = pivot_table['Imprs'].apply(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else '')
pivot_table['Visits'] = pivot_table['Visits'].apply(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else '')
pivot_table['New Visits'] = pivot_table['New Visits'].apply(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else '')
pivot_table['Transactions (1d)'] = pivot_table['Transactions (1d)'].apply(lambda x: '-' if pd.isnull(x) else '{:,.2f}'.format(round(x, 2)))
pivot_table['Email Signups (1d)'] = pivot_table['Email Signups (1d)'].apply(lambda x: '-' if pd.isnull(x) else '{:,.2f}'.format(round(x, 2)))

pivot_table.columns = ['Sum of ' + col for col in pivot_table.columns]



print(pivot_table)

# Answer to number 3
conn = sqlite3.connect('pivot_table.db')
pivot_table.to_sql('pivot_table', conn)
conn.close()
