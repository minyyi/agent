from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 
api_key = os.getenv('OPENAI_API_KEY') 
client = OpenAI(api_key = api_key)


def summarize_txt(file_path: str):
    client = OpenAI(api_key = api_key)
    
    #파일 읽어오기
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
        
    #요약을 위한 시스템 프롬프트를 생성
    system_prompt = f'''
    너는 다음 글을 요약하는 봇이야. 아래 글을 읽고 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약해줘.

    작성해야 하는 포맷은 다음과 같다.
    
    # 제목
    
    ## 저자의 문제 인식 및 주장(15문장 이내)
    
    ## 저자 소개
    
    =====================================================이하 텍스트=====================================================
    {text}
    '''
    
    print(system_prompt)
    print('-------------------------') #프롬프트 준비 완료
    
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.1,  # 0.1로 하면 답변이 더 정확해짐 / 자유도
    messages=[
        {"role": "system", "content": system_prompt},  # 시스템 메시지
    ],
    )

    return response.choices[0].message.content  # 답변 내용 출력

    
if __name__ == "__main__":
    file_path = './output/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축_with_preprocessing.txt'  # 요약할 파일 경로
    summary = summarize_txt(file_path)
    print(summary)  # 요약 결과 출력
    
    with open('./output/summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)