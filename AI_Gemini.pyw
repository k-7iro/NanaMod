import google.generativeai as genai

generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
safety_settings=[
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
model = genai.GenerativeModel(model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)
token_id = "gemini"

def set_token(token):
    genai.configure(api_key=token)

def call_ai(*args):
    try:
        responce = model.generate_content(args)
    except:
        pass
    return responce.text or "Error"
