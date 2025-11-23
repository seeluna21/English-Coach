import streamlit as st
import google.generativeai as genai
import os

# 页面配置
st.set_page_config(page_title="My Native English Coach", page_icon="🇺🇸")


# --- 核心逻辑 ---
def get_native_explanation(chinese_text):
    # 从 Streamlit Secrets 读取 API Key (更安全)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        return "⚠️ Error: API Key not found. Please set it in Streamlit Secrets."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are an expert American English verbal coach. 
    The user is an advanced learner who wants to sound native.

    Analyze this Chinese phrase: "{chinese_text}"

    Output your response in this EXACT structure using Markdown:

    ### 🎯 Native Translation
    [Give the most natural, native way to say this.]

    ### 🎬 Scenario & Nuance
    [Explain when to use it. Tone? Formal vs Casual?]

    ### 🗣️ Example Sentences
    * [Example 1]
    * [Example 2]
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


# --- 网页界面 ---
st.title("🇺🇸 Native English Coach")
st.caption("Enter Chinese below to get the native American expression.")

# 输入区
user_input = st.text_area("Chinese / Chinglish Phrase:", height=100, placeholder="e.g., 好烦啊, 我看看先")

if st.button("Translate & Explain", type="primary"):
    if not user_input:
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Asking the native coach..."):
            result = get_native_explanation(user_input)
            st.markdown("---")
            st.markdown(result)

# 页脚
st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash")