from typing import Dict, Any
import json
from langchain.chains import APIChain
from typing import Any, Dict, Optional
from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
)


class ModAPIChain(APIChain):
    """Chain that makes API calls and summarizes the responses to answer a question,
    but doesn't display any API outputs for confidentiality! (only difference to APIChain)"""
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        question = inputs[self.question_key]
        api_url = self.api_request_chain.predict(
            question=question,
            api_docs=self.api_docs,
            callbacks=_run_manager.get_child(),
        )
        _run_manager.on_text(api_url, color="green", end="\n", verbose=self.verbose)
        api_response = self.requests_wrapper.get(api_url)
        answer = self.api_answer_chain.predict(
            question=question,
            api_docs=self.api_docs,
            api_url=api_url,
            api_response=api_response,
            callbacks=_run_manager.get_child(),
        )
        return {self.output_key: answer}


class APIResponse(APIChain):
    """Chain that makes API calls and summarizes the responses to answer a question."""
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        question = inputs[self.question_key]
        api_url = self.api_request_chain.predict(
            question=question,
            api_docs=self.api_docs,
            callbacks=_run_manager.get_child(),
        )
        _run_manager.on_text(api_url, color="green", end="\n", verbose=self.verbose)
        api_response = self.requests_wrapper.get(api_url)
        answer = api_response
        return {self.output_key: answer}


class FlexAPIChain(APIChain):
    """
    Flexible API Chain which can create all request types
    whereby the body is passed as an attribute. Relies on
    specific Prompt Templates.
    """
    body: dict = {}
    def _call(self, inputs: Dict[str, str], run_manager= None) -> Dict[str, str]:
        question = inputs[self.question_key]
        request_info = self.api_request_chain.predict(
            question=question, api_docs=self.api_docs
        )
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        api_url, request_method = request_info.split('|')
        _run_manager.on_text(request_method, color="green", end="\n", verbose=self.verbose)
        _run_manager.on_text(api_url, color="green", end="\n", verbose=self.verbose)

        # get the method with same name
        request_func = getattr(self.requests_wrapper, request_method.lower().rstrip().lstrip())

        api_response = request_func(api_url, self.body)
        return {self.output_key: api_response}


class FlexAPIChainPayload(APIChain):
    """
    Flexible API Chain which can create all request types
    including the necessary payload. Relies on
    specific Prompt Templates.
    """
    def _call(self, inputs: Dict[str, str], run_manager = None) -> Dict[str, str]:
        question = inputs[self.question_key]
        request_info = self.api_request_chain.predict(
            question=question, api_docs=self.api_docs
        )
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        api_url, request_method, body = request_info.split('|')
        _run_manager.on_text(body, color="green", end="\n", verbose=self.verbose)
        _run_manager.on_text(request_method, color="green", end="\n", verbose=self.verbose)
        _run_manager.on_text(api_url, color="green", end="\n", verbose=self.verbose)

        # get the method with same name
        request_func = getattr(self.requests_wrapper, request_method.lower().rstrip().lstrip())

        api_response = request_func(api_url, json.loads(body))
        return {self.output_key: api_response}