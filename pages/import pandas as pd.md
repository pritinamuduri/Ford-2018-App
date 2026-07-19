import pandas as pd
file_id ='file_id ='1gqU4G-UcC1UM185WxAbidXaT5XYFaLVx'
url = f'https://drive.google.com/uc?id={file_id}'
df = pd.read_csv(f'https://drive.google.com/uc?id={file_id}')
print(df.columns.tolist())