# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from scipy import stats

# st.set_page_config(page_title="심부전 분석", layout="wide")

# @st.cache_data
# def load_data():
#     df = pd.read_csv(r'D:\ml_study\heart_failure.csv')
#     df["사망여부"] = df["DEATH_EVENT"].map({0: "생존", 1: "사망"})
#     return df
# df = load_data()

# age_range = st.sidebar.slider("나이 범위", 40, 95, (40, 95))
# sex = st.sidebar.multiselect("성별", [1, 0], default=[1, 0])
# data = df[(df.age.between(*age_range)) & (df.sex.isin(sex))]

# # 핵심 지표 4개
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("환자 수", len(data))

# tab1, tab2, tab3 = st.tabs(
#     ["기술통계","가설검정","상관"])
# with tab1:
#     pick = st.selectbox("변수", ["age","ejection_fraction"])
#     if len(data) > 1:
#         fig, ax = plt.subplots()
#         sns.histplot(data=data, x=pick, hue="사망여부", kde=True, ax=ax)
#         st.pyplot(fig)
#         plt.clf()
#     else:
#         st.warning("선택한 조건에 해당하는 데이터가 너무 적어 그래프를 그릴 수 없습니다.")
#     fig, ax = plt.subplots()
#     st.write(f"현재 선택된 데이터 개수: {len(data)}")
#     st.write(data.head())
#     sns.histplot(data=data, x=pick,
#                  hue="DEATH_EVENT", kde=True, ax=ax)
#     st.pyplot(fig)

# var = pick        
# g_alive = data[data.DEATH_EVENT==0][var]
# g_dead  = data[data.DEATH_EVENT==1][var]
# t, p_val = stats.ttest_ind(
#     g_alive, g_dead, equal_var=False)
# st.metric("p-value", f"{p_val:.4f}")
# if p_val < 0.05:
#     st.success("차이가 유의합니다")
# else:
#     st.info("유의하지 않습니다")

# # 교차표(분할표) 만들    
# ctab = pd.crosstab(
#     data['high_blood_pressure'],
#     data['DEATH_EVENT'])
# st.dataframe(ctab)

# # 카이제곱 검정
# chi2, p, dof, _ = \
#     stats.chi2_contingency(ctab)
# st.metric("p-value", f"{p:.4f}")

# # 상관 히트맵
# cols = ["age","ejection_fraction",
#         "serum_creatinine","time","DEATH_EVENT"]
# corr = data[cols].corr()

# fig, ax = plt.subplots()
# sns.heatmap(corr, annot=True,
#             cmap="RdYlGn_r", center=0, ax=ax)
# st.pyplot(fig)


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# 1. 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="심부전 분석", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv(r'D:\ml_study\heart_failure.csv')
    df["사망여부"] = df["DEATH_EVENT"].map({0: "생존", 1: "사망"})
    return df

df = load_data()

# 사이드바 설정
age_range = st.sidebar.slider("나이 범위", 40, 95, (40, 95))
# 성별 매핑 (UI는 남/여, 데이터는 1/0)
gender_map = {'남': 1, '여': 0}
selected_labels = st.sidebar.multiselect("성별", list(gender_map.keys()), default=['남', '여'])
selected_values = [gender_map[label] for label in selected_labels]

# 데이터 필터링
data = df[(df.age.between(*age_range)) & (df.sex.isin(selected_values))]

st.title("심부전 데이터 분석 대시보드")
c1, c2, c3, c4 = st.columns(4)
c1.metric("환자 수", len(data))

tab1, tab2, tab3 = st.tabs(["기술통계", "가설검정", "상관"])

with tab1:
    pick = st.selectbox("분석할 변수", ["age", "ejection_fraction"])
    if len(data) > 1:
        fig, ax = plt.subplots()
        sns.histplot(data=data, x=pick, hue="사망여부", kde=True, ax=ax)
        st.pyplot(fig)
        plt.clf()
    else:
        st.warning("데이터가 부족하여 히스토그램을 그릴 수 없습니다.")

with tab2:
    st.subheader("평균 차이 검정 (t-test)")
    if len(data[data.DEATH_EVENT == 0]) > 1 and len(data[data.DEATH_EVENT == 1]) > 1:
        g_alive = data[data.DEATH_EVENT == 0][pick]
        g_dead = data[data.DEATH_EVENT == 1][pick]
        t, p_val = stats.ttest_ind(g_alive, g_dead, equal_var=False)
        st.metric(f"{pick} p-value", f"{p_val:.4f}")
    else:
        st.info("비교할 집단 중 하나가 너무 적습니다.")
        
    st.subheader("교차표 및 카이제곱 검정")
    ctab = pd.crosstab(data['high_blood_pressure'], data['DEATH_EVENT'])
    st.dataframe(ctab)
    chi2, p, dof, _ = stats.chi2_contingency(ctab)
    st.metric("카이제곱 p-value", f"{p:.4f}")

with tab3:
    st.subheader("변수 간 상관관계 히트맵")
    cols = ["age", "ejection_fraction", "serum_creatinine", "time", "DEATH_EVENT"]
    corr = data[cols].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="RdYlGn_r", center=0, ax=ax)
    st.pyplot(fig)
    plt.clf()