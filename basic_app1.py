import streamlit as st
import pandas as pd
# 제목 표시
st.title("내 첫 스트림릿 앱~~")

st.header("간단한 계산기 🧮")
num1 = st.number_input("첫 번째 숫자", value=0)
num2 = st.number_input("두 번째 숫자", value=0)

# 연산 선택
operation = st.selectbox("연산을 선택하세요.",["더하기", "빼기", "곱하기", "나누기"])
if st.button("계산하기"):
    # pass
    if operation == "더하기":
        result = num1 + num2
    elif operation == "빼기":
        result = num1 - num2
    elif operation == "곱하기":
        result = num1 * num2
    elif operation == "나누기":
        if num2 !=0:
            result = num1 / num2
        else:
            result = "0으로 나눌 수 없습니다."
    st.success(f"결과: {result}")



st.markdown("---")  # 구분선 추가!

st.header("데이터 표시 학습")
df = pd.DataFrame({
    '이름': ["철수", "영희", "민수"],
    '나이': [25, 30, 35]
})

# 차트 그리기
st.line_chart(df['나이'])

# 표로 보여주기
st.dataframe(df)

st.markdown("---")  # 구분선 추가!


# 텍스트 표시
st.header("안녕 스트림릿은 처음이지")
st.subheader("안녕 스트림릿은 처음이지")
st.text("안녕 스트림릿은 처음이지")
st.write("안녕 스트림릿은 처음이지")

# 사용자 이름 입력 받기
name = st.text_input("이름을 입력하세요.")

# 버튼 만들기
if st.button("인사하기"):
    st.write(f"안녕하세요. {name}님")

# 입력받기
text = st.text_input("텍스트를 입력하세요")
number = st.number_input("숫자를 입력하세요.")

# 슬라이더
st.slider("나이를 선택하세요", 0, 100, 25)

# 선택상자
st.selectbox("좋아하는 색은?", ["빨강", "파랑", "초록"])

# 체크박스
if st.checkbox("동의합니까?"):
    st.write("동의하셨습니다.")