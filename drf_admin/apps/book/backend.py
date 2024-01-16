import openai
# https://platform.openai.com/api-keys
openai.api_key = "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"  # 替换为您的 OpenAI API 密钥


def get_gpt_response(prompt):
    # 建立ChatCompletion端點的請求
    temp='你要扮演的角色說明:你是高雄市長，口頭禪是高雄發大財，民進黨抹黑我，征服宇宙;我的問題:'
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::8NcRQDt1",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": temp+prompt},
        ],
    )
    # print(response.choices[0].message)

    return response.choices[0].message["content"]

# print(get_gpt_response("你好"))