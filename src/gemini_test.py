import google.generativeai as genai
api_key = "API_KEY"
genai.configure(api_key=api_key)
def test_gemini_api(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt])
        print("Response from Gemini API:")
        print(response.text)
    except Exception as e:
        print("An error occurred:", e)


test_prompt = "What is the capital of France?"
test_gemini_api(test_prompt)
