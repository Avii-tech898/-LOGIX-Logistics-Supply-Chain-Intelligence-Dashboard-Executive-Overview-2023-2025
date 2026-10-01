import os
from pathlib import Path
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title='LOGIX | Logistics Intelligence', page_icon='🚚', layout='wide')

st.markdown('''<style>
:root{--navy:#073B4C;--teal:#0F766E;--teal2:#14B8A6;--blue:#2563EB;--bg:#F4F7F9;--text:#0F172A;--muted:#64748B;--line:#E2E8F0}
.stApp{background:var(--bg)}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#06384A 0%,#0B5F61 100%);border-right:1px solid rgba(255,255,255,.08)}
[data-testid="stSidebar"] *{color:#fff!important}
.block-container{padding-top:1.1rem;padding-bottom:1.5rem;max-width:1600px}
.logix-header{position:relative;overflow:hidden;min-height:185px;background:linear-gradient(90deg,rgba(255,255,255,.97) 0%,rgba(255,255,255,.91) 45%,rgba(231,247,244,.62) 100%),url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNjAwIiBoZWlnaHQ9IjQyMCI+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImciIHgxPSIwIiB5MT0iMCIgeDI9IjEiIHkyPSIxIj4KPHN0b3Agc3RvcC1jb2xvcj0iI0VBRjhGNSIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI0VBRjNGRiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8cGF0dGVybiBpZD0iZ3JpZCIgd2lkdGg9IjgwIiBoZWlnaHQ9IjgwIiBwYXR0ZXJuVW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHBhdGggZD0iTTAgNDBIODBNNDAgMFY4MCIgc3Ryb2tlPSIjMEY3NjZFIiBzdHJva2Utb3BhY2l0eT0iLjA0NSIvPgo8Y2lyY2xlIGN4PSI0MCIgY3k9IjQwIiByPSIyIiBmaWxsPSIjMEY3NjZFIiBmaWxsLW9wYWNpdHk9Ii4wOCIvPgo8L3BhdHRlcm4+PC9kZWZzPgo8cmVjdCB3aWR0aD0iMTYwMCIgaGVpZ2h0PSI0MjAiIGZpbGw9InVybCgjZykiLz4KPHJlY3Qgd2lkdGg9IjE2MDAiIGhlaWdodD0iNDIwIiBmaWxsPSJ1cmwoI2dyaWQpIi8+CjxnIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzBGNzY2RSIgc3Ryb2tlLW9wYWNpdHk9Ii4xMSIgc3Ryb2tlLXdpZHRoPSI0Ij4KPHBhdGggZD0iTTgzMCAzMzVDOTcwIDIxMCAxMDYwIDMwNSAxMTYwIDE5MFMxMzkwIDkwIDE1NzAgMTY1Ii8+CjxwYXRoIGQ9Ik05MDAgMzc1QzEwNDAgMjYwIDExNDAgMzQ1IDEyNDAgMjQwUzE0NTAgMTUwIDE1OTAgMjE1Ii8+CjwvZz4KPGcgZmlsbD0iIzBGNzY2RSIgZmlsbC1vcGFjaXR5PSIuMDciPgo8cmVjdCB4PSIxMTYwIiB5PSIxMjUiIHdpZHRoPSIxNjAiIGhlaWdodD0iMTA1IiByeD0iOCIvPgo8cmVjdCB4PSIxMzQwIiB5PSIxNDUiIHdpZHRoPSIxMjUiIGhlaWdodD0iODUiIHJ4PSI4Ii8+CjxyZWN0IHg9IjE0OTAiIHk9IjEwNSIgd2lkdGg9Ijc1IiBoZWlnaHQ9IjEyNSIgcng9IjgiLz4KPC9nPgo8ZyBmaWxsPSIjMjU2M0VCIiBmaWxsLW9wYWNpdHk9Ii4wOCI+CjxwYXRoIGQ9Ik0xMDQwIDI4NWgxMDBsMzAgNDVoLTE2NXoiLz48Y2lyY2xlIGN4PSIxMDcwIiBjeT0iMzM1IiByPSIxOCIvPjxjaXJjbGUgY3g9IjExNDAiIGN5PSIzMzUiIHI9IjE4Ii8+CjwvZz48L3N2Zz4=") center/cover no-repeat;border:1px solid #D8E6EA;border-radius:22px;padding:25px 30px;margin-bottom:15px;box-shadow:0 7px 24px rgba(15,23,42,.065)}
.logix-title{font-size:38px;line-height:1;font-weight:900;color:var(--navy);letter-spacing:.6px}
.logix-subtitle{color:var(--muted);font-size:14px;margin-top:3px}
.logix-badge{display:inline-block;margin-top:13px;padding:6px 10px;border-radius:999px;background:#E7F7F4;color:var(--teal);font-size:11px;font-weight:800;border:1px solid #C7ECE6}
.kpi{background:#fff;border:1px solid var(--line);border-radius:17px;padding:14px 15px;min-height:112px;box-shadow:0 4px 17px rgba(15,23,42,.055)}
.kpi-label{color:var(--muted);font-size:12px;font-weight:750}
.kpi-value{color:var(--text);font-size:24px;font-weight:900;margin-top:8px}
.section-title{color:var(--navy);font-size:18px;font-weight:900;margin:19px 0 8px}
.small-note{color:var(--muted);font-size:11px}
.footer{text-align:center;color:#64748B;font-size:11px;padding:14px 0 0}
</style>''', unsafe_allow_html=True)

