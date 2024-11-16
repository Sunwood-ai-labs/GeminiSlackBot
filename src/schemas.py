RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "blocks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "text": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "text": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
}

SYSTEM_PROMPT = """あなたは親切なアシスタントです。
メッセージに対して、分かりやすく構造化された形で応答してください。
可能な限り絵文字を使用し、情報を見やすく提示してください。"""
