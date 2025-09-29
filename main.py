# 前端，实现一个AI对话的网页
# 运行请在终端输出 streamlit run main.py 并回车
# 运行前需要安装一些依赖库：请在终端输入pip install streamlit langchain langchain-community langchain-moonshot
import streamlit as st
from langchain_community.llms.moonshot import Moonshot
from langchain.memory import ConversationSummaryBufferMemory  # 使用ConversationSummaryBufferMemory可以节省memory的存储空间，并且可以设置窗口，以保留近期信息的完整性
from utils import get_chat_response

# 用一个for循环，显示历史对话
def show_history_message(i):
    for message in st.session_state["history_list"][i]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    # 再把历史对话的内容，重新填入session_state["message"]列表中
    st.session_state["message"] = st.session_state["history_list"][i].copy()
    # 清空memory中的历史对话
    st.session_state["memory"].clear()
    # 重新构建memory（通过重新创建）
    for msg in st.session_state["history_list"][i]:
        if msg["role"] == "human":
            st.session_state["memory"].save_context({"input": msg["content"]}, {"output": ""})
        elif msg["role"] == "assistant":
            # 找到对应的human消息来配对
            pass

st.title("KIKI盗版AI对话系统")

# 初始化session_state（只初始化一次）
if "history_list" not in st.session_state:
    st.session_state["history_list"] = []

# 创建侧边栏
with st.sidebar:
    api_key = st.text_input("请输入您的KIMI_API密钥：", type="password")
    st.markdown("[点击这里获取您的API密钥](https://platform.moonshot.cn/console/api-keys)")
    # 在侧边栏中加入一个列表，用于存储每轮对话的对话，每轮对话可以通过列表中的一个按钮点击进入，点击进入后，主页面会显示该轮对话的内容
    st.subheader("历史对话列表")
    
    # 检查历史对话数量限制
    if len(st.session_state["history_list"]) >= 10:
        st.error("历史对话列表最多只能保存10轮对话")
        st.stop()
    
    # 创建一个按钮，用于点击进入该轮对话
    for i in range(len(st.session_state["history_list"])):
        if st.button(f"第{i+1}轮对话", key=f"history_{i}"):
            # 当按了按钮后，先清空主页面显示的内容，并调用一个show_history_message函数，传入参数为i，在主页面显示该轮对话的内容
            st.session_state["message"] = []  # 清空主页面显示的内容
            show_history_message(i)
            st.rerun()  # 重新运行页面，目的是更新侧边栏

if "memory" not in st.session_state:  # 如果memory不存在，则创建一个,session_state是streamlit的变量，用于存储记忆和对话内容
    if api_key:  # 只有在有API密钥时才创建memory
        model = Moonshot(api_key=api_key)
        st.session_state["memory"] = ConversationSummaryBufferMemory(
            llm=model,  # 添加必需的llm参数
            max_token_limit=1000
        )
    else:
        st.info("请输入您的API密钥")
        st.stop()
    st.session_state["message"] = [{"role": "assistant", "content": "你好，我是KIMI它爹KIKI，你也可以叫我富勤，请问有什么可以帮你的吗？"}]  # 创建一个对话列表，用于存储这次对话的信息

# 主页面显示这次对话的内容
for message in st.session_state["message"]:
    with st.chat_message(message["role"]): # 在role角色下显示对话内容,role可以是assistant或human
        st.write(message["content"])

# 接下来实现用户输入，和AI回应
prompt = st.chat_input("好孩子，请说出你的疑惑：")
if prompt:
    if not api_key:
        st.error("请输入您的API密钥")
        st.stop()
    # human的输入（先存入message列表中）
    st.session_state["message"].append({"role": "human", "content": prompt})  # 把用户输入的信息存入"message"列表中
    st.chat_message("human").write(prompt) # 在human角色下显示用户输入的内容
    # AI的回应
    with st.spinner("不要打扰富勤的思考哟！"):
        sys_prompt = "请使用中文回答"
        prompt = (sys_prompt,prompt)
        response = get_chat_response(prompt, st.session_state["memory"], api_key)
        st.session_state["message"].append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# 设置一个保存按钮，用于保存这次对话的内容，保存后自动清空主页面显示的内容
if st.button("保存"):
    if len(st.session_state["history_list"]) >= 10:
        st.error("历史对话列表最多只能保存10轮对话")
    else:
        st.session_state["history_list"].append(st.session_state["message"].copy())  # .copy()是深拷贝，不会影响原来的列表  
        st.success("对话已保存")
        st.session_state["message"] = []
        # 清空ConversationSummaryBufferMemory的记忆
        st.session_state["memory"].clear()
        st.rerun()  # 重新运行页面以更新侧边栏

# 设置一个丢弃按钮，用于丢弃这次对话的内容
if st.button("丢弃"):
    st.session_state["message"] = []
    st.success("对话已丢弃")

# 问题
# 我是一只哥布林，我想繁衍后代，我现在有几个选项：1.力工梭哈流，攒攒彩礼钱，2.理工脉冲流，给学姐不断送礼物讨好她，3.延续哥布林的传统，直接去抢劫美少女回山洞。 
# 请告诉我，我应该如何选择？