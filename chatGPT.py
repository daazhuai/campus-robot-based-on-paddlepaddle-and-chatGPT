import openai

openai.api_key = "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"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="我爱你，gpt",
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)
message = response.choices[0].text
print(message)