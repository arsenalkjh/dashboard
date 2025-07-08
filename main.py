import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


df_test = pd.read_csv('./data/test_group.csv',delimiter=";")
df_control = pd.read_csv('./data/control_group.csv',delimiter=";")

df = pd.concat([df_test, df_control], ignore_index=True)

df.rename(columns={
    "Spend [USD]": "지출 금액",
    "# of Impressions": "노출수",
    "Reach": "도달한 사람 수",
    "# of Website Clicks": "클릭수",
    "# of Searches": "검색수",
    "# of View Content": "조회수",
    "# of Add to Cart": "장바구니 담기 수",
    "# of Purchase": "구매수",
    "Campaign Name":"캠페인"
}, inplace=True)

df.replace({"캠페인": {"Test Campaign": "Test Group", "Control Campaign": "Control Group"}}, inplace=True)

df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")

df = df.dropna()
df['클릭율'] = df['클릭수'] / df['노출수']
df['구매전환율'] = df['구매수'] / df['조회수']


st.set_page_config(
    page_title="마케팅 주요 지표 대시보드",
    layout="wide",
    initial_sidebar_state="collapsed"  
)

cols = st.columns([2,1])
cols1  = st.columns(3)
with cols[0]:
    option = st.selectbox(
        "옵션을 선택하세요",
        ("새로운 캠페인", "기존 캠페인", "전체")
    )
with cols[1]:
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;text-align:center;margin:10px;">
            <h4 style="margin:5px;">마케팅 총 지출 금액</h4>
            <h2 style="color:#4A90E2;">{df["지출 금액"].sum()} USD</h2>
        </div>
        """, unsafe_allow_html=True
    )

with cols1[0]:
    if option == "새로운 캠페인":
        fig1 = px.line(df[df["캠페인"] == "Test Group"], x="Date", y="노출수")

        fig1.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="새로운 캠페인 노출수"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        
        fig2 = px.line(df[df["캠페인"] == "Test Group"], x="Date", y="클릭수")
        
        fig2.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="새로운 캠페인 클릭수"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )

        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        
    elif option == "전체":
        fig1 = px.line(df, x="Date", y="노출수", color="캠페인")

        fig1.update_layout(
            showlegend=True,      # 범례 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="전체 캠페인 노출수"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        
        fig2 = px.line(df, x="Date", y="클릭수", color="캠페인")
        
        fig2.update_layout(
            showlegend=True,      # 범례 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="전체 캠페인 클릭수"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )

        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
    else:
        fig1 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="노출수")

        fig1.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="기존 캠페인 노출수"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        fig2 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="클릭수")
        
        fig2.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="기존 캠페인 클릭수"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )

        st.plotly_chart(fig1)
        st.plotly_chart(fig2)

with cols1[1]:
    if option == "새로운 캠페인":
        fig3 = px.line(df[df["캠페인"] == "Test Group"], x="Date", y="클릭율")
        
        fig3.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="새로운 캠페인 클릭율"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        
        fig4 = px.line(df[df["캠페인"] == "Test Group"], x="Date", y="구매전환율")
        
        fig4.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="새로운 캠페인 구매전환율"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
        
    elif option == "전체": 
        fig3 = px.line(df, x="Date", y="클릭율", color="캠페인")
        
        fig3.update_layout(
            showlegend=True,      # 범례 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="전체 캠페인 클릭율"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        
        fig4 = px.line(df, x="Date", y="구매전환율", color="캠페인")
        
        fig4.update_layout(
            showlegend=True,      # 범례 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="전체 캠페인 구매전환율"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
        
    else:
        fig3 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="클릭율")
        
        fig3.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="기존 캠페인 클릭율"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        
        fig4 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="구매전환율")
        fig4.update_layout(
            showlegend=False,      # 범례 아예 안 보이게
            xaxis=dict(
                visible=False      # x축 축과 눈금, 라벨 전부 숨기기
            ),
            yaxis=dict(
                visible=False      # y축 축과 눈금, 라벨 전부 숨기기
            ),
            title=dict(text="기존 캠페인 구매전환율"),    # 타이틀 빈 문자열로 제거
            plot_bgcolor='#f7f9fc',
            width=400,
            height=300
        )
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
with cols1[2]:
    selected_date = st.date_input(
        "날짜를 선택하세요", 
        value=df["Date"].min().date(), 
        min_value=df["Date"].min().date(), 
        max_value=df["Date"].max().date()
    )
    
    filtered_df = df[df["Date"].dt.date == selected_date]

    st.dataframe(filtered_df.iloc[:, 0:10].reset_index(drop=True), use_container_width=True)
    labels = ["노출수", "클릭수", "조회수", "장바구니 담기 수", "구매수"]
    values = [
        df["노출수"].sum(),
        df["클릭수"].sum(),
        df["조회수"].sum(),
        df["장바구니 담기 수"].sum(),
        df["구매수"].sum()
    ]

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    fig = go.Figure(go.Funnel(
        y=labels,
        x=values,
        marker={"color": colors}
    ))

    # 타이틀 추가
    fig.update_layout(
        title={
            'text': "기간 전체 단계별 전환 퍼널",
            'x': 0.35,  # 가운데 정렬
            'xanchor': 'center',
            'font': dict(size=20)
        }
    )

    st.plotly_chart(fig, use_container_width=True)
    
st.markdown("---")
fig5 = px.line(
    df,
    x="Date",
    y="구매수",
    color="캠페인",
    title='일 평균 구매수 추이',
    color_discrete_map={"Test Group": "steelblue", "Control Group": "orange"}
)

st.plotly_chart(fig5, use_container_width=True)