@st.cache_resource
def conn():
    return mysql.connector.connect(host=os.getenv('LOGIX_DB_HOST','localhost'), port=int(os.getenv('LOGIX_DB_PORT','3306')), user=os.getenv('LOGIX_DB_USER','root'), password=os.getenv('LOGIX_DB_PASSWORD',''), database=os.getenv('LOGIX_DB_NAME','logix'))

@st.cache_data(ttl=300)
def q(sql, params=None):
    return pd.read_sql(sql, conn(), params=params)

def money(v):
    v=float(v or 0); return f'₹{v/1e9:.2f}B' if abs(v)>=1e9 else (f'₹{v/1e6:.2f}M' if abs(v)>=1e6 else f'₹{v:,.2f}')
def num(v): return f'{int(round(float(v or 0))):,}'
def pct(v): return f'{float(v or 0):.2f}%'
def card(label,value,icon):
    st.markdown(
        f'<div class="kpi"><div style="display:flex;justify-content:space-between;align-items:center">'
        f'<div class="kpi-label">{label}</div><div style="width:34px;height:34px;border-radius:11px;'
        f'background:#E8F7F5;display:flex;align-items:center;justify-content:center;font-size:17px">{icon}</div>'
        f'</div><div class="kpi-value">{value}</div><div class="small-note">LOGIX live data</div></div>',
        unsafe_allow_html=True)


def style_fig(fig,height=340):
    fig.update_layout(template="plotly_white",height=height,
        margin=dict(l=8,r=8,t=35,b=8),paper_bgcolor="white",plot_bgcolor="white",
        font=dict(family="Segoe UI, Arial",color="#0F172A",size=11),
        legend=dict(orientation="h",y=1.08))
    fig.update_xaxes(showgrid=False,linecolor="#E2E8F0")
    fig.update_yaxes(gridcolor="#EEF2F6",linecolor="#E2E8F0")
    return fig

def filters():
    mm=q('SELECT MIN(order_date) min_date, MAX(order_date) max_date FROM orders').iloc[0]
    mn,mx=pd.to_datetime(mm.min_date).date(),pd.to_datetime(mm.max_date).date()
    wh=q('SELECT warehouse_id,warehouse_name FROM warehouses ORDER BY warehouse_name')
    pa=q('SELECT partner_id,partner_name FROM delivery_partners ORDER BY partner_name')
    stt=q('SELECT DISTINCT order_status FROM orders ORDER BY order_status')
    st.sidebar.markdown('### Filters')
    dr=st.sidebar.date_input('Order date range',(mn,mx),min_value=mn,max_value=mx)
    if not isinstance(dr,tuple) or len(dr)!=2: dr=(mn,mx)
    w=st.sidebar.selectbox('Warehouse',['All']+wh.warehouse_name.tolist())
    p=st.sidebar.selectbox('Delivery Partner',['All']+pa.partner_name.tolist())
    s=st.sidebar.selectbox('Order Status',['All']+stt.order_status.tolist())
    clauses=['o.order_date BETWEEN %s AND %s']; params=[dr[0],dr[1]]
    if w!='All': clauses.append('s.warehouse_id=(SELECT warehouse_id FROM warehouses WHERE warehouse_name=%s LIMIT 1)'); params.append(w)
    if p!='All': clauses.append('s.delivery_partner_id=(SELECT partner_id FROM delivery_partners WHERE partner_name=%s LIMIT 1)'); params.append(p)
    if s!='All': clauses.append('o.order_status=%s'); params.append(s)
    return ' AND '.join(clauses),params

