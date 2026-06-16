import streamlit as st
import numpy as np
import pandas as pd
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 0.5rem;
            font-family: 'Outfit', sans-serif;
        }
        
        /* 커스텀 하단 푸터 */
    st.markdown("<br>", unsafe_allow_html=True)
    # 탭 메뉴
    tab_dashboard, tab_table, tab_ref = st.tabs(["📊 성능 그래프 분석", "📋 속도별 상세 데이터", "📖 Holtrop & Mennen Formulation"])
    tab_dashboard, tab_table, tab_ref = st.tabs(["📊 성능 그래프 분석", "📋 속도별 상세 데이터", "📖 학술 논문급 저항 공식 해설"])
    # ----------------- 탭 1: 대시보드 그래프 -----------------
    with tab_dashboard:
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    # ----------------- 탭 3: 학술 논문급 저항 공식 해설 (영어 원문) -----------------
    # ----------------- 탭 3: 학술 논문급 저항 공식 해설 (순수 수식) -----------------
    with tab_ref:
        st.subheader("Holtrop & Mennen (1982, 1984) Resistance Estimation Formulation")
        st.write("The exact mathematical regression formulas implemented in this calculator are presented below in their original scientific format, based on the statistical regression analysis conducted at MARIN.")
        st.subheader("Holtrop & Mennen (1982, 1984) 학술 연구 저항 공식 해설")
        st.write("이 대시보드 그래프에 반영된 각 저항 성분의 정밀 연산식은 Holtrop & Mennen의 원래 수학적 회귀 모델에 기반을 두고 있습니다. 각 성분의 수식과 원리는 다음과 같습니다.")
        
        st.markdown("---")
        
        # 1. Total Governing Equation
        st.markdown("### 1. Governing Equation")
        st.write("The total bare-hull and appended resistance $R_T$ of the ship is defined as:")
        # 1. 전체 지배 방정식
        st.markdown("### 1. 지배 방정식 (Governing Equation)")
        st.write("선박의 bare hull(부가물이 없는 상태) 및 부가물 장착 시의 총저항 $R_T$는 다음과 같이 정의됩니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_T = R_F (1 + k_1) + R_{APP} + R_W + R_B + R_{TR} + R_A$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Nomenclature:**
        - $R_T$: Total resistance
        - $R_F$: Frictional resistance according to the ITTC-1957 line
        - $1 + k_1$: Three-dimensional form factor of the hull
        - $R_{APP}$: Appendage resistance
        - $R_W$: Wave-making and wave-breaking resistance
        - $R_B$: Additional pressure resistance of a bulbous bow near the water surface
        - $R_{TR}$: Additional pressure resistance of an immersed transom stern
        - $R_A$: Model-ship correlation allowance (roughness and scaling correction)
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
        st.markdown("### 2. Frictional Resistance ($R_F$)")
        st.write("The frictional drag represents the shear force acting along the wetted surface of the ship hull. It is calculated using the ITTC-1957 friction correlation line:")
        # 2. 마찰 저항
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
        **Nomenclature:**
        - $\\rho$: Density of water ($1025 \\text{ kg/m}^3$ for seawater)
        - $V$: Vessel speed through water (m/s)
        - $S$: Total wetted surface area ($\\text{m}^2$)
        - $Re$: Reynolds number
        - $\\nu$: Kinematic viscosity of seawater ($1.188 \\times 10^{-6} \\text{ m}^2\\text{/s}$ at $15^\\circ\\text{C}$)
        **주요 매개변수 기호 설명:**
        - $\\rho$: 해수 밀도 ($1025 \\text{ kg/m}^3$)
        - $V$: 선속 (m/s)
        - $S$: 침수 표면적 ($\\text{m}^2$)
        - $Re$: 레이놀즈 수 (Reynolds Number)
        - $\\nu$: 해수 동점성 계수 ($1.188 \\times 10^{-6} \\text{ m}^2\\text{/s}$ at $15^\\circ\\text{C}$)
        """)
        st.write("The wetted surface area $S$ is calculated using Holtrop's regression formula:")
        st.write("침수 표면적 $S$는 Holtrop의 다음과 같은 회귀식으로 도출됩니다.")
        st.markdown("""
        <div class='math-block'>
        $$S = L_{bp} (2T + B)\\sqrt{C_m}(0.453 + 0.4425 C_b - 0.2862 C_m - 0.003467\\frac{B}{T} + 0.3696 C_{wp}) + \\frac{2.38 A_{BT}}{C_b}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Nomenclature:**
        - $L_{bp}$: Length between perpendiculars (m)
        - $B$: Moulded breadth (m)
        - $T$: Moulded draft (m)
        - $C_b$: Block coefficient
        - $C_m$: Midship section coefficient
        - $C_{wp}$: Waterplane area coefficient
        - $A_{BT}$: Transverse cross-sectional area of bulbous bow ($\\text{m}^2$)
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
        st.markdown("### 3. Viscous Resistance & Form Factor ($1+k_1$)")
        st.write("The form factor $(1+k_1)$ accounts for the three-dimensional flow effects (viscous pressure drag due to boundary layer thickening and separation at the aft body). Frictional resistance is scaled by this factor to yield total viscous resistance:")
        # 3. 형상 계수 및 점성 저항
        st.markdown("### 3. 점성 저항 및 형상 계수 (Viscous Resistance & Form Factor, $1+k_1$)")
        st.write("선체 주위의 3차원 유동으로 인한 압력 저하와 선미 박리에 의한 저항을 고려하기 위해 마찰저항에 형상계수 $(1+k_1)$를 승산합니다.")
        st.markdown("""
        <div class='math-block'>
        $$1 + k_1 = 0.93 + 0.487118 \\cdot c_{14} \\cdot \\left(\\frac{B}{L_{bp}}\\right)^{1.06806} \\cdot \\left(\\frac{T}{L_{bp}}\\right)^{0.46106} \\cdot \\left(\\frac{L_{bp}}{L_R}\\right)^{0.12156} \\cdot \\left(\\frac{L_{bp}^3}{\\nabla}\\right)^{0.36486} \\cdot (1 - C_{wp})^{-0.60424}$$
        $$L_R = L_{bp} \\left( 1 - C_p + \\frac{0.06 C_p LCB}{4 C_p - 1} \\right)$$
        $$c_{14} = 1.0 + 0.011 \\cdot C_{stern}$$
        $$c_{14} = 1.0 + 0.011 * C_{stern}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Nomenclature:**
        - $L_R$: Length of run (m)
        - $C_p$: Prismatic coefficient ($C_b/C_m$)
        - $LCB$: Longitudinal center of buoyancy (percentage of $L_{bp}$ forward of amidships, e.g. +2.5%)
        - $c_{14}$: Stern shape factor parameter
        - $C_{stern}$: Stern shape parameter (U-shape stern sections: $+10$, normal sections: $0$, V-shape sections: $-10$)
        - $\\nabla$: Displacement volume ($\\text{m}^3$)
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
        st.markdown("### 4. Appendage Resistance ($R_{APP}$)")
        st.write("Appendage resistance represents the viscous and form drag added by devices external to the main hull girder, such as rudders, shafts, bilge keels, and struts:")
        # 4. 부가물 저항
        st.markdown("### 4. 부가물 저항 (Appendage Resistance, $R_{APP}$)")
        st.write("타(Rudder), 빌지킬(Bilge Keel), 축계 등의 부가물이 유동을 방해하여 추가되는 마찰 및 형상 항력입니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_{APP} = \\frac{1}{2} \\rho V^2 S_{APP} C_{F} (1 + k_{app})$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Nomenclature:**
        - $S_{APP}$: Wetted surface area of appendages ($\\text{m}^2$)
        - $1 + k_{app}$: Drag allowance factor of appendages
        **주요 매개변수 기호 설명:**
        - $S_{APP}$: 부가물 총 침수 표면적 ($\\text{m}^2$)
        - $1 + k_{app}$: 부가물 형상 저항 증가계수
        """)
        st.markdown("---")
        # 5. Wave-making Resistance
        st.markdown("### 5. Wave-making Resistance ($R_W$)")
        st.write("Wave-making resistance represents the energy dissipation associated with the generation of gravity wave systems at the free surface. It is calculated using the following regression formulation for Froude numbers $F_n < 0.4$:")
        # 5. 조파 저항
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
        **Nomenclature:**
        - $g$: Acceleration due to gravity ($9.80665 \\text{ m/s}^2$)
        - $F_n$: Froude number
        - $c_1, m_1, m_2, \\lambda$: Empirical coefficients and exponents
        - $c_2$: Bulbous bow wave-making reduction factor
        - $c_5$: Transom stern wave-making reduction factor
        **주요 매개변수 기호 설명:**
        - $g$: 중력 가속도 ($9.80665 \\text{ m/s}^2$)
        - $F_n$: 프루드 수 (Froude Number)
        - $c_1, m_1, m_2, \\lambda$: 선형 비 회귀 계수들
        - $c_2$: 구상선수 조파 감쇄 계수
        - $c_5$: 트랜섬 Stern 형상 계수
        """)
        st.write("The half-angle of entrance $i_E$ (in degrees) is calculated using hull particulars as follows:")
        st.write("선수 반각 $i_E$는 다음과 같은 지수 회귀 함수로 예측됩니다.")
        st.markdown("""
        <div class='math-block'>
        $$i_E = 1 + 89 \\exp \\left[ -\\left(\\frac{L_{bp}}{B}\\right)^{0.80856} (1-C_{wp})^{0.30484} (1-C_p-0.0225 LCB)^{0.6367} \\left(\\frac{L_R}{B}\\right)^{0.34574} \\left(\\frac{100\\nabla}{L_{bp}^3}\\right)^{0.16302} \\right]$$
        </div>
        """, unsafe_allow_html=True)
        st.write("The bulbous bow correction coefficient $c_2$ and the transom stern correction coefficient $c_5$ are calculated as:")
        st.write("구상선수 파도 소멸 보정 계수 $c_2$와 트랜섬 보정 계수 $c_5$는 다음과 같습니다.")
        st.markdown("""
        <div class='math-block'>
        $$c_2 = \\exp(-1.89 \\sqrt{c_3})$$
        $$c_3 = 0.56 \\frac{A_{BT}^{1.5}}{B T (0.56 \\sqrt{A_{BT}} + h_b)}$$
        $$c_5 = 1 - 0.8 \\frac{A_{trans}}{B T C_b}$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Nomenclature:**
        - $h_b$: Height of center of bulb area above keel (m)
        - $A_{trans}$: Immersed transom stern area at zero speed ($\\text{m}^2$)
        **주요 매개변수 기호 설명:**
        - $h_b$: 구상선수 중심 높이 (m)
        - $A_{trans}$: 트랜섬 침수 단면적 ($\\text{m}^2$)
        """)
        st.markdown("---")
        # 6. Bulbous Bow Resistance
        st.markdown("### 6. Bulbous Bow Additional Resistance ($R_B$)")
        st.write("The bulbous bow generates a wave system that interferes destructively with the bow wave system, reducing wave resistance. However, it also introduces an additional pressure resistance term $R_B$ due to local flow stagnation:")
        # 6. 구상선수 저항
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
        **Nomenclature:**
        - $P_B$: Bulb emergence parameter (characterizing the bulb's distance to the waterplane)
        - $F_{ni}$: Immersion Froude number based on the bulb's vertical position
        **주요 매개변수 기호 설명:**
        - $P_B$: 구상선수 돌출 출현 파라미터 (Emergence Parameter)
        - $F_{ni}$: 구상선수 기준 프루드 수 (Immersion Froude Number)
        """)
        st.markdown("---")
        # 7. Transom Stern Resistance
        st.markdown("### 7. Transom Stern Additional Resistance ($R_{TR}$)")
        st.write("The transom stern resistance accounts for the loss of pressure recovery (negative pressure drag) behind an immersed transom stern chine due to flow separation:")
        # 7. 트랜섬 저항
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
        **Nomenclature:**
        - $Fn_T$: Transom Froude number based on transom immersion depth
        - $c_6$: Transom pressure drag coefficient
        **주요 매개변수 기호 설명:**
        - $Fn_T$: 트랜섬 침수 프루드 수
        - $c_6$: 트랜섬 압력 저항 보정 계수
        """)
        st.markdown("---")
        # 8. Correlation Allowance
        st.markdown("### 8. Model-Ship Correlation Allowance ($R_A$)")
        st.write("The model-ship correlation allowance accounts for the scaling discrepancies between model tests and full-scale trials (e.g. boundary layer thickness differences) and the average hull surface roughness of a new ship (standardized at 150 µm):")
        # 8. 상관 수정 저항
        st.markdown("### 8. 상관 수정 allowance (Correlation Allowance, $R_A$)")
        st.write("모형선 시험 결과를 실물 선박 크기로 확장(Scaling)할 때 발생하는 오차 보정치와 실제 선체의 거칠기(Welding bead, 마모 등)로 인한 추가 항력 계수 $C_A$에 기반합니다.")
        st.markdown("""
        <div class='math-block'>
        $$R_A = \\frac{1}{2} \\rho S V^2 C_A$$
        $$C_A = 0.00351 \\cdot L_{bp}^{-0.3} - 0.00138$$
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Nomenclature:**
        - $C_A$: Model-ship correlation allowance coefficient
        **주요 매개변수 기호 설명:**
        - $C_A$: 모델-실선 상관 수정 계수
        """)
