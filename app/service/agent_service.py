import json
import os
from openai import OpenAI
from app.service.time_service import TimeService
from app.service.vector_service import VectorService

class AgentService:
    def __init__(self, time_service: TimeService, vector_service: VectorService):
        self.time_service = time_service
        self.vector_service = vector_service
        
        api_key = os.getenv("UPSTAGE_API_KEY")
        
        self.client = OpenAI(api_key=api_key)

    def process_query(self, query: str):
        found_rules = self.vector_service.search(query)
        context_str = "\n".join(found_rules) if found_rules else "관련 규정 없음"
        
        print(f"검색된 규정: {context_str}")

        system_prompt = f"""
        당신은 글로벌 회사의 유능한 AI 비서입니다.
        아래의 [회사 규정]을 참고하여 사용자의 질문에 답하세요.
        시간 확인이 필요하면 반드시 도구(Tool)를 사용하세요.
        
        [회사 규정]
        {context_str}
        """

        #Tool 정의
        tools = [{
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get current time for a specific timezone",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "enum": ["Asia/Seoul", "America/New_York", "Europe/London"],
                        }
                    },
                    "required": ["timezone"]
                }
            }
        }]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )
        
        message = response.choices[0].message

        #도구 사용 요청 처리
        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                if tool_call.function.name == "get_current_time":
                    args = json.loads(tool_call.function.arguments)
                    timezone = args.get("timezone")
                    
                    #시간 조회
                    time_result = self.time_service.get_current_time(timezone)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": time_result
                    })
            
            #최종 답변 생성
            final_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return final_response.choices[0].message.content
            
        return message.content