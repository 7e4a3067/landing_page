import streamlit as st
import os
import json
import mammoth  # 必须安装: pip install mammoth

# ==========================================
# 1. 基础配置与数据管理
# ==========================================

st.set_page_config(page_title="2025 Python Summit", layout="wide")

# 文件路径配置
DATA_FILE = "tnc_data.json"
LANG_CONFIG_FILE = "languages.json"

# 预设的 20+ 种语言
DEFAULT_LANGUAGES = {
    "zh": "Chinese (Simplified) - 简体中文",
    "en": "English - 英语",
    "ms": "Malay - 马来语",
    "th": "Thai - 泰语",
    "vi": "Vietnamese - 越南语",
    "id": "Indonesian - 印尼语",
    "ja": "Japanese - 日语",
    "ko": "Korean - 韩语",
    "tl": "Tagalog - 菲律宾语",
    "hi": "Hindi - 印地语",
    "es": "Spanish - 西班牙语",
    "pt": "Portuguese - 葡萄牙语",
    "fr": "French - 法语",
    "de": "German - 德语",
    "ru": "Russian - 俄语",
    "ar": "Arabic - 阿拉伯语",
    "tr": "Turkish - 土耳其语",
    "it": "Italian - 意大利语",
    "pl": "Polish - 波兰语",
    "nl": "Dutch - 荷兰语"
}

