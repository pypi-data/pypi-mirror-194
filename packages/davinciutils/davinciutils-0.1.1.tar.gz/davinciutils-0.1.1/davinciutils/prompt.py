from IPython.core.magic import register_cell_magic
import openai
import os


@register_cell_magic
def chatgpt(line, cell, max_tokens=500):
    response = openai.Completion.create(
        engine=os.environ["OPENAI_DEPLOYMENT_NAME"], prompt=cell, max_tokens=max_tokens
    )
    return response["choices"][0]["text"]
