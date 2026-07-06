import pandas as pd

def extract_excel_text(file):

    df = pd.read_excel(file)

    return df.to_string(index=False)