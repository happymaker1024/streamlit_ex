import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# 페이지 설정
st.set_page_config(page_title="상품 관리 시스템", page_icon="🛒", layout="wide")

# MySQL 연결 함수
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'joy'),
        password=os.getenv('DB_PASSWORD', '1234'),
        database=os.getenv('DB_NAME', 'ecommerce_db'),
    )

# 상품 조회 (Read)
def get_products():
    conn = get_connection()
    query = "SELECT * FROM products ORDER BY id DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 상품 추가 (Create)
def add_product(name, category, price, stock, description):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO products (name, category, price, stock, description)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, category, price, stock, description))
    conn.commit()
    cursor.close()
    conn.close()

# 상품 수정 (Update)
def update_product(product_id, name, category, price, stock, description):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE products 
        SET name=%s, category=%s, price=%s, stock=%s, description=%s
        WHERE id=%s
    """
    cursor.execute(query, (name, category, price, stock, description, product_id))
    conn.commit()
    cursor.close()
    conn.close()

# 상품 삭제 (Delete)
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM products WHERE id=%s"
    cursor.execute(query, (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

# 메인 앱
def main():
    st.title("🛒 E-커머스 상품 관리 시스템")
    
    # 사이드바 메뉴
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["상품 목록 조회", "상품 추가", "상품 수정", "상품 삭제"]
    )
    
    st.sidebar.divider()
    st.sidebar.info("📌 MySQL 8.4 + PyMySQL 사용")
    
    # 1. 상품 목록 조회
    if menu == "상품 목록 조회":
        st.header("📋 전체 상품 목록")
        
        try:
            df = get_products()
            
            if df.empty:
                st.warning("등록된 상품이 없습니다.")
            else:
                st.dataframe(df, use_container_width=True)
                st.success(f"총 {len(df)}개의 상품이 등록되어 있습니다.")
                
                # 통계 정보
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 상품 수", len(df))
                with col2:
                    st.metric("총 재고", df['stock'].sum())
                with col3:
                    st.metric("평균 가격", f"₩{df['price'].mean():,.0f}")
                    
        except Exception as e:
            st.error(f"오류 발생: {e}")
    
    # 2. 상품 추가
    elif menu == "상품 추가":
        st.header("➕ 새 상품 추가")
        
        with st.form("add_product_form"):
            name = st.text_input("상품명", placeholder="예: 스마트폰")
            category = st.selectbox(
                "카테고리",
                ["전자제품", "가구", "의류", "식품", "도서", "기타"]
            )
            price = st.number_input("가격 (원)", min_value=0, step=1000)
            stock = st.number_input("재고 수량", min_value=0, step=1)
            description = st.text_area("상품 설명", placeholder="상품에 대한 설명을 입력하세요")
            
            submitted = st.form_submit_button("상품 추가")
            
            if submitted:
                if name and price > 0:
                    try:
                        add_product(name, category, price, stock, description)
                        st.success(f"✅ '{name}' 상품이 성공적으로 추가되었습니다!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"오류 발생: {e}")
                else:
                    st.warning("상품명과 가격은 필수 입력 항목입니다.")
    
    # 3. 상품 수정
    elif menu == "상품 수정":
        st.header("✏️ 상품 정보 수정")
        
        try:
            df = get_products()
            
            if df.empty:
                st.warning("수정할 상품이 없습니다.")
            else:
                # 상품 선택
                product_list = df['name'].tolist()
                product_ids = df['id'].tolist()
                
                selected_product = st.selectbox(
                    "수정할 상품 선택",
                    product_list
                )
                
                # 선택한 상품의 인덱스 찾기
                selected_index = product_list.index(selected_product)
                selected_id = product_ids[selected_index]
                
                # 현재 상품 정보 가져오기
                current_product = df[df['id'] == selected_id].iloc[0]
                
                st.divider()
                
                with st.form("update_product_form"):
                    name = st.text_input("상품명", value=current_product['name'])
                    category = st.selectbox(
                        "카테고리",
                        ["전자제품", "가구", "의류", "식품", "도서", "기타"],
                        index=["전자제품", "가구", "의류", "식품", "도서", "기타"].index(current_product['category']) if current_product['category'] in ["전자제품", "가구", "의류", "식품", "도서", "기타"] else 5
                    )
                    price = st.number_input("가격 (원)", min_value=0.0,  value=float(current_product['price']), step=1000.0)
                    stock = st.number_input("재고 수량", min_value=0, value=int(current_product['stock']), step=1)
                    description = st.text_area("상품 설명", value=current_product['description'] if pd.notna(current_product['description']) else "")
                    
                    submitted = st.form_submit_button("수정 완료")
                    
                    if submitted:
                        try:
                            update_product(selected_id, name, category, price, stock, description)
                            st.success(f"✅ '{name}' 상품 정보가 수정되었습니다!")
                        except Exception as e:
                            st.error(f"오류 발생: {e}")
                            
        except Exception as e:
            st.error(f"오류 발생: {e}")
    
    # 4. 상품 삭제
    elif menu == "상품 삭제":
        st.header("🗑️ 상품 삭제")
        
        try:
            df = get_products()
            
            if df.empty:
                st.warning("삭제할 상품이 없습니다.")
            else:
                # 상품 선택
                product_list = df['name'].tolist()
                product_ids = df['id'].tolist()
                
                selected_product = st.selectbox(
                    "삭제할 상품 선택",
                    product_list
                )
                
                selected_index = product_list.index(selected_product)
                selected_id = product_ids[selected_index]
                
                # 선택한 상품 정보 표시
                current_product = df[df['id'] == selected_id].iloc[0]
                
                st.divider()
                st.write("**삭제할 상품 정보:**")
                st.write(f"- 상품명: {current_product['name']}")
                st.write(f"- 카테고리: {current_product['category']}")
                st.write(f"- 가격: ₩{current_product['price']:,.0f}")
                st.write(f"- 재고: {current_product['stock']}개")
                
                st.divider()
                
                # 삭제 확인
                confirm = st.checkbox("정말로 이 상품을 삭제하시겠습니까?")
                
                if st.button("삭제하기", type="primary", disabled=not confirm):
                    try:
                        delete_product(selected_id)
                        st.success(f"✅ '{selected_product}' 상품이 삭제되었습니다!")
                        st.rerun()  # 페이지 새로고침
                    except Exception as e:
                        st.error(f"오류 발생: {e}")
                        
        except Exception as e:
            st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()