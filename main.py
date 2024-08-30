import asyncio
import pandas as pd
import streamlit as st
from core import Core


async def process_excel_file(excel_file):
    df = pd.read_excel(excel_file, names=['Links', 'Count'], header=None, sheet_name='Лист2')
    results = await core.run_parse_tasks(df.loc[:, 'Links'].values)
    results['Кол-во'] = df['Count']
    results['Стоимость'] = results['Кол-во'].map(int) * results['Цена'].map(int)

    columns_titles = ['Наименование', 'Кол-во', 'Цена', 'Стоимость', 'Наличие']
    results = results.reindex(columns=columns_titles)
    return results


async def main():
    st.title("Обработка товаров из Excel файла")

    uploaded_excel_file = st.file_uploader("Загрузите Excel файл", type=["xlsx", "xls"])

    if uploaded_excel_file is not None:
        st.write("Обработанные данные")
        results = await process_excel_file(uploaded_excel_file)
        st.dataframe(results, width=1080)
    else:
        st.write("Пожалуйста, загрузите Excel файл.")

# Can be deleted
if __name__ == '__main__':
    core = Core()
    asyncio.run(main())
