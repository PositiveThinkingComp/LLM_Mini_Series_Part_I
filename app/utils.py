from langchain import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.api.prompt import API_URL_PROMPT_TEMPLATE


def find_value(dictionary: dict, key):
    """
    Recursive function to return the value of key in a dictionary
    (Code was also created by an LLM)
    """
    if key in dictionary:
        return dictionary[key]
    for k, v in dictionary.items():
        if isinstance(v, dict):
            item = find_value(v, key)
            if item is not None:
                return item


def create_custom_response_template(custom_resp: str):
    # Customized Prompt
    API_RESPONSE_PROMPT_TEMPLATE = (
        API_URL_PROMPT_TEMPLATE
        + """ {api_url}

    Here is the response from the API:

    {api_response}""" + f"\n\n{custom_resp}"
    )

    return PromptTemplate(
        input_variables=["api_docs", "question", "api_url", "api_response"],
        template=API_RESPONSE_PROMPT_TEMPLATE,
    )


def custom_api_prompt(llm, chain, question, custom_resp):
    """
    Helper function for separating the api-link creation and the post-processing on the response
    """
    resp_prompt = create_custom_response_template(custom_resp)
    get_answer_chain = LLMChain(llm=llm, prompt=resp_prompt)
    chain.api_answer_chain = get_answer_chain
    return chain.run(question)


