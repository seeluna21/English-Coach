import streamlit as st
import google.generativeai as genai
import os

# 页面配置
st.set_page_config(page_title="My Native English Coach", page_icon="🇺🇸")

# --- 智能模型选择器 ---
def get_available_model():
    """自动寻找当前账号可用的免费模型"""
    try:
        # 1. 获取所有模型
        all_models = [m.name for m in genai.list_models()]
        
        # 2. 优先寻找 flash 模型 (通常免费且快)
        for model in all_models:
            if "flash" in model and "v1beta" not in model: # 避开不稳定的beta版
                return model.replace("models/", "")
        
        # 3. 如果没有flash，找 pro 模型
        for model in all_models:
            if "pro" in model and "exp" not in model: # 避开 exp (实验版)
                return model.replace("models/", "")
                
        # 4. 实在不行，就返回默认的
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash" # 兜底

# --- 核心逻辑 ---
def get_native_explanation(chinese_text):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        return "⚠️ Error: API Key not found. Please set it in Streamlit Secrets."

    genai.configure(api_key=api_key)
    
    # 自动选择模型
    target_model = get_available_model()
    # 在界面上悄悄显示用了哪个模型 (方便调试)
    print(f"Using model: {target_model}") 
    
    model = genai.GenerativeModel(target_model)

    prompt = f"""
    You are an expert American English verbal coach. 
    The user is an advanced learner.
    
    Analyze this Chinese phrase: "{chinese_text}"

    Output your response in this EXACT structure using Markdown:

    ### 🎯 Native Translation
    [Natural spoken English]

    ### 🎬 Scenario & Nuance
    [When to use it? Tone?]

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
st.caption("Powered by Python & Gemini")