st.markdown('<div class="logix-header"><div class="logix-title">🚚 LOGIX</div><div style="font-size:21px;font-weight:800;color:#0F172A;margin-top:7px">Logistics & Supply Chain Intelligence Dashboard</div><div class="logix-subtitle">Executive Overview | 2023–2025</div><span class="logix-badge">● LIVE MYSQL DATA • INTERACTIVE ANALYTICS</span></div>',unsafe_allow_html=True)
st.sidebar.markdown('## 🚚 LOGIX'); st.sidebar.caption('Data-Driven Logistics Intelligence'); st.sidebar.markdown('---')
page=st.sidebar.radio('Navigation',['Executive Overview','Delivery & Logistics','Warehouse & Inventory','Customer & Sales','Returns & Payments','Fleet Performance'])
if st.sidebar.button('🔄 Refresh data',use_container_width=True): q.clear(); st.rerun()
try: where,params=filters()
except Exception as e: st.error(f'Database error: {e}'); st.info('Check .env and make sure MySQL/logix is running.'); st.stop()

if page=='Executive Overview':
    k=q(f'''SELECT COUNT(DISTINCT o.order_id) orders,COUNT(DISTINCT o.customer_id) customers,COALESCE(SUM(oi.line_total),0) revenue,COALESCE(SUM(s.shipping_cost),0) cost,COUNT(DISTINCT CASE WHEN s.shipment_status='Failed' THEN s.shipment_id END) failed,COUNT(DISTINCT r.return_id) returns,COALESCE(SUM(r.refund_amount),0) refunds,COUNT(DISTINCT CASE WHEN s.shipment_status='Delivered' THEN s.shipment_id END) delivered,COUNT(DISTINCT CASE WHEN s.shipment_status='Delivered' AND s.actual_delivery_date<=s.expected_delivery_date THEN s.shipment_id END) ontime FROM orders o LEFT JOIN order_items oi ON o.order_id=oi.order_id LEFT JOIN shipments s ON o.order_id=s.order_id LEFT JOIN returns r ON o.order_id=r.order_id WHERE {where}''',params).iloc[0]
    orders,customers,revenue,cost,failed,returns,refunds,delivered,ontime=[float(k[x] or 0) for x in ['orders','customers','revenue','cost','failed','returns','refunds','delivered','ontime']]
    vals=[('Total Orders',num(orders),'📦'),('Total Customers',num(customers),'👥'),('Total Revenue',money(revenue),'₹'),('Logistics Cost',money(cost),'🚚'),('Failed Shipments',num(failed),'⚠️'),('Total Returns',num(returns),'↩️')]
    for c,v in zip(st.columns(6),vals):
        with c: card(*v)
    vals2=[('On-Time Delivery',pct(ontime/delivered*100 if delivered else 0),'⏱️'),('Revenue / Order',money(revenue/orders if orders else 0),'📈'),('Cost / Order',money(cost/orders if orders else 0),'💰'),('Return Rate',pct(returns/orders*100 if orders else 0),'↩️'),('Shipment Failure Rate',pct(failed/orders*100 if orders else 0),'⚠️'),('Total Refunds',money(refunds),'💳')]
    for c,v in zip(st.columns(6),vals2):
        with c: card(*v)
    m=q(f'''SELECT DATE_FORMAT(o.order_date,'%Y-%m-01') month,COUNT(DISTINCT o.order_id) orders,COALESCE(SUM(oi.line_total),0) revenue FROM orders o LEFT JOIN order_items oi ON o.order_id=oi.order_id LEFT JOIN shipments s ON s.order_id=o.order_id WHERE {where} GROUP BY DATE_FORMAT(o.order_date,'%Y-%m-01') ORDER BY month''',params); m.month=pd.to_datetime(m.month)
    st.markdown('<div class="section-title">📈 Monthly Revenue & Orders Trend</div>',unsafe_allow_html=True)
    fig=go.Figure([go.Bar(x=m.month,y=m.revenue/1e9,name='Revenue (₹B)'),go.Scatter(x=m.month,y=m.orders,name='Orders',mode='lines+markers',yaxis='y2')]); fig.update_layout(template='plotly_white',height=350,yaxis_title='Revenue (₹B)',yaxis2=dict(title='Orders',overlaying='y',side='right'),legend=dict(orientation='h')); st.plotly_chart(style_fig(fig,360),use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        sh=q(f'''SELECT s.shipment_status,COUNT(*) shipments FROM shipments s JOIN orders o ON o.order_id=s.order_id WHERE {where} GROUP BY s.shipment_status ORDER BY shipments DESC''',params); fig=px.pie(sh,names='shipment_status',values='shipments',hole=.58,); st.plotly_chart(style_fig(fig),use_container_width=True)
    with c2:
        cat=q(f'''SELECT p.category,COALESCE(SUM(oi.line_total),0) revenue FROM order_items oi JOIN orders o ON o.order_id=oi.order_id JOIN products p ON p.product_id=oi.product_id LEFT JOIN shipments s ON s.order_id=o.order_id WHERE {where} GROUP BY p.category ORDER BY revenue DESC''',params); cat['B']=cat.revenue/1e9; fig=px.bar(cat.sort_values('B'),x='B',y='category',orientation='h',text='B',); fig.update_traces(marker_color='#0F766E',texttemplate='₹%{text:.2f}B',textposition='outside'); st.plotly_chart(style_fig(fig),use_container_width=True)
    c1,c2,c3=st.columns(3)
    with c1:
        wh=q(f'''SELECT w.warehouse_name,COUNT(DISTINCT s.shipment_id) shipments FROM shipments s JOIN orders o ON o.order_id=s.order_id JOIN warehouses w ON w.warehouse_id=s.warehouse_id WHERE {where} GROUP BY w.warehouse_name ORDER BY shipments DESC LIMIT 10''',params); fig=px.bar(wh.sort_values('shipments'),x='shipments',y='warehouse_name',orientation='h',); fig.update_traces(marker_color='#14B8A6'); st.plotly_chart(style_fig(fig),use_container_width=True)
    with c2:
        seg=q(f'''SELECT c.customer_segment,COUNT(DISTINCT c.customer_id) customers FROM customers c JOIN orders o ON o.customer_id=c.customer_id LEFT JOIN shipments s ON s.order_id=o.order_id WHERE {where} GROUP BY c.customer_segment''',params); fig=px.pie(seg,names='customer_segment',values='customers',hole=.58,); st.plotly_chart(style_fig(fig),use_container_width=True)
    with c3:
        dp=q(f'''SELECT p.partner_name,COUNT(DISTINCT s.shipment_id) shipments FROM shipments s JOIN orders o ON o.order_id=s.order_id JOIN delivery_partners p ON p.partner_id=s.delivery_partner_id WHERE {where} GROUP BY p.partner_name ORDER BY shipments DESC LIMIT 10''',params); fig=px.bar(dp.sort_values('shipments'),x='shipments',y='partner_name',orientation='h',); fig.update_traces(marker_color='#2563EB'); st.plotly_chart(style_fig(fig),use_container_width=True)

elif page=='Delivery & Logistics':
    st.markdown('<div class="section-title">🚚 Delivery & Logistics</div>',unsafe_allow_html=True)
    d=q(f'''SELECT s.delivery_type,s.shipment_status,COUNT(*) shipments,AVG(s.distance_km) avg_distance,AVG(s.shipping_cost) avg_cost FROM shipments s JOIN orders o ON o.order_id=s.order_id WHERE {where} GROUP BY s.delivery_type,s.shipment_status''',params)
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.bar(d,x='delivery_type',y='shipments',color='shipment_status',barmode='stack',title='Shipment Status by Delivery Type'),use_container_width=True)
    with c2: st.plotly_chart(px.scatter(d,x='avg_distance',y='avg_cost',size='shipments',color='shipment_status',hover_data=['delivery_type'],title='Distance vs Shipping Cost'),use_container_width=True)

