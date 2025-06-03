from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() # .env 파일에서 환경변수 로드
api_key = os.getenv('OPENAI_API_KEY') #  환경변수에서 API 키를 가져옴
client = OpenAI(api_key = api_key)


def get_ai_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,  # 0.1로 하면 답변이 더 정확해짐 / 자유도
        messages=messages,
        max_tokens=100,
    )
    return response.choices[0].message.content  #  답변 내용 출력 / 랭체인 사용하면 달라짐
    

messages=[ #  대화의 흐름을 나타내는 메시지들, 형식이 정해져 있음
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야"}, # 시스템 메시지
]

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit": # "exit" 입력 시 종료
        break
    messages.append({"role": "user", "content": user_input})  # 유저 메시지 추가
    ai_response = get_ai_response(messages)
    
    #챗지피티가 상대방 대답(유저입력한 메시지)만 보면 전체적인 문맥을 파악할 수 없음
    # AI가 대답한 메시지를 다시 messages에 추가
    messages.append({"role": "assistant", "content": ai_response})  # AI 메시지 추가
    ai_response = get_ai_response(messages)
    print(f"AI: {ai_response}")