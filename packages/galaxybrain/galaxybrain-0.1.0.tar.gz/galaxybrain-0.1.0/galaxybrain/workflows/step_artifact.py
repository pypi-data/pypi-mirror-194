from abc import ABC
from typing import Optional
from attrs import define, field
from galaxybrain.utils import TiktokenTokenizer, Tokenizer


@define
class StepArtifact(ABC):
    value: Optional[any]
    tokenizer: Tokenizer = field(default=TiktokenTokenizer(), kw_only=True)

    def token_count(self) -> Optional[int]:
        if isinstance(self.value, str):
            return self.tokenizer.token_count(self.value)
        else:
            return None
