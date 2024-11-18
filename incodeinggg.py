import pandas as pd

# CSV 파일 읽기 (원래 인코딩 설정)
df = pd.read_csv("C:\Users\suaje\OneDrive\Desktop\편람.csv", encoding="CP949")  # 또는 'EUC-KR'

# UTF-8로 저장
df.to_csv("C:\Users\suaje\OneDrive\Desktop\편람.csv", encoding="utf-8", index=False)