elif page=='Warehouse & Inventory':
    st.markdown('<div class="section-title">🏭 Warehouse & Inventory</div>',unsafe_allow_html=True)
    inv=q('''SELECT w.warehouse_name,w.city,w.state,COUNT(i.inventory_id) records,COALESCE(SUM(i.current_stock),0) current_stock,COALESCE(SUM(i.inventory_value),0) inventory_value FROM inventory i JOIN warehouses w ON w.warehouse_id=i.warehouse_id GROUP BY w.warehouse_name,w.city,w.state ORDER BY inventory_value DESC''')
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.bar(inv.head(15).sort_values('inventory_value'),x='inventory_value',y='warehouse_name',orientation='h',title='Top Warehouses by Inventory Value'),use_container_width=True)
    with c2:
        ss=q('SELECT stock_status,COUNT(*) records FROM inventory GROUP BY stock_status ORDER BY records DESC'); st.plotly_chart(px.pie(ss,names='stock_status',values='records',hole=.55,title='Inventory Stock Status'),use_container_width=True)
    st.dataframe(inv,use_container_width=True,hide_index=True)

elif page=='Customer & Sales':
    st.markdown('<div class="section-title">👥 Customer & Sales</div>',unsafe_allow_html=True)
    d=q(f'''SELECT p.category,c.customer_segment,COUNT(DISTINCT o.order_id) orders,COALESCE(SUM(oi.line_total),0) revenue FROM order_items oi JOIN orders o ON o.order_id=oi.order_id JOIN products p ON p.product_id=oi.product_id JOIN customers c ON c.customer_id=o.customer_id LEFT JOIN shipments s ON s.order_id=o.order_id WHERE {where} GROUP BY p.category,c.customer_segment''',params)
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.bar(d.groupby('category',as_index=False).revenue.sum().sort_values('revenue'),x='revenue',y='category',orientation='h',title='Revenue by Category'),use_container_width=True)
    with c2: st.plotly_chart(px.pie(d.groupby('customer_segment',as_index=False).revenue.sum(),names='customer_segment',values='revenue',hole=.55,title='Revenue by Customer Segment'),use_container_width=True)
    st.dataframe(d.sort_values('revenue',ascending=False),use_container_width=True,hide_index=True)

