import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest


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
        ("전체","새로운 캠페인", "기존 캠페인")
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
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="새로운 캠페인 노출수"),
            width=400,
            height=300
        )
        
        fig2 = px.line(df[df["캠페인"] == "Test Group"], x="Date", y="클릭수")
        
        fig2.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="새로운 캠페인 클릭수"), 
            width=400,
            height=300
        )

        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        
    elif option == "전체":
        fig1 = px.line(df, x="Date", y="노출수", color="캠페인")

        fig1.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="전체 캠페인 노출수"),
            width=400,
            height=300
        )

        
        fig2 = px.line(df, x="Date", y="클릭수", color="캠페인")
        
        fig2.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="전체 캠페인 클릭수"),
            width=400,
            height=300
        )

        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
    else:
        fig1 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="노출수")

        fig1.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="기존 캠페인 노출수"),
            width=400,
            height=300
        )
        fig2 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="클릭수")
        
        fig2.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="기존 캠페인 클릭수"),
            width=400,
            height=300
        )

        st.plotly_chart(fig1)
        st.plotly_chart(fig2)

with cols1[1]:
    if option == "새로운 캠페인":
        fig3 = px.line(df[df["캠페인"] == "Test Group"], x="Date", y="클릭율")
        
        fig3.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="새로운 캠페인 클릭율"),
            width=400,
            height=300
        )
        
        fig4 = px.line(df[df["캠페인"] == "Test Group"], x="Date", y="구매전환율")
        
        fig4.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="새로운 캠페인 구매전환율"),
            width=400,
            height=300
        )
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
        
    elif option == "전체": 
        fig3 = px.line(df, x="Date", y="클릭율", color="캠페인")
        
        fig3.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="전체 캠페인 클릭율"),
            width=400,
            height=300
        )
        
        fig4 = px.line(df, x="Date", y="구매전환율", color="캠페인")
        
        fig4.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="전체 캠페인 구매전환율"),
            width=400,
            height=300
        )
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
        
    else:
        fig3 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="클릭율")
        
        fig3.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="기존 캠페인 클릭율"),
            width=400,
            height=300
        )
        
        fig4 = px.line(df[df["캠페인"] == "Control Group"], x="Date", y="구매전환율")
        fig4.update_layout(
            xaxis=dict(
                title='',        # 축 제목 없애기
                showline=False,  # 축 선 숨기기
                showticklabels=True,  # 눈금 라벨은 보이기
                ticks='outside'       # 눈금선 모양(선 밖에 표시)
            ),
            yaxis=dict(
                visible=False      # y축은 완전히 숨기기 (필요하면 조절)
            ),
            plot_bgcolor='#f7f9fc',
            title=dict(text="기존 캠페인 구매전환율"),
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
st.title("A/B 테스트 대시보드")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;text-align:center;margin:10px;">
            <h4 style="margin:5px;">실험명</h4>
            <h2 style="color:#4A90E2;">마케팅 캠페인 성과 비교</h2>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;text-align:center;margin:10px;">
            <h4 style="margin:5px;">실험 기간</h4>
            <h2 style="color:#4A90E2;font-size:30px;">{df['Date'].min().date()} ~ {df['Date'].max().date()}</h2>
        </div>
        """, unsafe_allow_html=True
    )
    
with col3:
    selected_option = st.selectbox(
        "목표 지표를 선택하세요",
        options=["CTR(클릭율)", "CR(구매전환율)"]
    )
    
mid_cols = st.columns(3)
if selected_option == "CTR(클릭율)":
    campaign_counts = df['캠페인'].value_counts().reset_index()
    campaign_counts.columns = ['캠페인', '횟수']
    with mid_cols[0]:
        fig = px.pie(
        campaign_counts,
        names='캠페인',
        values='횟수',
        color='캠페인',
        color_discrete_map={
            'Test Group': '#FFA07A',
            'Control Group': '#87CEFA'
        },
        title="Test vs Control 그룹 비율"
        )
        st.plotly_chart(fig, use_container_width=True)
    with mid_cols[1]:
        proportion_df1 = (df.groupby('캠페인')['클릭수'].sum() / df.groupby('캠페인')['노출수'].sum()).reset_index(name='클릭율')

        fig = px.bar(
            proportion_df1,
            x='캠페인',
            y='클릭율',
            color='캠페인',
            color_discrete_map={
                'Test Group': '#FFA07A',
                'Control Group': '#87CEFA'
            },
            title="캠페인별 클릭율"
        )
        st.plotly_chart(fig, use_container_width=True)
    with mid_cols[2]:
        fig = px.box(
            df,
            x='캠페인',
            y='클릭율',
            color='캠페인',
            color_discrete_map={
                'Test Group': '#FFA07A',
                'Control Group': '#87CEFA'
            },
            title="캠페인별 클릭율 분포"
        )
        st.plotly_chart(fig, use_container_width=True)
    # 통계량 계산
    success_counts = df.groupby('캠페인')['클릭수'].sum().values
    trial_counts = df.groupby('캠페인')['노출수'].sum().values
    stat, p_value = proportions_ztest(count=success_counts, nobs=trial_counts)

    # 결과 메시지
    if p_value < 0.05:
        result_msg = "✅ <b style='color:green;'>통계적으로 유의미한 차이가 있습니다.</b>"
    else:
        result_msg = "⚠️ <b style='color:red;'>통계적으로 유의미한 차이가 없습니다.</b>"
    # 2개 컬럼으로 배치
    col1, col2 = st.columns(2)

    # t-통계량 & p-값
    with col1:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;text-align:center;margin:10px;">
                <h4>Z-통계량</h4>
                <h2 style="color:#4A90E2;">{stat:.4f}</h2>
                <h4>p-값</h4>
                <h2 style="color:#4A90E2;">{p_value:.4f}</h2>
            </div>
            """, unsafe_allow_html=True
        )

    # 결과 메시지
    with col2:
        st.markdown(
            f"""
            <div style="background-color:#ffffff;padding:20px;border-radius:10px;text-align:center;margin:10px;border:2px solid #e0e0e0;">
                <h4>검정 결과</h4>
                <p style="font-size:18px;">{result_msg}</p>
                <p style="font-size:14px;">통계적으로 유의미한 차이가 존재하더라도, 그 영향은 미비할 수 있습니다</p>
            </div>
            """, unsafe_allow_html=True
        )
