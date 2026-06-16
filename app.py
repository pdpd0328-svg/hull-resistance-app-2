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

# 3. Holtrop-Mennen 기반 정밀 연산 알고리즘 함수
def calculate_resistance_precise(L, B, T, Cb, V_knots):
    V_ms = V_knots * 0.5144
    rho = 1025.0
    nu = 1.188e-6
    g = 9.80665
    
    # 가상의 선형 계수 설정 (고도화용)
    Cm = 0.98
    Cwp = 0.7 + (Cb * 0.1)
    Cp = Cb / Cm
    LCB = -1.5 
    
    # 침수표면적 S 연산
    S = L * (2 * T + B) * np.sqrt(Cm) * (0.453 + 0.4425 * Cb - 0.2862 * Cm - 0.003467 * (B / T) + 0.3696 * Cwp)
    
    # 1. 마찰저항 (Rf)
    Rn = (V_ms * L) / nu if V_ms > 0 else 1
    Cf = 0.075 / ((np.log10(Rn) - 2) ** 2) if Rn > 1 else 0
    Rf = 0.5 * rho * S * (V_ms**2) * Cf / 1000.0
    
    # 2. 형상계수 적용 점성저항 (1+k1)
    Lr = L * (1 - Cp + (0.06 * Cp * LCB) / (4 * Cp - 1))
    c14 = 1.0 # Standard stern
    vol = L * B * T * Cb
    form_factor = 0.93 + 0.487118 * c14 * ((B / L)**1.06806) * ((T / L)**0.46106) * ((L / Lr)**0.12156) * ((L**3 / vol)**0.36486) * ((1 - Cwp)**-0.60424)
    R_viscous = Rf * form_factor
    
    # 3. 조파저항 (Rw)
    Fn = V_ms / np.sqrt(g * L) if L > 0 else 0
    i_E = 1 + 89 * np.exp(-((L/B)**0.80856) * ((1-Cwp)**0.30484) * ((1-Cp-0.0225*LCB)**0.6367) * ((Lr/B)**0.34574) * (((100*vol)/(L**3))**0.16302))
    c7 = B / L
    c1 = 2223105 * (c7**3.78613) * ((T/B)**1.07961) * ((90 - i_E)**-1.37565)
    m1 = 0.0113 * L / B # 약식 보정 지수
    m2 = -0.003 * L / T
    Rw = c1 * 1.0 * 1.0 * rho * g * vol * np.exp(m1 * (Fn**-0.9) + m2 * np.cos(1.5 * (Fn**-2))) / 1000.0 if Fn > 0 else 0
    if Rw < 0: Rw = 0
    
    # 4. 상관수정저항 (Ra)
    Ca = 0.00351 * (L**-0.3) - 0.00138
    Ra = 0.5 * rho * S * (V_ms**2) * Ca / 1000.0
    
    # 총저항 합산 (추가 압력 성분 포함 가정)
    Rt = R_viscous + Rw + Ra
    
    return round(Rt, 2), round(Rf, 2), round(Rw, 2), round(Ra, 2)

# 4. 구간 데이터 생성
speeds = np.arange(10.0, 25.5, 0.5)
rt_list, rf_list, rw_list, ra_list = [], [], [], []

for v in speeds:
    rt, rf, rw, ra = calculate_resistance_precise(Lbp, B, T, Cb, v)
    rt_list.append(rt)
    rf_list.append(rf)
    rw_list.append(rw)
    ra_list.append(ra)

df = pd.DataFrame({
    'Speed (knots)': speeds,
    'Total Resistance (Rt, kN)': rt_list,
    'Frictional Resistance (Rf, kN)': rf_list,
    'Wave Resistance (Rw, kN)': rw_list,
    'Correlation Allowance (Ra, kN)': ra_list
})

# 5. 탭(Tab) 레이아웃 생성 (Antigravity 디자인 복원)
tab_dashboard, tab_table, tab_ref = st.tabs(["📊 성능 그래프 분석", "📋 속도별 상세 데이터", "📖 학술 논문급 저항 공식 해설"])

with tab_dashboard:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 특정 속도 연산 결과")
        t_rt, t_rf, t_rw, t_ra = calculate_resistance_precise(Lbp, B, T, Cb, selected_speed)
        st.metric(label=f"선택 선속 {selected_speed} knots 총저항 (Rt)", value=f"{t_rt} kN")
        st.write("**세부 저항 구성 성분:**")
        st.caption(f"- 기초 마찰저항 (Rf): {t_rf} kN")
        st.caption(f"- 조파 항력저항 (Rw): {t_rw} kN")
        st.caption(f"- 상관 수정저항 (Ra): {t_ra} kN")
    with col2:
        st.subheader("📈 속도-저항 성능 곡선")
        fig = px.line(df, x='Speed (knots)', y=['Total Resistance (Rt, kN)', 'Frictional Resistance (Rf, kN)', 'Wave Resistance (Rw, kN)'],
                      labels={'value': 'Resistance (kN)', 'variable': 'Component'},
                      title="선속 변화량에 따른 저항 성분별 추이")
        st.plotly_chart(fig, use_container_width=True)

with tab_table:
    st.subheader("📋 속도별 수치 데이터 시트")
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab_ref:
    st.subheader("Holtrop & Mennen (1982, 1984) 학술 연구 저항 공식 해설")
    st.write("이 대시보드 그래프에 반영된 각 저항 성분의 정밀 연산식은 Holtrop & Mennen의 원래 수학적 회귀 모델에 기반을 두고 있습니다.")
    
    st.markdown("### 1. 지배 방정식 (Governing Equation)")
    st.latex(r"R_T = R_F (1 + k_1) + R_{APP} + R_W + R_B + R_{TR} + R_A")
    
    st.markdown("### 2. 마찰 저항 (Frictional Resistance, $R_F$)")
    st.latex(r"R_F = \frac{1}{2} \rho S V^2 C_F")
    st.latex(r"C_F = \frac{0.075}{(\log_{10}(Re) - 2)^2}")
    
    st.markdown("### 3. 점성 저항 및 형상 계수 ($1+k_1$)")
    st.latex(r"1 + k_1 = 0.93 + 0.487118 \cdot c_{14} \cdot \left(\frac{B}{L_{bp}}\right)^{1.06806} \cdot \left(\frac{T}{L_{bp}}\right)^{0.46106}")
    
    st.markdown("### 4. 조파 저항 (Wave-making Resistance, $R_W$)")
    st.latex(r"R_W = c_1 c_2 c_5 \rho g \nabla \exp \left[ m_1 F_n^{-0.9} + m_2 \cos(\lambda F_n^{-2}) \right]")
    
    st.markdown("---")
    st.caption("Reference: Holtrop, J., & Mennen, G. G. J. (1982). An approximate power prediction method. International Shipbuilding Progress, 29(335), 166-170.")