# --- 辅助函数：加载/保存数据 ---
def load_json(filepath, default_data):
    if not os.path.exists(filepath):
        return default_data
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default_data

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 辅助函数：智能查找图片路径 ---
def get_image_path(filename):
    # 优先找当前目录，再找 assets 目录，再找上一级目录的 assets
    possible_paths = [
        filename,
        os.path.join("assets", filename),
        os.path.join("..", "assets", filename)
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

# 初始化数据
tnc_data = load_json(DATA_FILE, {})
languages = load_json(LANG_CONFIG_FILE, DEFAULT_LANGUAGES)

# ==========================================
# 2. CSS 样式 (让表格好看)
# ==========================================
st.markdown("""
<style>
    /* 强制给所有表格添加边框，模拟 Word 效果 */
    table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 1rem;
        border: 1px solid #444; /* 外边框 */
    }
    th, td {
        border: 1px solid #ccc; /* 单元格边框 */
        padding: 8px;
        text-align: left;
        color: inherit; /* 继承字体颜色 */
    }
    th {
        background-color: #f0f2f6; /* 表头背景色 */
        color: #000;
    }
    /* 针对暗色模式的微调 */
    @media (prefers-color-scheme: dark) {
        th { background-color: #262730; color: #fff; }
        td { border-color: #444; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 页面逻辑
# ==========================================

# 页面导航
tab_home, tab_admin, tab_settings = st.tabs(["🏠 活动主页 / Home", "⚙️ 内容管理 / Admin", "🌍 语言设置 / Settings"])

# ------------------------------------------
# TAB 1: 用户主页
# ------------------------------------------
with tab_home:
    # 1. 尝试加载 Logo
    logo_path = get_image_path("logo.png")
    if logo_path:
        st.image(logo_path, width=200)
    else:
        st.warning("⚠️ Logo not found (logo.png)")

    # 2. 尝试加载 Banner
    banner_path = get_image_path("banner.png")
    # 兼容 jpg
    if not banner_path: 
        banner_path = get_image_path("banner.jpg")

    if banner_path:
        st.image(banner_path, use_container_width=True)
    else:
        st.info("Banner not found (banner.png)")

    st.divider()

    st.subheader("📋 Terms and Conditions")

    # 语言选择
    lang_code = st.selectbox(
        "Select Language / 选择语言",
        options=list(languages.keys()),
        format_func=lambda x: languages.get(x, x)
    )

    # 显示内容
    with st.container(border=True):
        content = tnc_data.get(lang_code, "")
        if content:
            st.markdown(content, unsafe_allow_html=True)
        else:
            st.markdown("*暂无内容 / No Content Uploaded*", unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: 管理后台 (核心功能)
# ------------------------------------------
with tab_admin:
    st.header("📄 Upload & Edit Word Files")
    st.info("上传 Word 文档后，系统会自动提取表格和文字。你可以继续编辑 HTML 代码来微调。")

    # 1. 选择要编辑的语言
    target_lang = st.selectbox(
        "Step 1: 选择目标语言 / Target Language",
        options=list(languages.keys()),
        format_func=lambda x: languages.get(x, x),
        key="admin_lang_select"
    )

    col1, col2 = st.columns([1, 1.5])

    # --- 左侧：上传区 ---
    with col1:
        st.markdown("### 📤 上传 Word (.docx)")
        uploaded_file = st.file_uploader(f"Upload for [{languages[target_lang]}]", type=['docx'], key=f"uploader_{target_lang}")

        if uploaded_file is not None:
            # 按钮：开始转换
            if st.button("🔄 开始转换 / Convert to HTML", type="primary"):
                try:
                    # 使用 mammoth 转换
                    result = mammoth.convert_to_html(uploaded_file)
                    html = result.value
                    messages = result.messages
                    
                    # 检查是否为空 (常见错误：内容在文本框里)
                    if not html.strip():
                        st.error("⚠️ 转换结果为空！")
                        st.warning("请检查：Word 里的表格是否放在了【文本框】里？请把表格复制到正文中再试。")
                    else:
                        # !!! 关键步骤：保存到 Session State，防止刷新丢失 !!!
                        st.session_state[f"temp_html_{target_lang}"] = html
                        st.success(f"✅ 转换成功！提取了 {len(html)} 个字符。")
                        st.rerun() # 强制刷新以更新右侧编辑器
                except Exception as e:
                    st.error(f"转换出错: {e}")

    # --- 右侧：编辑区 ---
    with col2:
        st.markdown("### ✏️ 编辑与发布")
        
        # 逻辑：优先显示刚刚转换的内容，如果没有，则显示数据库里已保存的内容
        # session_state key: f"temp_html_{target_lang}"
        
        current_saved_content = tnc_data.get(target_lang, "")
        draft_content = st.session_state.get(f"temp_html_{target_lang}", current_saved_content)

        # 编辑器 (Text Area)
        final_content = st.text_area(
            "HTML Editor (可微调内容)", 
            value=draft_content, 
            height=600,
            key=f"editor_{target_lang}"
        )

        # 保存按钮
        if st.button("💾 保存并发布 / Save & Publish", type="primary"):
            # 1. 保存到内存字典
            tnc_data[target_lang] = final_content
            # 2. 写入 JSON 文件
            save_json(DATA_FILE, tnc_data)
            
            # 3. 清理临时状态 (可选，这里保留以免用户想撤销，或者直接清除)
            # if f"temp_html_{target_lang}" in st.session_state:
            #     del st.session_state[f"temp_html_{target_lang}"]
            
            st.success(f"🎉 [{languages[target_lang]}] 内容已更新！去首页看看吧。")
            # 稍微等待一下让用户看到成功提示
            import time
            time.sleep(1)
            st.rerun()

# ------------------------------------------
# TAB 3: 语言设置
# ------------------------------------------
with tab_settings:
    st.header("🌍 添加新语言 / Add Language")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        new_code = st.text_input("Code (e.g., 'fr')", max_chars=5).strip()
    with c2:
        new_name = st.text_input("Name (e.g., 'French - 法语')").strip()
    with c3:
        st.write("")
        st.write("")
        if st.button("➕ 添加 / Add"):
            if new_code and new_name:
                if new_code in languages:
                    st.error("语言代码已存在 / Code exists")
                else:
                    languages[new_code] = new_name
                    save_json(LANG_CONFIG_FILE, languages)
                    st.success(f"Added: {new_name}")
                    st.rerun()
            else:
                st.warning("请填写完整 / Fill all fields")

    st.divider()
    st.write("Current Languages:", languages)