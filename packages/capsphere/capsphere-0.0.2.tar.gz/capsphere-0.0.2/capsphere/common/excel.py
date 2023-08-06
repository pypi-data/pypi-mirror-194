import pandas as pd


def create_worksheet(wb_name: str, data: list[dict]) -> None:
    first_row = 7
    first_col = 1
    last_col = 6

    average_rcf = generate_average_rcf(data)

    writer = pd.ExcelWriter(f'{wb_name}.xlsx', engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Sheet1')
    writer.sheets['Sheet1'] = worksheet
    worksheet.write('A4', 'Reconstructed Cash Flows')
    worksheet.write('A5', '*Average of 6 months bank statements')

    try:
        for output in data:
            index = [d['month'] for d in output]
            df = pd.DataFrame({k: [d[k] for d in output] for k in output[0].keys() if k != 'month'}, index=index)
            df_agg = df.agg(['sum', 'mean'])
            df_agg.index = ['Total', 'Average']
            table = pd.concat([df, df_agg])
            column_settings = [{'header': column} for column in table.columns]
            worksheet.add_table(first_row, first_col, first_row + 6, last_col, {'columns': column_settings})

            table.to_excel(writer, sheet_name='Sheet1', startrow=first_row, startcol=0)
            first_row += 10

        worksheet.write('A' + str(first_row), 'Reconstructed Cash Flow based on 6 months Bank Statements')

        average_rcf.to_excel(writer, sheet_name='Sheet1', startrow=first_row + 2, startcol=0)
        column_settings = [{'header': column} for column in average_rcf.columns]
        worksheet.add_table(first_row+2, first_col, first_row + 6, last_col, {'columns': column_settings})

    except Exception as err:
        raise err
    finally:
        writer.close()


def generate_average_rcf(rcf_list: list[dict]) -> pd.DataFrame:
    df_list = []

    for inner_list in rcf_list:
        inner_df_list = []
        for d in inner_list:
            df = pd.DataFrame.from_dict(d, orient='index').T
            inner_df_list.append(df)
        inner_result_df = pd.concat(inner_df_list)
        df_list.append(inner_result_df)

    average_rcf = pd.concat(df_list, axis=0, ignore_index=True)

    average_rcf = average_rcf.groupby('month').sum()

    total = average_rcf.sum().rename('Total')
    average = average_rcf.mean().rename('Average')
    average_rcf = average_rcf.T
    average_rcf = pd.concat((average_rcf, total), axis=1)
    average_rcf = pd.concat((average_rcf, average), axis=1)
    average_rcf = average_rcf.T
    return average_rcf
