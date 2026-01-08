import json
from openai import OpenAI
from app.service.time_service import TimeService
import os

class ChatService:
    def __init__(self, time_service: TimeService):
        self.time_service = time_service
        
        api_key = os.getenv("UPSTAGE_API_KEY")

        self.client = OpenAI(api_key=api_key) 

    def process_question(self, user_question: str):
        print(f"🔹 사용자 질문 수신: {user_question}") # 로그 출력

        #Tool 정의
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Retrieves current time for the given timezone.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "enum": ["Asia/Seoul", "America/New_York", "Europe/London", "Asia/Tokyo"],
                                "description": "The timezone to get the current time for."
                            }
                        },
                        "required": ["timezone"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]

        #AI에게 질문 전달
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Whenever asked about time, you MUST use the 'get_current_time' tool. Do not guess."},
            {"role": "user", "content": user_question}
        ]

        print("AI에게 답변 요청 중...")
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message

        #AI가 도구 사용을 요청했는지 확인
        if message.tool_calls:
            print(f"AI가 도구 사용을 요청함! ({len(message.tool_calls)}건)")
            
            messages.append(message)
            
            #요청된 모든 도구 실행
            for tool_call in message.tool_calls:
                if tool_call.function.name == "get_current_time":
                    args = json.loads(tool_call.function.arguments)
                    timezone = args.get("timezone")
                    
                    print(f"시간 조회 시도: {timezone}")

                    function_result = self.time_service.get_current_time(timezone)
                    
                    print(f"조회 결과: {function_result}")

                    #실행 결과를 메시지에 추가
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": function_result
                    })

            #최종 답변 요청
            print("최종 답변 생성 중...")
            final_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return final_response.choices[0].message.content
        
        else:
            pass