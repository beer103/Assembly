import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Assembly QR", page_icon="🤖")

query_params = st.query_params
part = query_params.get("part", "76809-89402D")
robot = query_params.get("Robot", "RB134")
substation = query_params.get("Sub", "5")

st.title("📦 ระบบบันทึกงาน Assembly")

with st.form("log_form"):
    st.markdown("### 🔍 ตรวจเช็คข้อมูล")
    st.text_input("📦 Part", part, disabled=True)
    st.text_input("🤖 Robot", robot, disabled=True)
    st.text_input("📍 Substation", substation, disabled=True)

    name = st.text_input("👤 กรอกชื่อพนักงาน")

    submitted = st.form_submit_button("✅ บันทึกข้อมูล")

    if submitted:
        if name.strip() == "":
            st.error("❗ กรุณากรอกชื่อก่อน")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = pd.DataFrame([[now, name, part, robot, substation]],
                              columns=["Timestamp", "Name", "Part", "Robot", "Substation"])
            df.to_csv("log.csv", mode='a', header=False, index=False)
            st.success("📌 บันทึกสำเร็จ!")
import io

# โหลดข้อมูล log.csv ถ้ามี
if pd.io.common.file_exists("log.csv"):
    log_df = pd.read_csv("log.csv")

    # สร้าง buffer เก็บ Excel ไฟล์
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        log_df.to_excel(writer, index=False, sheet_name='Log')
        writer.save()
    buffer.seek(0)

    # ปุ่มดาวน์โหลด Excel
    st.download_button(
        label="⬇️ ดาวน์โหลด Excel (log.xlsx)",
        data=buffer,
        file_name="log.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("📭 ยังไม่มีข้อมูลใน log.csv")