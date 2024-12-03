#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# 데이터 준비
df3 = pd.DataFrame({'2024.05.25. 성산2동 도착 통행량': [6304, 2876, 2623, 1501, 1155, 1152, 1057, 1046, 833, 828],
                    '2024년 5월 토요일 성산2동 평균 도착 통행량': [394.5, 44.75, 455.5, 96.75, 74.25, 39, 124.25, 84, 187, 56.5]},
                   index=['서교동', '회현동', '상암동', '한강로동', '공덕동', '반포4동', '서강동', '신사1동', '신촌동', '신사2동'])

df4 = pd.DataFrame({'2024.05.26. 성산2동 도착 통행량': [5288, 2435, 1771, 1069, 977, 770, 720, 710, 662, 556],
                    '2024년 5월 일요일 성산2동 평균 도착 통행량': [342.25, 383.5, 44.75, 96.75, 74.25, 39, 100.75, 84, 183.5, 90]},
                   index=['서교동', '상암동', '회현동', '한강로동', '공덕동', '반포4동', '서강동', '신사1동', '신촌동', '증산동'])

df5 = pd.DataFrame({'2024.08.03. 성산2동 도착 통행량': [8240, 3143, 2031, 1608, 1424, 1373, 1091, 1087, 811, 794],
                    '2024년 8월 토요일 성산2동 평균 도착 통행량': [394, 443.8, 145, 114.2, 122.4, 193.4, 150.4, 154.8, 198.8, 185.2]},
                   index=['서교동', '상암동', '회현동', '한강로동', '서강동', '공덕동', '여의동', '대흥동', '반포4동', '신촌동'])

df1 = pd.DataFrame({'2024.10.05. 여의동 도착 통행량': [6114, 5153, 4570, 4132, 2895, 2869, 2771, 2693, 2662, 2640],
                    '2024년 10월 토요일 여의동 평균 도착 통행량': [428.5, 243.5, 212.75, 168.75, 295, 258, 371.75, 159.25, 191.5, 336]},
                   index=['서교동', '역삼1동', '반포4동', '화곡1동', '노량진1동', '영등포본동', '한강로동', '사직동', '목1동', '당산2동'])

df2 = pd.DataFrame({'2024.10.26. 서교동 도착 통행량': [5979, 5255, 4609, 4391, 3297, 2955, 2884, 2665, 2563, 2527],
                    '2024년 10월 토요일 서교동 평균 도착 통행량': [297.5, 599.5, 1129, 413.75, 180, 152, 368.25, 439.5, 140, 172.75]},
                   index=['명동', '대흥동', '신촌동', '성산2동', '회현동', '을지로동', '종로1,2,3,4가동', '여의동', '반포4동', '소공동'])

# 그래프 생성 함수
def create_graph(df, title):
    melted_df = df.reset_index().melt(
        id_vars='index',
        var_name='날짜',
        value_name='통행량'
    )
    fig = px.bar(
        melted_df,
        x='index',
        y='통행량',
        color='날짜',
        barmode='group',
        title=title,
        labels={'index': '출발 행정동', '통행량': '통행량'}
    )
    fig.update_layout(
        xaxis_title="출발 행정동",
        yaxis_title="통행량",
        legend_title="날짜",
        xaxis_tickangle=45
    )
    return fig

# 그래프 제목과 데이터 연결
graphs = {
    "임영웅 콘서트(토요일) 통행량 비교": create_graph(df3, "임영웅 콘서트(토요일) 통행량 비교"),
    "임영웅 콘서트(일요일) 통행량 비교": create_graph(df4, "임영웅 콘서트(일요일) 통행량 비교"),
    "쿠팡 플레이 시리즈 통행량 비교": create_graph(df5, "쿠팡 플레이 시리즈 통행량 비교"),
    "서울세계불꽃축제 기간 통행량 비교": create_graph(df1, "서울세계불꽃축제 기간 통행량 비교"),
    "할로윈 전 주 토요일 서교동(홍대) 통행량 비교": create_graph(df2, "할로윈 전 주 토요일 서교동(홍대) 통행량 비교")
}

# 대시보드 생성
app = Dash(__name__)

app.layout = html.Div([
    html.H1("통행량 비교 대시보드", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='graph-title-selector',
        options=[{'label': title, 'value': title} for title in graphs.keys()],
        value=list(graphs.keys())[0],
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Div(id='selected-title', style={'textAlign': 'center', 'fontSize': '24px', 'margin': '20px 0', 'fontWeight': 'bold'}),
    dcc.Graph(
        id='bar-chart',
        style={'height': '800px'}
    )
])

@app.callback(
    [Output('bar-chart', 'figure'), Output('selected-title', 'children')],
    [Input('graph-title-selector', 'value')]
)
def update_graph(selected_title):
    return graphs[selected_title], selected_title

# 대시보드 실행
if __name__ == '__main__':
    app.run_server(debug=True)

