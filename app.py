import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# 1. 페이지 및 레이아웃 설정
st.set_page_config(page_title="선체 저항 계산 대시보드", layout="wide")

st.title("🚢 선체 저항 계산 자동화 프로토타입 프로그램")
st.write("본 프로그램은 입력된 선박의 제원을 바탕으로 속도별 총 저항(Total Resistance)을 추정합니다.")
st.markdown("---")

# 2. 사이드바 입력 제원 설정
st.sidebar.header("선박 주요 제원 입력 (Input Particulars)")
Lbp = st.sidebar.slider("선장 (Lbp, m)", min_value=50.0, max_value=400.0, value=175.0, step=1.0)
B = st.sidebar.slider("선폭 (B, m)", min_value=10.0, max_value=60.0, value=25.0, step=0.5)
T = st.sidebar.slider("흘수 (T, m)", min_value=2.0, max_value=20.0, value=8.5, step=0.1)
Cb = st.sidebar.slider("방형비척계수 (Cb)", min_value=0.50, max_value=0.90, value=0.70, step=0.01)

selected_speed = st.sidebar.slider("특정 계산 속도 (V, knots)", min_value=10.0, max_value=25.0, value=15.0, step=0.5)

# 3. Holtrop-Mennen 기반 저항 계산 알고리즘
def calculate_resistance(L, B, T, Cb, V_knots):
    V_ms = V_knots * 0.5144  # knots -> m/s 변환
    rho = 1025.0            # 해수 밀도
    nu = 1.188e-6           # 해수 동점성계수
    g = 9.81                # 중력가속도
    
    # 침수표면적(S) 근사식
    S = L * (2 * T + B) * np.sqrt(Cb) * (0.453 + 0.4425 * Cb - 0.2862 * Cb**2 - 0.00346 * B / T)
    
    # 레이놀즈 수 및 마찰저항 계수 (ITTC-1957 공식 적용)
    Rn = (V_ms * L) / nu if V_ms > 0 else 1
    Cf = 0.075 / ((np.log10(Rn) - 2) ** 2) if Rn > 1 else 0
    
    # 조파저항 계수 (프로토타입용 근사 모델)
    Fn = V_ms / np.sqrt(g * L) if L > 0 else 0
    Cw = 0.001 * (Cb ** 2) * np.exp(Fn)
    
    # 저항 성분 계산 (kN 단위)
    Rf = 0.5 * rho * S * (V_ms**2) * Cf / 1000.0
    Rw = 0.5 * rho * S * (V_ms**2) * Cw / 1000.0
    Rt = Rf + Rw
    
    return round(Rt, 2), round(Rf, 2), round(Rw, 2)

# 4. 10~25노트 구간 데이터 연산
speeds = np.arange(10.0, 25.5, 0.5)
rt_list, rf_list, rw_list = [], [], []

for v in speeds:
    rt, rf, rw = calculate_resistance(Lbp, B, T, Cb, v)
    rt_list.append(rt)
    rf_list.append(rf)
    rw_list.append(rw)

df = pd.DataFrame({
    'Speed (knots)': speeds,
    'Total Resistance (Rt, kN)': rt_list,
    'Frictional Resistance (Rf, kN)': rf_list,
    'Wave Resistance (Rw, kN)': rw_list
})

# 5. 화면 레이아웃 및 시각화 출력
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 특정 속도 계산 결과")
    target_rt, target_rf, target_rw = calculate_resistance(Lbp, B, T, Cb, selected_speed)
    st.metric(label=f"선택한 속도 {selected_speed} knots에서의 총 저항(Rt)", value=f"{target_rt} kN")
    
    st.write("**저항 세부 구성 요소:**")
    st.caption(f"- 마찰저항 (Rf): {target_rf} kN")
    st.caption(f"- 조파저항 (Rw): {target_rw} kN")
    
    st.write("**선박 제원 요약 데이터 프레임**")
    st.dataframe(df.set_index('Speed (knots)').head(8))

with col2:
    st.subheader("📈 속도-저항 곡선 (Resistance Curve)")
    fig = px.line(df, x='Speed (knots)', y=['Total Resistance (Rt, kN)', 'Frictional Resistance (Rf, kN)', 'Wave Resistance (Rw, kN)'],
                  labels={'value': 'Resistance (kN)', 'variable': 'Type'},
                  title=f"L={Lbp}m, B={B}m, T={T}m 조건의 저항 곡선")
    st.plotly_chart(fig, use_container_width=True)

# 6. 학술적 출처 명시 (Footer)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "Reference: Holtrop, J., & Mennen, G. G. J. (1982). An approximate power prediction method. International Shipbuilding Progress, 29(335), 166-170."
    "</div>", 
    unsafe_html=True
)
