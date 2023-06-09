from typing import Literal

import pydantic
from oasst_shared.schemas import inference


class GenerateStreamParameters(pydantic.BaseModel):
    max_new_tokens: int | None
    do_sample: bool | None
    top_k: int | None
    top_p: float | None
    temperature: float | None
    repetition_penalty: float | None
    seed: int | None
    stop: list[str] = ["\nUser:", "\nAssistant:"]  # TODO: make this a bit more workable because it's mutliple tokens
    details: bool = True

    @staticmethod
    def from_work_request(work_request: inference.WorkRequest) -> "GenerateStreamParameters":
        return GenerateStreamParameters(
            max_new_tokens=work_request.max_new_tokens,
            do_sample=work_request.do_sample,
            top_k=work_request.top_k,
            top_p=work_request.top_p,
            temperature=work_request.temperature,
            repetition_penalty=work_request.repetition_penalty,
            seed=work_request.seed,
        )


class Token(pydantic.BaseModel):
    text: str
    logprob: float
    id: int

    def __len__(self) -> int:
        return len(self.text)

    def to_token_response(self) -> inference.TokenResponse:
        return inference.TokenResponse(
            text=self.text,
            log_prob=self.logprob,
            token_id=self.id,
        )


class StreamDetails(pydantic.BaseModel):
    generated_tokens: int
    seed: int | None
    finish_reason: Literal["length", "eos_token", "stop_sequence"]


class GenerateStreamResponse(pydantic.BaseModel):
    token: Token
    generated_text: str | None
    details: StreamDetails | None
