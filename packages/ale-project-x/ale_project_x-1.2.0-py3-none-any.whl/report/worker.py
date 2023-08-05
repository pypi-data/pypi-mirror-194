from openpyxl import Workbook, load_workbook
import pandas as pd
import os
import report

DASH_SEP = chr(8211) #the separator in excel file is an en dash – (8211) not a usual dash - (45) but the dash I used to know turn out to be a hyphen-minus
AMOUNT_IN_VND_HEADER = "amount in vnd"
TRANSACTION_DATE_HEADER = "Ngày giao dịch"
CUSTOMER_ACCOUNT_NUMBER_HEADER = "Số tài khoản khách hàng"
TRANSACTION_NO_HEADER = "Lần giao dịch"
TRANSACTION_TYPE_HEADER = "Loại giao dịch"
AMOUNT_HEADER = "Tổng số tiền"
CURRENCY_HEADER = "Loại tiền"
REMARK_HEADER = "Ghi chú"
SOURCE_ACCOUNT_HEADER = "Tài khoản nguồn"
SOURCE_CUSTOMER_HEADER = "Tên chủ tài khoản nguồn"
DESTINATION_ACCOUNT_HEADER = "Tài khoản đích"
DESTINATION_CUSTOMER_HEADER = "Tên chủ tài khoản đích"
USD_TO_VND = 23500
EUR_TO_VND = 25500
CURRENCY_USD = "USD"
CURRENCY_VND = "VND"
CURRENCY_EUR = "EUR"
TOTAL_INCOME = "(A)Doanh thu số tiền về"
INCOME_FROM_SALE = "+ Trực tiếp từ HĐKD (B)"
INCOME_FROM_DEPOSIT = "+ Nộp tiền mặt (C)"
INCOME_FROM_CAPITAL_TRANSFER = "+ Điều vốn (D)"
OTHER = "+ Khác (E)"
EXCHANGE_RATE = {
    CURRENCY_USD: USD_TO_VND,
    CURRENCY_VND: 1,
    CURRENCY_EUR: EUR_TO_VND
}

def run(input_folder_path, output_folder_path):
    
    dtf_total = _read_data_from_folder(input_folder_path)

    dtf_total = _enrich_data(dtf_total)

    dtf_total = _categorize_data(dtf_total)
    print(dtf_total)

    group_df = dtf_total.groupby(['year','category']).sum(AMOUNT_IN_VND_HEADER)
    print(type(group_df))
    all_years = set(group_df.index.get_level_values("year"))
    
    OUTPUT_ITEM_LABEL = "Chỉ tiêu (trđ)"

    outputDict = {
        OUTPUT_ITEM_LABEL: [TOTAL_INCOME, INCOME_FROM_SALE, INCOME_FROM_DEPOSIT, INCOME_FROM_CAPITAL_TRANSFER, OTHER]
    }
    for year in all_years:
        _B = group_df.loc[(year, 'B'), AMOUNT_IN_VND_HEADER]
        _C = group_df.loc[(year, 'C'), AMOUNT_IN_VND_HEADER]
        _D = group_df.loc[(year, 'D'), AMOUNT_IN_VND_HEADER]
        _A = _B + _C + _D
        _E = group_df.loc[(year, 'E'), AMOUNT_IN_VND_HEADER]
        outputDict[year] = [_A, _B, _C, _D, _E]

    outputDf = pd.DataFrame.from_dict(outputDict)

    if (not os.path.isdir(output_folder_path)): os.makedirs(output_folder_path)
    output_file_path = os.path.join(output_folder_path,"output.xlsx")
    with pd.ExcelWriter(output_file_path) as excel_writer:
        dtf_total.to_excel(excel_writer,"Sheet1",index=False)
        outputDf.to_excel(excel_writer, "Sheet2",index=False)
    
    abs_output_file_path = os.path.abspath(output_file_path)
    print(f'File has been created in {abs_output_file_path}')

def _read_data_from_folder(input_folder_path):
    file_names = [f for f in os.listdir(input_folder_path) if f.endswith(".xlsx")]
    print(file_names)
    df_list = [_df_from_file_path(os.path.join(input_folder_path, file_name)) for file_name in file_names]

    dtf_total = pd.concat(df_list)
    dtf_total.reset_index(inplace=True)

    return dtf_total

def _clean_data(df: pd.DataFrame):
    df_out = df.copy(deep=True)
    df_out[DESTINATION_CUSTOMER_HEADER].fillna("",inplace=True)

    return df_out

def _read_and_clean_data(input_folder_path):
    df = _read_data_from_folder(input_folder_path)
    df = _clean_data(df)

    return df

def _df_from_file_path(file_path) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    df = df.iloc[:-1]

    return df

def _enrich_data(df: pd.DataFrame):
    df_out = df.copy(deep=True)
    df_out[AMOUNT_IN_VND_HEADER] = df_out.apply(lambda row: round(float(row[AMOUNT_HEADER])*EXCHANGE_RATE[row[CURRENCY_HEADER]]/1000000,3), axis=1)

    return df_out

