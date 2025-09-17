import streamlit as st
from openai import OpenAI
# from dotenv import load_dotenv 
import os 
from PIL import Image, ImageDraw, ImageFilter

key111=st.secrets['API_KEY']


client = OpenAI(api_key=key111)
# ai 설정

st.title('앱 이름')
st.text_input('이름을 입력해주세요',key='u_name')
if st.session_state.u_name:
    st.subheader(f"반가워요, {st.session_state.u_name}님! 저는 당신의 친구입니다.")
    st.subheader("저를 만나기 전에 몇 가지 물어볼게 있어요!")
    st.text_input('제 이름은 무엇인가요?',key='f_name')
    if st.session_state.f_name:
        st.selectbox(
            '제 성격은 어떤가요?:',
            ['따뜻하고 친절한', '활발하고 귀여운', '항상 유머가 넘치는', '직설적이고 현실적인'], key='song'
        )
        if st.session_state.song:
            friend_image =st.text_input("마지막으로 당신의 고민이 있나요?",key='image')


            if st.session_state.image:
                # gpt

                if "openai_model" not in st.session_state:
                    st.session_state["openai_model"] = "gpt-3.5-turbo"

                if "messages" not in st.session_state:
                    system_message = f"""
                    너는 이제 {st.session_state.f_name}라는 이름을 가진 AI 친구야.
                    너의 성격은 {st.session_state.song}이고, 사용자 즉,{st.session_state.u_name}의 고민을 잘 들어주는 조언자겸 친구야. 사용자의 고민은{st.session_state.image}
                    성격에 맞게 답변해줘."""
                    st.session_state.messages = []
                    st.session_state.messages = [{"role": "system", "content": system_message}]


                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                if prompt := st.chat_input("What is up?"):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):
                        stream = client.chat.completions.create(
                            model=st.session_state["openai_model"],
                            messages=[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ],
                            stream=True,
                        )
                        response = st.write_stream(stream)
                    st.session_state.messages.append({"role": "assistant", "content": response})









#     # 추가1. 
# system_message=f"""
#     너는 이제 {friend_name}라는 이름을 가진 AI 친구야.
#     너의 성격은 {st.session_state.song}이고, 사용자 즉,{user_name}의 고민을 잘 들어주는 조언자겸 친구야.
#     성격에 맞게 답변해줘."""
# # 추가1의 끝.. 

# # Streamlit에서는 페이지 새로고침 때마다 변수들이 초기화되기 때문에,
# # session_state라는 저장소를 사용해 상태를 유지합니다.
# # 여기서는 사용할 모델을 "gpt-3.5-turbo"로 기본 설정하며, 이미 있으면 덮어쓰지 않습니다.
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# # 대화 내용을 저장할 리스트를 session_state.messages에 둡니다.
# # 처음 실행시에는 빈 리스트를 만들고, 시스템 메시지를 첫 메시지로 넣습니다.
# # 이렇게 하면 챗봇이 처음부터 지정한 역할대로 대답할 수 있습니다.
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.messages = [{"role": "system", "content": system_message}]