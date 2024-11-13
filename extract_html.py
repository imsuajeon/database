from bs4 import BeautifulSoup

# HTML 파일 열기
with open(r'C:\Users\cele9\Umchi.ckenpizzapasta\incheon.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, 'lxml')

# 예시: 모든 <div> 태그에서 텍스트 추출
div_tags = soup.find_all('div')
extracted_data = []
for div_tag in div_tags:
    # div 태그 내부의 텍스트만 추출
    extracted_data.append(div_tag.get_text())

print(extracted_data)  # 추출한 데이터 확인