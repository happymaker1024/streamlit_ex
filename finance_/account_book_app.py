import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime, date
from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv(override=True)

# 페이지 설정
st.set_page_config(page_title="나의 가계부", page_icon="💰", layout="wide")

# MySQL 연결
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'joy'),
        password=os.getenv('DB_PASSWORD', '1234'),
        database=os.getenv('DB_NAME', 'finance_db'),
        charset='utf8mb4'
    )

# 모든 거래 조회
def get_all_transactions():
    conn = get_connection()
    query = "SELECT * FROM transactions ORDER BY date DESC, id DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 거래 추가
def add_transaction(trans_date, category, description, amount, trans_type):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (trans_date, category, description, amount, trans_type))
    conn.commit()
    cursor.close()
    conn.close()

# 거래 삭제
def delete_transaction(trans_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM transactions WHERE id=%s"
    cursor.execute(query, (trans_id,))
    conn.commit()
    cursor.close()
    conn.close()

# 메인 앱
def main():
    st.title("💰 나의 가계부")
    st.write("간단하게 수입과 지출을 관리해보세요!")
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📊 내역 보기", "➕ 추가하기", "🗑️ 삭제하기"])
    
    # 탭 1: 거래 내역 보기
    with tab1:
        st.header("💳 거래 내역")
        
        try:
            df = get_all_transactions()
            
            if df.empty:
                st.info("아직 등록된 거래가 없습니다. '추가하기' 탭에서 거래를 등록해보세요!")
            else:
                # 전체 내역 표시
                st.dataframe(df, use_container_width=True)
                
                st.divider()
                
                # 통계 정보
                st.subheader("📈 이번 달 요약")
                
                col1, col2, col3 = st.columns(3)
                
                # 수입 계산
                income = df[df['type'] == '수입']['amount'].sum()
                with col1:
                    st.metric("총 수입", f"₩{income:,}")
                
                # 지출 계산
                expense = df[df['type'] == '지출']['amount'].sum()
                with col2:
                    st.metric("총 지출", f"₩{expense:,}")
                
                # 잔액 계산
                balance = income - expense
                with col3:
                    st.metric("잔액", f"₩{balance:,}", 
                             delta=f"₩{balance:,}" if balance >= 0 else f"-₩{abs(balance):,}")
                
                st.divider()
                
                # 카테고리별 지출
                st.subheader("🏷️ 카테고리별 지출")
                expense_df = df[df['type'] == '지출']
                if not expense_df.empty:
                    category_sum = expense_df.groupby('category')['amount'].sum().reset_index()
                    category_sum = category_sum.sort_values('amount', ascending=False)
                    st.bar_chart(category_sum.set_index('category'))
                else:
                    st.info("지출 내역이 없습니다.")
                    
        except Exception as e:
            st.error(f"오류 발생: {e}")
    
    # 탭 2: 거래 추가
    with tab2:
        st.header("➕ 새 거래 추가")
        
        with st.form("add_transaction_form"):
            # 날짜 선택
            trans_date = st.date_input("날짜", value=date.today())
            
            # 수입/지출 선택
            trans_type = st.radio("구분", ["수입", "지출"], horizontal=True)
            
            # 카테고리 선택 (수입/지출에 따라 다름)
            if trans_type == "수입":
                categories = ["월급", "용돈", "상여금", "투자수익", "기타수입"]
            else:
                categories = ["식비", "교통", "쇼핑", "공과금", "통신비", "의료", "기타지출"]
            
            category = st.selectbox("카테고리", categories)
            
            # 설명
            description = st.text_input("내용", placeholder="예: 편의점, 지하철 등")
            
            # 금액
            amount = st.number_input("금액 (원)", min_value=0, step=1000)
            
            # 제출 버튼
            submitted = st.form_submit_button("추가하기", use_container_width=True)
        
        if submitted:
            if amount > 0:
                try:
                    add_transaction(trans_date, category, description, amount, trans_type)
                    st.success(f"✅ {trans_type} {amount:,}원이 추가되었습니다!")
                    st.balloons()
                except Exception as e:
                    st.error(f"오류 발생: {e}")
            else:
                st.warning("금액을 입력해주세요!")
    
    # 탭 3: 거래 삭제
    with tab3:
        st.header("🗑️ 거래 삭제")
        
        try:
            df = get_all_transactions()
            
            if df.empty:
                st.info("삭제할 거래가 없습니다.")
            else:
                # 삭제할 거래 선택
                st.write("삭제할 거래를 선택하세요:")
                
                # 거래 목록 표시 (날짜, 카테고리, 내용, 금액)
                df['display'] = df.apply(
                    lambda x: f"{x['date']} | {x['type']} | {x['category']} | {x['description']} | ₩{x['amount']:,}", 
                    axis=1
                )
                
                selected_display = st.selectbox(
                    "거래 선택",
                    df['display'].tolist()
                )
                
                # 선택한 거래의 ID 찾기
                selected_id = df[df['display'] == selected_display]['id'].iloc[0]
                selected_row = df[df['id'] == selected_id].iloc[0]
                
                st.divider()
                
                # 선택한 거래 정보 표시
                st.write("**삭제할 거래 정보:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"📅 날짜: {selected_row['date']}")
                    st.write(f"🏷️ 카테고리: {selected_row['category']}")
                with col2:
                    st.write(f"💰 금액: ₩{selected_row['amount']:,}")
                    st.write(f"📝 내용: {selected_row['description']}")
                
                st.divider()
                
                # 삭제 확인
                col1, col2 = st.columns([3, 1])
                with col1:
                    confirm = st.checkbox("정말로 삭제하시겠습니까?")
                with col2:
                    if st.button("삭제", type="primary", disabled=not confirm, use_container_width=True):
                        try:
                            delete_transaction(selected_id)
                            st.success("✅ 삭제되었습니다!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"오류 발생: {e}")
                            
        except Exception as e:
            st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()