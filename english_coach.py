import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Debug Mode", page_icon="🐞")
st.title("🐞 API 诊断模式")

# 1. 读取 API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ 成功读取 API Key (结尾是: " + api_key[-4:] + ")")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ 读取 Key 失败: {e}")
    st.stop()

# 2. 列出所有可用模型
st.write("### 🔍 正在扫描可用模型...")
try:
    found_models = []
    for m in genai.list_models():
        # 只显示支持生成文本的模型
        if 'generateContent' in m.supported_generation_methods:
            found_models.append(m.name)
            st.code(f"发现模型: {m.name}")
    
    if not found_models:
        st.error("❌ 扫描完成，但列表为空！说明你的 API Key 没有访问任何模型的权限。")
        st.info("建议：去 Google AI Studio 重新创建一个 Key，或者检查账号是否被封禁。")
    else:
        st.success(f"✅ 扫描完成！共发现 {len(found_models)} 个可用模型。")
        
        # 3. 自动尝试第一个可用模型
        model_name = found_models[0].replace("models/", "") # 去掉前缀
        st.write(f"👉 正在尝试使用: **{model_name}** 进行测试...")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say Hello to me in English")
        st.balloons()
        st.success(f"🎉 测试成功！回复内容: {response.text}")

except Exception as e:
    st.error(f"❌ 发生错误: {e}")
