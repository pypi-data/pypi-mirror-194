import dataclasses
from typing import List, Union, Dict, ClassVar

from vatis.asr_commons.domain.expression import Expressions
from vatis.asr_commons.json.deserialization import JSONDeserializable


class ReplacementMergeOption:
    MERGE_LEFT: ClassVar[str] = 'MERGE_LEFT'
    STANDALONE: ClassVar[str] = 'STANDALONE'
    MERGE_RIGHT: ClassVar[str] = 'MERGE_RIGHT'


@dataclasses.dataclass(frozen=True)
class FindReplaceConfig(JSONDeserializable):
    replacement: str
    regex: List[str]
    enabled: bool = True
    merge: str = ReplacementMergeOption.STANDALONE

    def __post_init__(self):
        assert self.replacement is not None, '"replacement" must not be none'
        assert self.regex is not None, '"regex" must not be none'
        assert self.enabled is not None, '"enabled" must not be none'
        assert self.merge is not None, '"merge" must not be none'

    @staticmethod
    def from_json(json_dict: dict):
        return FindReplaceConfig(**json_dict)


class FindReplaceExpressions(Expressions):
    def __init__(self, expressions: Dict[str, List[str]] = None):
        super(FindReplaceExpressions, self).__init__(expressions)

    @staticmethod
    def from_find_replace_config_list(expressions: List[Union[FindReplaceConfig, dict]]) -> 'FindReplaceExpressions':
        parsed_expressions: Dict[str, List[str]] = {}

        for find_replace_config in expressions:
            if isinstance(find_replace_config, FindReplaceConfig):
                pass
            elif isinstance(find_replace_config, dict):
                find_replace_config = FindReplaceConfig.from_json(find_replace_config)
            else:
                raise ValueError(f'Bad type: {type(find_replace_config)}')

            if find_replace_config.replacement not in parsed_expressions:
                parsed_expressions[find_replace_config.replacement] = find_replace_config.regex.copy()
            else:
                raise ValueError(f'Duplicate replacement: {find_replace_config.replacement}')

        return FindReplaceExpressions(parsed_expressions)
