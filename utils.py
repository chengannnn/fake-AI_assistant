# 写一个函数，实现把对话存入memory中，并返回ai的回答

from langchain.chains import ConversationChain
from langchain_community.llms.moonshot import Moonshot  # 使用Moonshot模型

def get_chat_response(user_input, memory, api_key):
    model = Moonshot(api_key=api_key)
    chain = ConversationChain(llm=model, memory=memory)  # conversationchain可以自动把对话存入memory中

    response = chain.invoke(user_input)  # ai的回复,这里的回复和user的输入都会自动存入memory中
    return response["response"]  # AI的回复结构是： {'response': '回复内容', 'history': '对话历史'}
                                 # 所以想要提取AI的回复的内容需要用response["response"]

# 测试代码
if __name__ == "__main__":
    from langchain.memory import ConversationBufferMemory
    memory = ConversationBufferMemory()
    api_key = "sk-3gRgxkd8QoXXhMRjiewN42fQjjUXPYtMlKeLWcnv5rSEgCeY"
    response1 = get_chat_response("我是曹操", memory, api_key=api_key)  # 第一轮对话
    response2 = get_chat_response("我的上一句话是什么?", memory, api_key=api_key)  # 测试memory是否正常
    print(response2)