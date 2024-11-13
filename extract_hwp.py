import pyhwp

hwp = pyhwp.HWPReader('인천대수강신청편람.hwp')

text = hwp.extract_text()

print(text)