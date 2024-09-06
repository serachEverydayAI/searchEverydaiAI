# import openai
#from .. config import API_KEY
#
# openai.api_key = API_KEY
#
# def summarize_article(article_text: str) -> str:
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Summarize the following article:\n\n{article_text}",
#         max_tokens=100
#     )
#     return response.choices[0].text.strip()