else:
    campaign_counts = df['캠페인'].value_counts().reset_index()
    campaign_counts.columns = ['캠페인', '횟수']
    with mid_cols[0]:
        fig = px.pie(
        campaign_counts,
        names='캠페인',
        values='횟수',
        color='캠페인',
        color_discrete_map={
            'Test Group': '#FFA07A',
            'Control Group': '#87CEFA'
        },
        title="Test vs Control 그룹 비율"
        )
        st.plotly_chart(fig, use_container_width=True)
    with mid_cols[1]:
        proportion_df = (df.groupby('캠페인')['구매수'].sum() / df.groupby('캠페인')['조회수'].sum()).reset_index(name='구매전환율')
        fig = px.bar(
            proportion_df,
            x='캠페인',
            y='구매전환율',
            color='캠페인',
            color_discrete_map={
                'Test Group': '#FFA07A',
                'Control Group': '#87CEFA'
            },
            title="캠페인별 구매전환율"
        )
        st.plotly_chart(fig, use_container_width=True)

    with mid_cols[2]:
        fig = px.box(
            df,
            x='캠페인',
            y='구매전환율',
            color='캠페인',
            color_discrete_map={
                'Test Group': '#FFA07A',
                'Control Group': '#87CEFA'
            },
            title="캠페인별 구매전환율 분포"
        )
        st.plotly_chart(fig, use_container_width=True)
    # 통계량 계산
    success_counts_cr = df.groupby('캠페인')['구매수'].sum().values
    trial_counts_cr = df.groupby('캠페인')['조회수'].sum().values
    stat_cr, p_value_cr = proportions_ztest(count=success_counts_cr, nobs=trial_counts_cr)
    
    if p_value_cr < 0.05:
        result_msg = "✅ <b style='color:green;'>통계적으로 유의미한 차이가 있습니다.</b>"
    else:
        result_msg = "⚠️ <b style='color:red;'>통계적으로 유의미한 차이가 없습니다.</b>"

    # 2개 컬럼으로 배치
    col1, col2 = st.columns(2)

    # t-통계량 & p-값
    with col1:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;text-align:center;margin:10px;">
                <h4>Z-통계량</h4>
                <h2 style="color:#4A90E2;">{stat_cr}</h2>
                <h4>p-값</h4>
                <h2 style="color:#4A90E2;">{p_value_cr}</h2>
            </div>
            """, unsafe_allow_html=True
        )
    # 결과 메시지
    with col2:
        st.markdown(
            f"""
            <div style="background-color:#ffffff;padding:20px;border-radius:10px;text-align:center;margin:10px;border:2px solid #e0e0e0;">
                <h4>검정 결과</h4>
                <p style="font-size:18px;">{result_msg}</p>
                <p style="font-size:14px;">통계적으로 유의미한 차이가 존재하더라도, 그 영향은 미비할 수 있습니다</p>
            </div>
            """, unsafe_allow_html=True
        )  
