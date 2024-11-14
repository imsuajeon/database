import pandas as pd

# 절대 경로를 사용하여 파일 불러오기
file_path = r"C:\ummchickenpizzapasta\database\인천대_건물명.csv"
df = pd.read_csv(file_path)

# 데이터의 첫 몇 행을 출력
print(df.head())
