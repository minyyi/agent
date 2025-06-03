from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() # .env 파일에서 환경변수 로드
api_key = os.getenv('OPENAI_API_KEY') #  환경변수에서 API 키를 가져옴
client = OpenAI(api_key = api_key)
response = client.chat.completions.create( #  렝체인 아님
#   어떤 모델, 어떤 질문 할지 
    model="gpt-4o",
    temperature=0.1, # 0.1로 하면 답변이 더 정확해짐 / 자유도
    messages=[ #  대화의 흐름을 나타내는 메시지들, 형식이 정해져 있음
        {"role": "system", "content": "You are a helpful assistant."}, # 시스템 메시지
        # {"role": "user", "content": "2022년 월드컵 우승팀은 어디야?"}, # 유저 메시지
        {"role": "user", "content": "2026년 월드컵 개최국가는 어디야?"}, # 유저 메시지
    ],
    max_tokens=100,
    # temperature=0.7,
)

print(response)
print('-------------------------')
print(response.choices[0].message.content) #  답변 내용 출력 / 랭체인 사용하면 달라짐