def _categorize_data(df: pd.DataFrame):
    df_out = df.copy(deep=True)
    customerName = df_out[SOURCE_CUSTOMER_HEADER][0:1][0]
    keywords = customerName.split(" ")
    keywords = keywords[-2:]
    keywords = " ".join(keywords)
    df_out['sub_category'] = "B"
    df_out['year'] = df_out.apply(lambda row: str(row[TRANSACTION_DATE_HEADER].year), axis=1)
    df_out[DESTINATION_CUSTOMER_HEADER].fillna("",inplace=True)
    
    df_out = _apply_E1(df_out)
    df_out = _apply_E2(df_out)
    df_out = _apply_E3(df_out)
    df_out = _apply_E4(df_out)
    df_out = _apply_E5(df_out)

    df_out = _apply_D1(df_out)
    df_out = _apply_D2(df_out)

    df_out = _apply_C1(df_out)

    df_out['category'] = df_out['sub_category'].str[:1]
    
    return df_out

def _contain_keywords(value, keywords):
    first_text_before_seperator = value.split(DASH_SEP)[0].strip()
    words_in_text = first_text_before_seperator.split(" ")
    last_words_in_text = words_in_text[-2:]
    text_to_be_compared = " ".join(last_words_in_text)

    return text_to_be_compared == keywords

def _apply_E1(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    cond_1 = df_out[DESTINATION_CUSTOMER_HEADER].apply(lambda value: "TAI KHOAN TRUNG GIAN" in str(value).upper())
    cond_2 = df_out[REMARK_HEADER].apply(lambda value: "VFX" in str(value).upper())
    cond_3 = df_out[REMARK_HEADER].apply(lambda value: "TAT TOAN" in str(value).upper())
    final_cond = cond_1 & (cond_2 | cond_3)
    df_out.loc[final_cond, 'sub_category'] = 'E1'
    

    return df_out

def _apply_E2(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    cond_1 = df_out[DESTINATION_CUSTOMER_HEADER].apply(lambda value: "BAO HIEM XA HOI" in str(value).upper())

    final_cond = cond_1

    df_out.loc[final_cond, 'sub_category'] = 'E2'
    
    return df_out

def _apply_E3(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    cond_1 = df_out[DESTINATION_CUSTOMER_HEADER].apply(lambda value: "THUE GIA TRI" in str(value).upper())

    final_cond = cond_1

    df_out.loc[final_cond, 'sub_category'] = 'E3'
    
    return df_out

def _apply_E4(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    cond_1 = df_out[REMARK_HEADER].apply(lambda value: "HUY HOP DONG" in str(value).upper())
    cond_2 = df_out[REMARK_HEADER].apply(lambda value: "HOAN UNG" in str(value).upper())
    cond_3 = df_out[REMARK_HEADER].apply(lambda value: "HOAN TAM UNG" in str(value).upper())
    cond_4 = df_out[REMARK_HEADER].apply(lambda value: "HOAN TIEN UNG" in str(value).upper())

    final_cond = cond_1 | cond_2 | cond_3 | cond_4

    df_out.loc[final_cond, 'sub_category'] = 'E4'
    
    return df_out

def _apply_E5(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    cond_1 = df_out[DESTINATION_CUSTOMER_HEADER].apply(lambda value: len(str(value).upper().strip()) == 0)
    final_cond = cond_1

    df_out.loc[final_cond, 'sub_category'] = 'E5'
    
    return df_out

def _apply_D1(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    customerName = df_out[SOURCE_CUSTOMER_HEADER][0:1][0]
    keywords = customerName.split(" ")
    keywords = keywords[-2:]
    keywords = " ".join(keywords)
    cond_1 = df_out[CURRENCY_HEADER] == CURRENCY_VND
    cond_2 = df_out[DESTINATION_CUSTOMER_HEADER].apply(lambda value: _contain_keywords(value, keywords))
    final_cond = cond_1 & cond_2

    df_out.loc[final_cond, 'sub_category'] = 'D1'
    
    return df_out

def _apply_D2(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    customerName = df_out[SOURCE_CUSTOMER_HEADER][0:1][0]
    keywords = customerName.split(" ")
    keywords = keywords[-2:]
    keywords = " ".join(keywords)
    cond_1 = df_out[CURRENCY_HEADER] != CURRENCY_VND
    cond_2 = df_out[DESTINATION_CUSTOMER_HEADER].apply(lambda value: _contain_keywords(value, keywords))
    cond_3 = df_out[REMARK_HEADER].apply(lambda value: "CHUYEN TIEN" in str(value).upper())
    cond_4 = df_out[REMARK_HEADER].apply(lambda value: "DIEU VON" in str(value).upper()) 
    cond_5 = df_out[REMARK_HEADER].apply(lambda value: "CHUYEN VON" in str(value).upper())

    final_cond = cond_1 & cond_2 & (cond_3 | cond_4 | cond_5)

    df_out.loc[final_cond, 'sub_category'] = 'D2'
    
    return df_out

def _apply_C1(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy(deep=True)
    
    cond_1 = df_out[REMARK_HEADER].apply(lambda value: "NT" in str(value).upper())
    cond_2 = df_out[REMARK_HEADER].apply(lambda value: "NOP TIEN" in str(value).upper()) 
    cond_3 = df_out[REMARK_HEADER].apply(lambda value: "TIEN MAT" in str(value).upper())

    final_cond = cond_1 | cond_2 | cond_3

    df_out.loc[final_cond, 'sub_category'] = 'C1'
    
    return df_out