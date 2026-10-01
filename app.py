import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write("Tính tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP DỮ LIỆU
# =========================

st.subheader("📋 Thông tin tiền gửi")

# Số tiền gửi
principal = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

# Kỳ hạn
term = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

# Hình thức tính lãi
interest_type = st.radio(
    "Hình thức tính lãi",
    ["Lãi đơn", "Lãi kép"],
    horizontal=True
)

# Hình thức nhận lãi
payment_type = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# Lãi suất
interest_rate = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if principal <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if interest_rate < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    annual_rate = interest_rate / 100

    # Thời gian tính theo năm
    years = term / 12

    # ---------------------------------
    # Xác định số kỳ nhận lãi
    # ---------------------------------
    if payment_type == "Lãnh lãi hàng tháng":
        periods = term
        rate_per_period = annual_rate / 12

    elif payment_type == "Lãnh lãi hàng quý":
        periods = term / 3
        rate_per_period = annual_rate / 4

    else:
        periods = years
        rate_per_period = annual_rate

    # ---------------------------------
    # LÃI ĐƠN
    # ---------------------------------
    if interest_type == "Lãi đơn":

        # Tổng lãi
        total_interest = principal * annual_rate * years

        # Lãi mỗi kỳ
        periodic_interest = total_interest / periods

        # Tổng tiền cuối kỳ
        total_amount = principal + total_interest

        # ---------------------------------
        # LÃI KÉP
        # ---------------------------------
    else:

        # Lãi kép:
        # A = P(1+r)^n
        total_amount = principal * (
            (1 + rate_per_period) ** periods
        )

        total_interest = total_amount - principal

        # Lãi trung bình theo từng kỳ
        # (dùng để hiển thị tham khảo)
        periodic_interest = total_interest / periods

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.success("✅ Tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(periodic_interest)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(total_interest)
        )

    st.metric(
        "💰 Tổng tiền gốc + lãi",
        format_money(total_amount)
    )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================

    st.divider()

    st.subheader("📝 Chi tiết khoản gửi")

    st.write(f"**Số tiền gốc:** {format_money(principal)}")
    st.write(f"**Kỳ hạn:** {term} tháng")
    st.write(f"**Lãi suất:** {interest_rate:.2f}%/năm")
    st.write(f"**Hình thức:** {interest_type}")
    st.write(f"**Nhận lãi:** {payment_type}")

    # =========================
    # GIẢI THÍCH
    # =========================

    with st.expander("ℹ️ Xem cách tính"):

        if interest_type == "Lãi đơn":

            st.markdown("""
            ### Lãi đơn

            Tiền lãi được tính dựa trên **số tiền gốc ban đầu**.

            **Công thức:**

            `Tiền lãi = Tiền gốc × Lãi suất năm × Số năm`

            Tiền lãi không được nhập thêm vào vốn để tiếp tục sinh lãi.
            """)

        else:

            st.markdown("""
            ### Lãi kép

            Tiền lãi được cộng vào vốn, sau đó tiếp tục sinh ra
            tiền lãi ở các kỳ tiếp theo.

            **Công thức:**

            `A = P × (1 + r)^n`

            Trong đó:

            - `P`: Tiền gốc
            - `r`: Lãi suất mỗi kỳ
            - `n`: Số kỳ
            - `A`: Tổng tiền nhận được
            """)

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "💡 Công cụ mang tính chất tham khảo. "
    "Lãi suất thực tế của ngân hàng có thể áp dụng các quy định khác."
)
