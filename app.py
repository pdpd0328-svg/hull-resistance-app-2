import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="선박 저항 계산 대시보드 (상세 설계 모드)",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 고급스러운 스타일링을 위한 커스텀 CSS 적용
st.markdown("""
    <style>
        /* 폰트 및 스타일 전반 적용 */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Noto Sans KR', 'Plus Jakarta Sans', sans-serif;
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        h1, h2, h3 {
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            font-weight: 700;
            color: #0f172a;
        }
        
        /* 프리미엄 그라데이션 타이틀 */
        .title-gradient {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            font-weight: 800;
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
            letter-spacing: -0.05em;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #475569;
            margin-bottom: 2rem;
            font-weight: 300;
        }
        /* 개별 메트릭 카드 스타일 */
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
            border: 1px solid #f1f5f9;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            border-color: #e2e8f0;
        }
        .metric-title {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2.25rem;
            font-weight: 700;
            color: #1e293b;
            font-family: 'Outfit', sans-serif;
            line-height: 1;
        }
        .metric-unit {
            font-size: 1rem;
            color: #64748b;
            font-weight: 400;
            margin-left: 0.25rem;
        }
        .metric-desc {
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 0.5rem;
        }
        
        /* 정보 배너 및 설명 박스 스타일 */
        .info-banner {
            background-color: #f8fafc;
            border-left: 4px solid #3b82f6;
            padding: 1rem 1.5rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 2rem;
        }
        
        .explanation-block {
            background-color: #f8fafc;
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            margin: 1rem 0;
        }
        .explanation-title {
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 0.5rem;
            font-family: 'Outfit', sans-serif;
        }
        
        /* 커스텀 하단 푸터 */
        .footer {
            margin-top: 4rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e2e8f0;
            font-size: 0.8rem;
            color: #64748b;
            text-align: center;
        }
        
        /* 수식 블록 스타일 */
        .math-block {
            background-color: #f1f5f9;
            padding: 1.2rem;
            border-radius: 10px;
            border: 1px solid #cbd5e1;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- 사이드바 상세 입력창 -----------------
st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 1.5rem;'>
        <h2 style='margin: 0; color: #1e3a8a; font-family: "Noto Sans KR"; font-size: 1.6rem;'>선체 제원 설정</h2>
        <p style='color: #64748b; font-size: 0.85rem; margin-top: 0.2rem;'>선형 및 부가물의 상세 치수를 입력하세요</p>
    </div>
""", unsafe_allow_html=True)

# 1. 기본 선체 제원
with st.sidebar.expander("1. 기본 선체 제원 (Main Dimensions)", expanded=True):
    Lbp = st.number_input("선박 수선간장 (Lbp) [m]", min_value=10.0, max_value=500.0, value=150.0, step=1.0, format="%.2f")
    B = st.number_input("선폭 (B) [m]", min_value=2.0, max_value=100.0, value=24.0, step=0.1, format="%.2f")
    T = st.number_input("계획 흘수 (T) [m]", min_value=1.0, max_value=30.0, value=9.0, step=0.1, format="%.2f")
    Cb = st.number_input("방형 비척 계수 (Cb)", min_value=0.3000, max_value=0.9500, value=0.7000, step=0.0010, format="%.4f")
    V_selected = st.number_input("설계 운항 속도 (V) [knots]", min_value=5.0, max_value=40.0, value=16.0, step=0.1, format="%.2f")

# 2. 선형 주요 계수
with st.sidebar.expander("2. 선형 주요 계수 (Coefficients)", expanded=False):
    Cm = st.number_input("중앙단면계수 (Cm)", min_value=0.5000, max_value=0.9990, value=0.9800, step=0.0010, format="%.4f")
    
    auto_cwp = st.checkbox("수선면적계수 (Cwp) 자동 계산", value=True, help="체크 해제 시 수동으로 Cwp를 입력할 수 있습니다.")
    if auto_cwp:
        Cwp_val = 0.7 * Cb + 0.3
        st.info(f"계산된 Cwp: {Cwp_val:.4f}")
    else:
        Cwp_val = st.number_input("수선면적계수 (Cwp) 입력", min_value=0.4000, max_value=0.9900, value=0.7900, step=0.0010, format="%.4f")
        
    LCB_pct = st.number_input(
        "종방향 부심 위치 (LCB) [% Lbp]", 
        min_value=-10.0, 
        max_value=10.0, 
        value=0.0, 
        step=0.1, 
        format="%.2f",
        help="Lbp 중앙부 기준 선수 방향(+), 선미 방향(-) 백분율 위치입니다."
    )

