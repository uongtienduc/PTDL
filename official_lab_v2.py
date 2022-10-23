# Học thêm tại: https://dash.plotly.com/

# Run this app with `python app.py` and

# visit http://127.0.0.1:8050/ in your web browser.

# BẤM CTRL '+' C ĐỂ TẮT APP ĐANG CHẠY

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./iuh-19500031-firebase-adminsdk-dihvv-44c3a67206.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20005201').where(u'DEALSIZE', u'==', 'Large').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)

app.title = "Finance Data Analysis"
figDoanhSoBanHang = px.histogram(df, x="YEAR_ID", y="SALES",
                                 barmode="group", color="YEAR_ID", title='DOANH SỐ BÁN HÀNG THEO NĂM', histfunc="sum",
                                 labels={'YEAR_ID': 'Từ năm 2003, 2004 và 2005', 'QTR_ID': 'Quý trong năm', 'Sum': 'Tổng doanh số'})
figTiLeGopVon = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
                            color='CATEGORY',
                            title='TỈ LỆ ĐÓNG GÓP CỦA DOANH SỐ THEO TỪNG DANH MỤC TRONG TỪNG NĂM')
figLoiNhuan = px.line(df, x='YEAR_ID', y='SALES',
                      labels={'YEAR_ID': 'Năm', 'SumSaleQTRYEAR': 'Doanh số'},
                      title='USER SIGNUPS')
figChart3 = px.line(df.sort_values(['ORDERDATE']), x='ORDERDATE', y='SALES',
                    labels={'YEAR_ID': 'Năm', 'SumSaleQTRYEAR': 'Doanh số'},
                    title='USER SIGNUPS')

figSoLuongHoaDon = px.sunburst(df, path=['YEAR_ID', 'QTR_ID'], values='QUANTITYORDERED',
                               color='QUANTITYORDERED',
                               labels={'parent': 'Năm', 'labels': 'Quý',
                                       'QUANTITYORDERED': 'Số lượng sản phẩm'},
                               title='HIT BY MARKETING STRATEGY')
# Tổng doanh số
totalRevenue = df['SALES'].sum()
# Lợi nhuận
variableCost = (df['PRICEEACH']*df['QUANTITYORDERED']).sum()
profit = totalRevenue - variableCost
# Top doanh số
maxSales = df['SALES'].max()

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(
                    children="Xây dựng danh mục sản phẩm tiềm năng", className="header-title"
                ),
                html.H3(
                    children="IUH-DHHTTT16B-20068371-Võ Phương Nam", className="header-title"
                )
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H2(
                            children="Doanh số sale",
                            className="title"
                        ),
                        html.P(
                            children=totalRevenue
                        )
                    ], className="div1"
                ),
                html.Div(
                    children=[
                        html.H2(
                            children="Lợi nhuận",
                            className="title"
                        ),
                        html.P(
                            children=profit
                        )
                    ], className="div1"
                ),
                html.Div(
                    children=[
                        html.H2(
                            children="Top doanh số",
                            className="title"
                        ),
                        html.P(
                            children=maxSales
                        )
                    ], className="div1"
                ),
                html.Div(
                    children=[
                        html.H2(
                            children="Top lợi nhuận",
                            className="title"
                        ),
                        html.P(
                            children="66.55"
                        )
                    ], className="div1"
                )
            ],
            className="header-dashboard"
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='soluong-graph',
                        figure=figDoanhSoBanHang),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                        id='doanhso-graph',
                        figure=figTiLeGopVon),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                        id='soluongdonhang-graph',
                        figure=figLoiNhuan),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                        id='soluong-graph-clone',
                        figure=figTiLeGopVon),
                    className="card"
                )
            ], className="wrapper")
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=1111)