import streamlit as st
import os
import json
import mammoth  # pip install mammoth

# ==========================================
# 1. 基础配置与数据结构
# ==========================================
st.set_page_config(page_title="2025 Event Platform", layout="wide", initial_sidebar_state="collapsed")

DATA_FILE = "campaigns.json"
ADMIN_PASSWORD = "123456"  # 🔐 管理员密码

# 预设语言
LANGUAGES = {
    "en": "English",
    "zh": "简体中文",
    "ms": "Bahasa Melayu"
}

# --- 数据读写函数 ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 加载数据
campaigns_db = load_data()

# ==========================================
# 2. 逻辑分流 (路由控制)
# ==========================================

# 获取 URL 里的参数 (?id=xxx)
query_params = st.query_params
# 兼容不同版本的 Streamlit 获取方式
campaign_id = query_params.get("id", None)
if isinstance(campaign_id, list): campaign_id = campaign_id[0]

# ==========================================
# 3. 场景 A: 客户看到的页面 (纯净版)
# ==========================================
if campaign_id:
    # 隐藏自带的菜单汉堡按钮和页脚，做到极致纯净
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
            .stAppHeader {display: none;} 
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # 检查活动是否存在
    if campaign_id not in campaigns_db:
        st.error("❌ 找不到该活动页面 (Campaign Not Found)")
        st.stop()

    data = campaigns_db[campaign_id]

    # --- 渲染客户页面 ---
    
    # 1. Banner (如果有上传)
    banner_file = f"assets/{campaign_id}_banner.png"
    if os.path.exists(banner_file):
        st.image(banner_file, use_container_width=True)
    else:
        # 如果没有专属Banner，显示标题
        st.title(data.get("title", "Event Page"))

    st.divider()

    # 2. 语言切换
    col_lang, _ = st.columns([1, 3])
    with col_lang:
        selected_lang = st.selectbox("🌐 Language", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])

    # 3. 内容展示 (HTML)
    content = data["content"].get(selected_lang, "")
    
    # CSS 美化表格
    st.markdown("""
    <style>
        table {width: 100%; border-collapse: collapse; border: 1px solid #ddd;}
        th, td {border: 1px solid #ddd; padding: 8px;}
        th {background-color: #f2f2f2;}
    </style>
    """, unsafe_allow_html=True)

    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.info("No content available for this language.")

# ==========================================
# 4. 场景 B: 管理员后台 (Admin Only)
# ==========================================
else:
    # 只有在没有 ?id=xxx 的时候，才会显示后台登录界面
    
    st.title("⚙️ Campaign Manager System")
    
    # --- 登录锁 ---
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        pwd = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Wrong password")
        st.stop()

    # --- 登录后的控制台 ---
    
    st.sidebar.header("管理菜单")
    menu = st.sidebar.radio("Menu", ["📦 活动列表 (Campaigns)", "➕ 新建活动 (Create New)"])

    if menu == "➕ 新建活动 (Create New)":
        st.subheader("Create New Campaign")
        new_id = st.text_input("设置 ID (英文/数字, 例如: xmas2025)").strip()
        new_title = st.text_input("活动标题 (内部备注)")
        
        if st.button("Create"):
            if not new_id:
                st.error("ID 不能为空")
            elif new_id in campaigns_db:
                st.error("ID 已存在！")
            else:
                campaigns_db[new_id] = {
                    "title": new_title,
                    "content": {l: "" for l in LANGUAGES} # 初始化空内容
                }
                save_data(campaigns_db)
                st.success(f"创建成功！ID: {new_id}")
                st.rerun()

    elif menu == "📦 活动列表 (Campaigns)":
        # 选择要编辑的活动
        all_ids = list(campaigns_db.keys())
        if not all_ids:
            st.info("还没有任何活动，请去新建一个。")
            st.stop()
            
        target_id = st.selectbox("选择要编辑的活动 / Select Campaign", all_ids)
        current_data = campaigns_db[target_id]

        st.divider()
        st.markdown(f"### 正在编辑: **{current_data['title']}**")
        
        # === 核心功能：生成专属链接 ===
        # 这里自动获取当前的基础网址，加上 ?id=xxx
        # 注意：本地测试是 localhost，上线后会自动变成你的域名
        base_url = "http://localhost:8501" # ⚠️ 上线后这里会自动变，或者你可以手动改为你的域名
        full_url = f"?id={target_id}"
        
        st.info(f"🔗 **客户专属链接 (发送这个给客户):**")
        st.code(f"{base_url}/{full_url}", language="text")
        st.caption("提示：在 Streamlit Cloud 上，把 localhost 换成你的 .app 网址即可。")

        # === 1. 上传该活动的 Banner ===
        st.write("#### 1. 上传 Banner")
        banner_up = st.file_uploader("Upload Banner (PNG/JPG)", type=["png", "jpg"], key=f"b_{target_id}")
        if banner_up:
            # 确保 assets 文件夹存在
            if not os.path.exists("assets"): os.makedirs("assets")
            # 保存为特定名字: assets/campaign1_banner.png
            save_path = f"assets/{target_id}_banner.png"
            with open(save_path, "wb") as f:
                f.write(banner_up.getbuffer())
            st.success("Banner 已更新！")
            st.image(save_path, width=300)

        # === 2. 编辑内容 (Word 上传) ===
        st.write("#### 2. 编辑 Terms & Content")
        edit_lang = st.radio("选择语言", list(LANGUAGES.keys()), horizontal=True, format_func=lambda x: LANGUAGES[x])
        
        word_file = st.file_uploader(f"上传 Word 文档 ({LANGUAGES[edit_lang]})", type=["docx"], key=f"w_{target_id}")
        
        if word_file and st.button("🔄 转换并保存内容"):
            result = mammoth.convert_to_html(word_file)
            html = result.value
            if html:
                campaigns_db[target_id]["content"][edit_lang] = html
                save_data(campaigns_db)
                st.success("内容已保存！")
                st.rerun()
            else:
                st.error("内容为空，请检查文本框问题。")

        # 预览当前内容
        with st.expander("👀 预览当前内容代码"):
            st.text(campaigns_db[target_id]["content"].get(edit_lang, "")[:200] + "...")