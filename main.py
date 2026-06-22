import streamlit as st
st.title("건강 데이터 탐험기")
st.write("이 앱은 의료 데이터를 쉽게 살펴보는 도구입니다")
name = st.text_input("이름을 입력하세요")

if name:
    st.write(f'반갑습니다. {name}님! 함께 시작해요')
else:
    st.info('위에 이름을 입력하면 인사를 드릴께요')

import streamlit as st
import pandas as pd
df = pd.read_csv(r'D:\ml_study\heart_failure.csv')
st.subheader(" 환자 데이터")
st.dataframe(df.head())
st.metric(label="전체 환자 수", value=f"{len(df)}명", delta="299건 수집")
avg = df['age'].mean()

st.metric("평균 나이", f"{avg:.1f}세")


import streamlit as st
import pandas as pd
df = pd.read_csv(r'D:\ml_study\heart_failure.csv')
# 슬라이더가 고른 나이가 age_max 로
age_max = st.slider("최대 나이", 40, 95, 70)
# 선택값으로 데이터를 걸러냄
filtered = df[df['age'] <= age_max]
st.write(f"{len(filtered)}명이 조건에 맞아요")
st.dataframe(filtered)

choice = st.selectbox("성별", ["남성", "여성"])
code = 1 if choice == "남성" else 0
result = df[df['sex'] == code]

# only_death = st.checkbox('사망 환자만 보기')
# if only 
st.write(f"{len(result)}명")
st.dataframe(result)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic' # Windows
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots()
ax.hist(df['age'], bins=20,
        color='#5BAFB8')
ax.set_xlabel("나이")
ax.set_ylabel("환자 수")

st.pyplot(fig)

counts = df['DEATH_EVENT'].value_counts()
#방법 A — 내장 차트
st.bar_chart(counts)
# 방법 B — matplotlib
fig, ax = plt.subplots()
ax.bar(["생존","사망"], counts, color=['#4CAF50', '#F44336'])
st.pyplot(fig)

import streamlit as st
import pandas as pd

# 왼쪽 사이드바에 필터를 둔다
st.sidebar.header(" 필터")
age = st.sidebar.slider("최대 나이", 40, 95, 70)
df = df[df['age'] <= age]
# 본문을 둘로 나눈다
c1, c2 = st.columns(2)
c1.metric("환자 수", len(df))
c2.metric("평균 나이", f"{df.age.mean():.0f}")

# st.sidebar.header("필터")
# age = st.sidebar.slider("최대 나이", 40, 95, 70)

# # 2. 필터링 (중요: 그래프를 그리기 전에 이 필터가 먼저 적용되어야 합니다)
# filtered_df = df[df['age'] <= age]

# # 3. 본문 구성 (지표 표시)
# c1, c2 = st.columns(2)
# c1.metric("환자 수", len(filtered_df))
# c2.metric("평균 나이", f"{filtered_df.age.mean():.0f}")

# # 4. 필터링된 데이터를 바탕으로 막대그래프 그리기
# st.subheader("사망 이벤트 분포 (필터 적용 결과)")

# # 필터링된 데이터에서 값 구하기
# counts = filtered_df['DEATH_EVENT'].value_counts()

# # 방법 B: Matplotlib 활용
# fig, ax = plt.subplots()
# ax.bar(["생존", "사망"], counts.reindex([0, 1], fill_value=0), color=['#4CAF50', '#F44336'])
# ax.set_title("사망 이벤트 분포")
# st.pyplot(fig)


# st.sidebar.header(" 필터")
# age = st.sidebar.slider("최대 나이", 40, 95, 70)
# df = df[df['age'] <= age]
tab1, tab2 = st.tabs(["표", "차트"])

with tab1:
    st.dataframe(df)
with tab2:
    fig, ax = plt.subplots()
    ax.hist(df['age'])
    st.pyplot()
    
# st.title(" 심부전 분석")
# st.write("👈 메뉴를 선택하세요")
# # pages/1_데이터.py
# import streamlit as st, pandas as pd
# st.title("📊 데이터")
# df = pd.read_csv("heart_failure.csv")
# st.dataframe(df)

# import streamlit as st
# def home():
#     st.title("🏠 홈")
# def data():
#     st.title("📊 데이터")
# pg = st.navigation([
#     st.Page(home, title="홈",
#             icon="🏠", default=True),
#     st.Page(data, title="데이터",
#             icon="📊"),
# ])
# pg.run()


@st.cache_data   # 이 줄이 핵심!
def load_data():
    return pd.read_csv("heart_failure.csv")
df = load_data()  # 처음 한 번만 실제 로딩