elif page=='Returns & Payments':
    st.markdown('<div class="section-title">↩️ Returns & Payments</div>',unsafe_allow_html=True)
    r=q(f'''SELECT r.return_reason,r.return_status,COUNT(*) return_count,COALESCE(SUM(r.return_amount),0) return_value,COALESCE(SUM(r.refund_amount),0) refund_value FROM returns r JOIN orders o ON o.order_id=r.order_id LEFT JOIN shipments s ON s.order_id=o.order_id WHERE {where} GROUP BY r.return_reason,r.return_status''',params)
    p=q(f'''SELECT p.payment_method,p.payment_status,COUNT(*) payments,COALESCE(SUM(p.amount),0) amount FROM payments p JOIN orders o ON o.order_id=p.order_id LEFT JOIN shipments s ON s.order_id=o.order_id WHERE {where} GROUP BY p.payment_method,p.payment_status''',params)
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.bar(r.groupby('return_reason',as_index=False).return_count.sum().sort_values('return_count'),x='return_count',y='return_reason',orientation='h',title='Return Reasons'),use_container_width=True)
    with c2: st.plotly_chart(px.pie(p.groupby('payment_method',as_index=False).amount.sum(),names='payment_method',values='amount',hole=.55,title='Payment Value by Method'),use_container_width=True)
    st.dataframe(r.sort_values('refund_value',ascending=False),use_container_width=True,hide_index=True)

else:
    st.markdown('<div class="section-title">🚛 Fleet Performance</div>',unsafe_allow_html=True)
    f=q('''SELECT d.driver_id,d.driver_name,d.experience_years,d.rating,d.city,d.status,v.vehicle_type,v.fuel_type,v.capacity_kg FROM drivers d LEFT JOIN vehicles v ON v.driver_id=d.driver_id''')
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.scatter(f.dropna(subset=['experience_years','rating']),x='experience_years',y='rating',size='capacity_kg',color='vehicle_type',hover_data=['driver_name','city'],title='Driver Experience vs Rating'),use_container_width=True)
    with c2:
        fm=f.fuel_type.value_counts().reset_index(); fm.columns=['fuel_type','vehicles']; st.plotly_chart(px.pie(fm,names='fuel_type',values='vehicles',hole=.55,title='Vehicle Fuel Mix'),use_container_width=True)
    st.dataframe(f,use_container_width=True,hide_index=True)

st.markdown('---'); st.markdown('<div class="small-note">LOGIX • Python + MySQL + Pandas + Plotly + Streamlit</div>',unsafe_allow_html=True)