# 3. 특수 선체 요소
with st.sidebar.expander("3. 특수 선체 요소 (Special Features)", expanded=False):
    stern_choice = st.selectbox(
        "선미 형상 유형 (Stern Shape)",
        options=["중립형 선형 (0)", "U형 선형 (+10)", "V형 선형 (-10)"],
        index=0
    )
    if "U형" in stern_choice:
        c_stern = 10.0
    elif "V형" in stern_choice:
        c_stern = -10.0
    else:
        c_stern = 0.0
    st.markdown("**구상 선수 (Bulbous Bow)**")
    A_bt = st.number_input("구상선수 최대 횡단면적 (A_bt) [m²]", min_value=0.0, max_value=150.0, value=0.0, step=0.5, format="%.2f")
    h_b = st.number_input("구상선수 중심 높이 (h_b) [m]", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f")
    st.markdown("**선미 트랜섬 (Transom Stern)**")
    A_trans = st.number_input("트랜섬 침수 단면적 (A_trans) [m²]", min_value=0.0, max_value=100.0, value=0.0, step=0.5, format="%.2f")

# 4. 부가물 정보
with st.sidebar.expander("4. 부가물 정보 (Appendages)", expanded=False):
    S_app = st.number_input("부가물 침수 표면적 (S_app) [m²]", min_value=0.0, max_value=1000.0, value=0.0, step=1.0, format="%.2f")
    one_plus_k_app = st.number_input("부가물 저항 계수 (1 + k_app)", min_value=1.0, max_value=4.0, value=1.5, step=0.1, format="%.2f")

# 설계 건전성 검토 및 조언 (한글 메시지)
warnings = []
if B / T < 1.5:
    warnings.append("⚠️ **폭-흘수 비 (B/T)**가 다소 낮습니다 (< 1.5). 이는 선박 복원성이 다소 불리할 수 있음을 나타내거나 일반적인 상선 계산 범위를 벗어날 수 있습니다.")
if B / T > 4.5:
    warnings.append("⚠️ **폭-흘수 비 (B/T)**가 다소 높습니다 (> 4.5). 얕은 물에서의 영향이나 유효 조파 저항 상승 우려가 있습니다.")
if Lbp / B < 4.0:
    warnings.append("⚠️ **길이-폭 비 (Lbp/B)**가 매우 낮습니다 (< 4.0). 선체가 통통하여 조파 저항(파도를 만듦으로써 받는 저항)이 과도하게 상승할 수 있습니다.")
if Lbp / B > 10.0:
    warnings.append("⚠️ **길이-폭 비 (Lbp/B)**가 매우 높습니다 (> 10.0). 선체가 매우 날씬하여 추진 효율에는 유리하나 선체 강도 및 종강도 설계 시 불리할 수 있습니다.")
if T >= B:
    warnings.append("❌ **계획 흘수 (T)**가 **선폭 (B)**보다 크거나 같을 수 없습니다. 정상적인 설계 범위 내로 흘수 혹은 선폭을 재조정해 주세요.")

# ----------------- 계산 엔진 (Holtrop & Mennen 1984 풀 공식 구현) -----------------
def calculate_resistance_components(Lbp, B, T, Cb, Cm, Cwp, LCB, c_stern, A_bt, h_b, A_trans, S_app, one_plus_k_app, V_knots):
    rho = 1025.0  # 해수 밀도 (kg/m3)
    g = 9.80665   # 중력 가속도 (m/s2)
    nu = 1.188e-6 # 해수 동점성 계수 (15℃ 기준, m2/s)
    
    V_ms = V_knots * 0.514444
    
    # 1. 배수 용적 (Displacement Volume)
    disp_vol = Cb * Lbp * B * T
    
    # 2. 침수 표면적 (S) 계산
    # Holtrop 침수표면적 공식
    S_hull = Lbp * (2 * T + B) * np.sqrt(Cm) * (0.453 + 0.4425 * Cb - 0.2862 * Cm - 0.003467 * (B / T) + 0.3696 * Cwp)
    if A_bt > 0 and Cb > 0:
        S_hull += 2.38 * A_bt / Cb
    
    # 3. 마찰 저항 (Rf) 계산
    if V_ms > 0:
        Re = (V_ms * Lbp) / nu
        Cf = 0.075 / (np.log10(Re) - 2) ** 2
    else:
        Re = 1.0
        Cf = 0.0
    
    Rf = 0.5 * rho * S_hull * (V_ms ** 2) * Cf / 1000.0  # kN 단위
    
    # 4. 형상 계수 (1 + k1) 및 점성 저항 계산
    vol_term = Lbp ** 3 / max(disp_vol, 1.0)
    
    # Prismatic Coefficient (Cp)
    Cp = Cb / max(0.5, Cm)
    
    # L_R (Length of run) 계산
    denom_Lr = 4 * Cp - 1.0
    if abs(denom_Lr) < 0.001:
        denom_Lr = 0.001 if denom_Lr >= 0 else -0.001
    
    Lr_over_L = 1.0 - Cp + 0.06 * Cp * LCB / denom_Lr
    Lr_over_L = max(0.05, Lr_over_L)
    
    c14 = 1.0 + 0.011 * c_stern
    
    # Holtrop & Mennen 1984 형상계수 regression 식
    k1_term = 0.487118 * c14 * (B / Lbp) ** 1.06806 * (T / Lbp) ** 0.46106 * (1.0 / Lr_over_L) ** 0.12156 * vol_term ** 0.36486 * (1.0 - Cwp) ** -0.60424
    k1 = 0.93 + k1_term - 1.0
    k1 = max(0.05, min(k1, 0.45))  # 물리적 경계 보호
    form_factor = 1 + k1
    R_visc = Rf * form_factor
    
    # 5. 부가물 저항 (Rapp) 계산
    if S_app > 0:
        Rapp = 0.5 * rho * (V_ms ** 2) * S_app * Cf * one_plus_k_app / 1000.0  # kN 단위
    else:
        Rapp = 0.0
    
    # 6. 조파 저항 (Rw) 계산
    Fn = V_ms / np.sqrt(g * Lbp) if Lbp > 0 else 0
    
    if Fn > 0:
        # 선수 반각 i_E 계산 (LCB 포함 Holtrop 공식)
        base_ie = 1.0 - Cp - 0.0225 * LCB
        base_ie = max(0.001, base_ie)
        
        ie_exp_arg = (
            - (Lbp / B) ** 0.80856 
            * (1.0 - Cwp) ** 0.30484 
            * base_ie ** 0.6367 
            * (Lr_over_L * Lbp / B) ** 0.34574 
            * (100 * disp_vol / (Lbp ** 3)) ** 0.16302
        )
        i_E = 1.0 + 89.0 * np.exp(ie_exp_arg)
        
        # c7 계수 계산 (B/Lbp 비율 조건 분기)
        b_over_l = B / Lbp
        if b_over_l < 0.11:
            c7 = 0.229577 * b_over_l ** 0.33333
        elif b_over_l <= 0.25:
            c7 = b_over_l
        else:
            c7 = 0.5 - 0.0625 / b_over_l
            
        c1 = 2223105.0 * c7 ** 3.78613 * (T / B) ** 1.07961 * (90.0 - i_E) ** -1.37565
        
        # c2 계수 계산 (구상 선수 벌브 영향 보정)
        if A_bt > 0:
            denom_c3 = B * T * (0.56 * np.sqrt(A_bt) + h_b)
            c3 = 0.56 * (A_bt ** 1.5) / max(0.001, denom_c3)
            c2 = np.exp(-1.89 * np.sqrt(c3))
        else:
            c2 = 1.0
            
        # c5 계수 계산 (트랜섬 선미 침수 영향 보정)
        denom_c5 = B * T * Cb
        if denom_c5 > 0:
            c5 = 1.0 - 0.8 * A_trans / denom_c5
            c5 = max(0.0, c5)
        else:
            c5 = 1.0
            
        m1 = 0.0113 * (Lbp / B) - 1.8
        
        # m2 계산 (c15 계수 계산 포함)
        vol_term_cube = Lbp ** 3 / max(disp_vol, 1.0)
        if vol_term_cube < 512.0:
            c15 = -0.003853 * (vol_term_cube - 475.24) ** 2 / 240000.0
        else:
            c15 = 0.0
        m2 = c15 * (Lbp / B) ** 2 * Cp ** 2
        
        lam = 1.4 - 0.08 * (Lbp / B)
        
        # 지수 조파 저항 계산
        exp_arg = m1 * (Fn ** -0.9) + m2 * np.cos(lam * (Fn ** -2))
        exp_arg = min(700.0, max(-700.0, exp_arg))  # 오버플로우 제한
        
        Rw = c1 * c2 * c5 * rho * g * disp_vol * np.exp(exp_arg) / 1000.0  # kN 단위
        Rw = max(0.0, Rw)
    else:
        Rw = 0.0
        
    # 7. 구상 선수 추가 압력 저항 (Rb) 계산
    if A_bt > 0 and T > 0:
        denom_Pb = T - 1.5 * h_b
        denom_Pb = max(0.001, denom_Pb)
        Pb = 0.56 * np.sqrt(A_bt) / denom_Pb
        
        term_under_sqrt = g * (T - h_b - 0.25 * np.sqrt(A_bt)) + 0.15 * V_ms ** 2
        term_under_sqrt = max(0.001, term_under_sqrt)
        Fni = V_ms / np.sqrt(term_under_sqrt)
        
        # Rb 공식
        Rb_term = 0.11 * np.exp(-3.0 / max(0.001, Pb ** 2)) * (Fni ** 3) * (A_bt ** 1.5) * rho * g / (1.0 + Fni ** 2)
        Rb = Rb_term / 1000.0  # kN 단위
        Rb = max(0.0, Rb)
    else:
        Rb = 0.0
        
    # 8. 트랜섬 선미 침수 저항 (Rtr) 계산
    if A_trans > 0:
        denom_Fnt = 2.0 * g * A_trans / (B * (1.0 + Cwp))
        Fnt = V_ms / np.sqrt(max(0.001, denom_Fnt))
        
        if Fnt < 5.0:
            c6 = 0.2 * (1.0 - 0.2 * Fnt)
        else:
            c6 = 0.0
        Rtr = 0.5 * rho * (V_ms ** 2) * A_trans * c6 / 1000.0  # kN 단위
        Rtr = max(0.0, Rtr)
    else:
        Rtr = 0.0
        
    # 9. 상관 수정 저항 (Ra) 계산
    Ca = 0.00351 * (Lbp ** -0.3) - 0.00138
    Ca = max(Ca, 0.0001)  # 최소 거칠기 한계
    Ra = 0.5 * rho * S_hull * (V_ms ** 2) * Ca / 1000.0  # kN 단위
    
    # 총저항 (Rt) 합산
    Rt = R_visc + Rapp + Rw + Rb + Rtr + Ra
    
    # 유효 동력 (Pe)
    Pe_kW = Rt * V_ms  # kN * m/s = kW
    Pe_hp = Pe_kW * 1.34102  # kW -> 마력(hp)
    
    return {
        'S': S_hull,
        'disp_vol': disp_vol,
        'Re': Re,
        'Cf': Cf,
        'Rf': Rf,
        'form_factor': form_factor,
        'R_visc': R_visc,
        'Rapp': Rapp,
        'Fn': Fn,
        'Rw': Rw,
        'Rb': Rb,
        'Rtr': Rtr,
        'Ca': Ca,
        'Ra': Ra,
        'Rt': Rt,
        'Pe_kW': Pe_kW,
        'Pe_hp': Pe_hp
    }

# 입력한 수치에 기반한 저항 계산 수행
res_selected = calculate_resistance_components(
    Lbp, B, T, Cb, Cm, Cwp_val, LCB_pct, c_stern, A_bt, h_b, A_trans, S_app, one_plus_k_app, V_selected
)

# ----------------- 웹 대시보드 화면 구성 -----------------
st.markdown("<div class='title-gradient'>선박 저항 및 유효 마력 예측 대시보드 (상세 모드)</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Holtrop & Mennen (1984) 풀 경험식을 기반으로 구상선수, 트랜섬 선미, 선체 형상 계수 및 부가물 영향을 정밀 계산합니다.</div>", unsafe_allow_html=True)

# 오류 제어
if T >= B:
    st.error("🚨 제원 설정 오류: 계획 흘수(T)는 선폭(B)보다 반드시 작아야 연산이 가능합니다. 왼쪽 패널의 제원을 확인하여 조정해 주시기 바랍니다.")
else:
    # 설계 조건 경고
    if warnings:
        with st.expander("🔍 선체 설계 제원비 분석 알림", expanded=False):
            for w in warnings:
                st.write(w)
                
    # 1. 핵심 성과 지표 (KPI) 카드 행
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>총저항 (Rt)</div>
                <div class='metric-value'>{res_selected['Rt']:.2f}<span class='metric-unit'>kN</span></div>
                <div class='metric-desc'>{V_selected:.2f} 노트 기준 (Froude 수: {res_selected['Fn']:.3f})</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>필요 유효 마력 (Pe)</div>
                <div class='metric-value'>{res_selected['Pe_kW']:.1f}<span class='metric-unit'>kW</span></div>
                <div class='metric-desc'>약 {res_selected['Pe_hp']:.0f} 마력 (hp) 소요</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        # 비중이 높은 상위 성분 분석
        components = {
            '점성 저항': res_selected['R_visc'],
            '조파 저항': res_selected['Rw'],
            '구상선수 저항': res_selected['Rb'],
            '트랜섬 저항': res_selected['Rtr'],
            '부가물 저항': res_selected['Rapp'],
            '상관 수정 저항': res_selected['Ra']
        }
        max_comp = max(components, key=components.get)
        max_val_pct = (components[max_comp] / res_selected['Rt']) * 100.0
        
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>주요 저항 성분</div>
                <div class='metric-value'>{max_comp}</div>
                <div class='metric-desc'>전체 저항의 {max_val_pct:.1f}% 차지</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>침수 표면적 (S)</div>
                <div class='metric-value'>{res_selected['S']:.1f}<span class='metric-unit'>m²</span></div>
                <div class='metric-desc'>배수 용적: {res_selected['disp_vol']:.1f} m³</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 탭 메뉴
    tab_dashboard, tab_table, tab_ref = st.tabs(["📊 성능 그래프 분석", "📋 속도별 상세 데이터", "📖 학술 논문급 저항 공식 해설"])
    
    # ----------------- 탭 1: 대시보드 그래프 -----------------
    with tab_dashboard:
        # 10노트부터 25노트까지 계산 수행
        speeds = np.linspace(10.0, 25.0, 31)
        # 선택한 속도가 범위 밖일 경우 그래프 범위 동적 처리
        if V_selected < 10.0:
            speeds = np.linspace(V_selected, 25.0, 31)
        elif V_selected > 25.0:
            speeds = np.linspace(10.0, V_selected, 31)
            
        data_range = []
        for v in speeds:
            r = calculate_resistance_components(
                Lbp, B, T, Cb, Cm, Cwp_val, LCB_pct, c_stern, A_bt, h_b, A_trans, S_app, one_plus_k_app, v
            )
            data_range.append({
                '속도 (knots)': v,
                '마찰저항 (Rf)': r['Rf'],
                '점성저항 (R_visc)': r['R_visc'],
                '조파저항 (Rw)': r['Rw'],
                '구상선수저항 (Rb)': r['Rb'],
                '트랜섬저항 (Rtr)': r['Rtr'],
                '부가물저항 (Rapp)': r['Rapp'],
                '상관저항 (Ra)': r['Ra'],
                '총저항 (Rt)': r['Rt'],
                '유효동력 (kW)': r['Pe_kW']
            })
            
        df = pd.DataFrame(data_range)
        
        # Plotly를 이용한 상호작용 그래프 작성
        fig = go.Figure()
        
        # 선 추가
        fig.add_trace(go.Scatter(
            x=df['속도 (knots)'], y=df['총저항 (Rt)'],
            mode='lines+markers', name='총저항 (Rt)',
            line=dict(color='#0f172a', width=4),
            marker=dict(size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['속도 (knots)'], y=df['점성저항 (R_visc)'],
            mode='lines', name='점성저항 (Rf * (1+k1))',
            line=dict(color='#2563eb', width=2, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['속도 (knots)'], y=df['마찰저항 (Rf)'],
            mode='lines', name='순수 마찰저항 (Rf)',
            line=dict(color='#60a5fa', width=1.5, dash='dot')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['속도 (knots)'], y=df['조파저항 (Rw)'],
            mode='lines', name='조파저항 (Rw)',
            line=dict(color='#dc2626', width=2)
        ))
        
        if A_bt > 0:
            fig.add_trace(go.Scatter(
                x=df['속도 (knots)'], y=df['구상선수저항 (Rb)'],
                mode='lines', name='구상선수저항 (Rb)',
                line=dict(color='#d97706', width=2, dash='dashdot')
            ))
            
        if A_trans > 0:
            fig.add_trace(go.Scatter(
                x=df['속도 (knots)'], y=df['트랜섬저항 (Rtr)'],
                mode='lines', name='트랜섬저항 (Rtr)',
                line=dict(color='#7c3aed', width=2, dash='dash')
            ))
            
        if S_app > 0:
            fig.add_trace(go.Scatter(
                x=df['속도 (knots)'], y=df['부가물저항 (Rapp)'],
                mode='lines', name='부가물저항 (Rapp)',
                line=dict(color='#db2777', width=1.5, dash='dot')
            ))
        
        fig.add_trace(go.Scatter(
            x=df['속도 (knots)'], y=df['상관저항 (Ra)'],
            mode='lines', name='상관 및 거칠기 저항 (Ra)',
            line=dict(color='#10b981', width=1.5, dash='dot')
        ))
        
        # 선택한 속도 위치에 수직 기준선 추가
        fig.add_shape(
            type="line",
            x0=V_selected, y0=0, x1=V_selected, y1=max(df['총저항 (Rt)']) * 1.05,
            line=dict(color="#f97316", width=2, dash="dashdot"),
        )
        
        # 선택 속도 지점 데이터 풍선 띄우기
        fig.add_annotation(
            x=V_selected, y=res_selected['Rt'],
            text=f"선택 속도: {V_selected:.2f} kts ({res_selected['Rt']:.2f} kN)",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#f97316",
            ax=45, ay=-45,
            bgcolor="#ffedd5",
            bordercolor="#fed7aa",
            borderwidth=1,
            borderpad=4,
            font=dict(size=11, color="#7c2d12")
        )
        
        fig.update_layout(
            title=dict(
                text='선체 속도별 저항 구성 성분 분포',
                font=dict(family='Noto Sans KR', size=18, color='#0f172a')
            ),
            xaxis_title='선박 속력 (V) [knots]',
            yaxis_title='저항값 [kN]',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(248, 250, 252, 0.7)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=80, b=40),
            height=580
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='#e2e8f0', linecolor='#cbd5e1')
        fig.update_yaxes(showgrid=True, gridcolor='#e2e8f0', linecolor='#cbd5e1')
        
        st.plotly_chart(fig, use_container_width=True)
        
    # ----------------- 탭 2: 수치 표 -----------------
    with tab_table:
        st.subheader("속도 구간별 저항 계산 수치 데이터")
        st.write("아래 표는 선박 속도 증가에 따라 각 저항 성분이 어떻게 변화하는지 정량적으로 보여줍니다.")
        
        df_display = df.copy()
        df_display = df_display.round({
            '속도 (knots)': 2,
            '마찰저항 (Rf)': 2,
            '점성저항 (R_visc)': 2,
            '조파저항 (Rw)': 2,
            '구상선수저항 (Rb)': 2,
            '트랜섬저항 (Rtr)': 2,
            '부가물저항 (Rapp)': 2,
            '상관저항 (Ra)': 2,
            '총저항 (Rt)': 2,
            '유효동력 (kW)': 1
        })
        
        # 열 매핑 한글화
        df_display.columns = [
            '속력 [kts]', '마찰저항 Rf [kN]', '점성저항 R_visc [kN]',
            '조파저항 Rw [kN]', '구상선수저항 Rb [kN]', '트랜섬저항 Rtr [kN]',
            '부가물저항 Rapp [kN]', '상관수정 Ra [kN]', '총저항 Rt [kN]', '필요 유효동력 Pe [kW]'
        ]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
    # ----------------- 탭 3: 학술 논문급 저항 공식 해설 -----------------
    with tab_ref:
        st.subheader("Holtrop & Mennen (1982, 1984) 학술 연구 저항 공식 해설")
        st.write("이 대시보드 그래프에 반영된 각 저항 성분의 정밀 연산식은 Holtrop & Mennen의 원래 수학적 회귀 모델에 기반을 두고 있습니다. 각 성분의 수식과 원리는 다음과 같습니다.")
        
        st.markdown("---")
        
        # 1. Total Governing Equation
        st.markdown("### 1. 지배 방정식 (Governing Equation)")
        st.write("선박의 bare hull(부가물이 없는 상태) 및 부가물 장착 시의 총저항 $R_T$는 다음과 같이 정의됩니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_T = R_F (1 + k_1) + R_{APP} + R_W + R_B + R_{TR} + R_A$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $R_T$: 총저항 (Total Resistance)
        - $R_F$: 마찰저항 (Frictional Resistance)
        - $1 + k_1$: 선형 형상 계수 (Form Factor)
        - $R_{APP}$: 부가물 저항 (Appendage Resistance)
        - $R_W$: 조파저항 (Wave-making Resistance)
        - $R_B$: 구상선수 추가 저항 (Bulbous Bow Resistance)
        - $R_{TR}$: 트랜섬 선미 압력 저항 (Transom Stern Resistance)
        - $R_A$: 모형-실선 상관수정저항 (Correlation Allowance)
        """)
        
        st.markdown("---")
        
        # 2. Frictional Resistance
        st.markdown("### 2. 마찰 저항 (Frictional Resistance, $R_F$)")
        st.write("물과 선체 접촉면 사이의 점성으로 인해 발생하는 힘입니다. ITTC-1957(국제수조회의) 권장 마찰선 공식에 의한 마찰 항력 계수 $C_F$를 기초로 합니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_F = \\frac{1}{2} \\rho S V^2 C_F$$
        $$C_F = \\frac{0.075}{(\\log_{10}(Re) - 2)^2}$$
        $$Re = \\frac{V L_{bp}}{\\nu}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $\\rho$: 해수 밀도 ($1025 \\text{ kg/m}^3$)
        - $V$: 선속 (m/s)
        - $S$: 침수 표면적 ($\\text{m}^2$)
        - $Re$: 레이놀즈 수 (Reynolds Number)
        - $\\nu$: 해수 동점성 계수 ($1.188 \\times 10^{-6} \\text{ m}^2\\text{/s}$ at $15^\\circ\\text{C}$)
        """)
        st.write("침수 표면적 $S$는 Holtrop의 다음과 같은 회귀식으로 도출됩니다.")
        st.markdown("""
        <div class='math-block'>
        $$S = L_{bp} (2T + B)\\sqrt{C_m}(0.453 + 0.4425 C_b - 0.2862 C_m - 0.003467\\frac{B}{T} + 0.3696 C_{wp}) + \\frac{2.38 A_{BT}}{C_b}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $L_{bp}$: 선박 수선간장 (m)
        - $B$: 선폭 (m)
        - $T$: 흘수 (m)
        - $C_b$: 방형 비척 계수
        - $C_m$: 중앙단면 계수
        - $C_{wp}$: 수선면적 계수
        - $A_{BT}$: 구상선수 최대 횡단면적 ($\\text{m}^2$)
        """)
        
        st.markdown("---")
        
        # 3. Form Factor and Viscous Resistance
        st.markdown("### 3. 점성 저항 및 형상 계수 (Viscous Resistance & Form Factor, $1+k_1$)")
        st.write("선체 주위의 3차원 유동으로 인한 압력 저하와 선미 박리에 의한 저항을 고려하기 위해 마찰저항에 형상계수 $(1+k_1)$를 승산합니다.")
        st.markdown("""
        <div class='math-block'>
        $$1 + k_1 = 0.93 + 0.487118 \\cdot c_{14} \\cdot \\left(\\frac{B}{L_{bp}}\\right)^{1.06806} \\cdot \\left(\\frac{T}{L_{bp}}\\right)^{0.46106} \\cdot \\left(\\frac{L_{bp}}{L_R}\\right)^{0.12156} \\cdot \\left(\\frac{L_{bp}^3}{\\nabla}\\right)^{0.36486} \\cdot (1 - C_{wp})^{-0.60424}$$
        $$L_R = L_{bp} \\left( 1 - C_p + \\frac{0.06 C_p LCB}{4 C_p - 1} \\right)$$
        $$c_{14} = 1.0 + 0.011 \\cdot C_{stern}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $L_R$: 런의 길이 (Length of run, m)
        - $C_p$: 주형 비척 계수 (Prismatic Coefficient, $C_b/C_m$)
        - $LCB$: 종방향 부심 위치 (% Lbp)
        - $c_{14}$: 선미 형상 계수
        - $C_{stern}$: 선미 형상 매개변수 (U형 선형: $+10$, 중립: $0$, V형 선형: $-10$)
        - $\\nabla$: 배수 용적 (Displacement Volume, $\\text{m}^3$)
        """)
        
        st.markdown("---")
        
        # 4. Appendage Resistance
        st.markdown("### 4. 부가물 저항 (Appendage Resistance, $R_{APP}$)")
        st.write("타(Rudder), 빌지킬(Bilge Keel), 축계 등의 부가물이 유동을 방해하여 추가되는 마찰 및 형상 항력입니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_{APP} = \\frac{1}{2} \\rho V^2 S_{APP} C_{F} (1 + k_{app})$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $S_{APP}$: 부가물 총 침수 표면적 ($\\text{m}^2$)
        - $1 + k_{app}$: 부가물 형상 저항 증가계수
        """)
        
        st.markdown("---")
        
        # 5. Wave-making Resistance
        st.markdown("### 5. 조파 저항 (Wave-making Resistance, $R_W$)")
        st.write("선박이 주행하며 일으키는 파도계로 인해 선체 표면의 전후방에 압력차가 생기며 발생하는 저항입니다. Froude 수 ($F_n$)에 극도로 민감합니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_W = c_1 c_2 c_5 \\rho g \\nabla \\exp \\left[ m_1 F_n^{-0.9} + m_2 \\cos(\\lambda F_n^{-2}) \\right]$$
        $$c_1 = 2223105 \\cdot c_7^{3.78613} \\cdot \\left(\\frac{T}{B}\\right)^{1.07961} \\cdot (90 - i_E)^{-1.37565}$$
        $$F_n = \\frac{V}{\\sqrt{g L_{bp}}}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $g$: 중력 가속도 ($9.80665 \\text{ m/s}^2$)
        - $F_n$: 프루드 수 (Froude Number)
        - $c_1, m_1, m_2, \\lambda$: 선형 비 회귀 계수들
        - $c_2$: 구상선수 조파 감쇄 계수
        - $c_5$: 트랜섬 Stern 형상 계수
        """)
        st.write("선수 반각 $i_E$는 다음과 같은 지수 회귀 함수로 예측됩니다.")
        st.markdown("""
        <div class='math-block'>
        $$i_E = 1 + 89 \\exp \\left[ -\\left(\\frac{L_{bp}}{B}\\right)^{0.80856} (1-C_{wp})^{0.30484} (1-C_p-0.0225 LCB)^{0.6367} \\left(\\frac{L_R}{B}\\right)^{0.34574} \\left(\\frac{100\\nabla}{L_{bp}^3}\\right)^{0.16302} \\right]$$
        </div>
        """, unsafe_allow_html=True)
        st.write("구상선수 파도 소멸 보정 계수 $c_2$와 트랜섬 보정 계수 $c_5$는 다음과 같습니다.")
        st.markdown("""
        <div class='math-block'>
        $$c_2 = \\exp(-1.89 \\sqrt{c_3})$$
        $$c_3 = 0.56 \\frac{A_{BT}^{1.5}}{B T (0.56 \\sqrt{A_{BT}} + h_b)}$$
        $$c_5 = 1 - 0.8 \\frac{A_{trans}}{B T C_b}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $h_b$: 구상선수 중심 높이 (m)
        - $A_{trans}$: 트랜섬 침수 단면적 ($\\text{m}^2$)
        """)
        
        st.markdown("---")
        
        # 6. Bulbous Bow Resistance
        st.markdown("### 6. 구상선수 추가 저항 (Bulbous Bow Resistance, $R_B$)")
        st.write("구상선수가 생성하는 인위적인 파도와 자연 파도가 간섭하여 조파 저항은 감소되나, 벌브 자체에 물이 부딪히며 발생하는 추가 압력 항력 성분입니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_B = 0.11 \\cdot \\exp(-3 P_B^{-2}) \\cdot F_{ni}^3 \\cdot \\frac{A_{BT}^{1.5} \\rho g}{1 + F_{ni}^2}$$
        $$P_B = 0.56 \\frac{\\sqrt{A_{BT}}}{T - 1.5 h_b}$$
        $$F_{ni} = \\frac{V}{\\sqrt{g (T - h_b - 0.25 \\sqrt{A_{BT}}) + 0.15 V^2}}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $P_B$: 구상선수 돌출 출현 파라미터 (Emergence Parameter)
        - $F_{ni}$: 구상선수 기준 프루드 수 (Immersion Froude Number)
        """)
        
        st.markdown("---")
        
        # 7. Transom Stern Resistance
        st.markdown("### 7. 트랜섬 선미 압력 저항 (Transom Stern Resistance, $R_{TR}$)")
        st.write("선미 아랫부분이 각지게 잘려나간 트랜섬(Transom) 구조가 물속에 잠겨 있을 때, 박리 현상 및 수평 유동 단절로 인해 선미 쪽 압력이 회복되지 못해 생기는 음압 저항입니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_{TR} = \\frac{1}{2} \\rho V^2 A_{trans} c_6$$
        $$Fn_T = \\frac{V}{\\sqrt{\\frac{2 g A_{trans}}{B(1 + C_{wp})}}}$$
        $$c_6 = 0.2 (1 - 0.2 Fn_T) \\quad (\\text{for } Fn_T < 5)$$
        $$c_6 = 0 \\quad (\\text{for } Fn_T \\geq 5)$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $Fn_T$: 트랜섬 침수 프루드 수
        - $c_6$: 트랜섬 압력 저항 보정 계수
        """)
        
        st.markdown("---")
        
        # 8. Correlation Allowance
        st.markdown("### 8. 상관 수정 저항 (Correlation Allowance, $R_A$)")
        st.write("모형선 시험 결과를 실물 선박 크기로 확장(Scaling)할 때 발생하는 오차 보정치와 실제 선체의 거칠기(Welding bead, 마모 등)로 인한 추가 항력 계수 $C_A$에 기반합니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_A = \\frac{1}{2} \\rho S V^2 C_A$$
        $$C_A = 0.00351 \\cdot L_{bp}^{-0.3} - 0.00138$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **주요 매개변수 기호 설명:**
        - $C_A$: 모델-실선 상관 수정 계수
        """)

# 학술 출처 및 고지 푸터
st.markdown(
    """
    <div class='footer'>
        <strong>Reference:</strong> Holtrop, J., & Mennen, G. G. J. (1982). An approximate power prediction method. 
        <em>International Shipbuilding Progress</em>, 29(335), 166-170.<br>
        Holtrop, J. (1984). A statistical re-analysis of resistance and propulsion data. 
        <em>International Shipbuilding Progress</em>, 31(363), 272-276.
    </div>
    """,
    unsafe_allow_html=True
)
