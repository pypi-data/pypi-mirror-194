from os import PathLike
from pathlib import Path
from typing import List, Dict, Optional, ClassVar


class ReplacementMerge:
    MERGE_LEFT: ClassVar[str] = 'MERGE_LEFT'
    STANDALONE: ClassVar[str] = 'STANDALONE'
    MERGE_RIGHT: ClassVar[str] = 'MERGE_RIGHT'
    MERGE_LEFT_RIGHT: ClassVar[str] = 'MERGE_LEFT_RIGHT'
    MERGE_LEFT_CAPITALIZE_NEXT: ClassVar[str] = 'MERGE_LEFT_CAPITALIZE_NEXT'


class Expressions:
    DEFAULT_REPLACEMENT_MERGE: ClassVar[str] = ReplacementMerge.STANDALONE

    def __init__(self, expressions: Dict[str, List[str]] = None,
                 replacement_merge: Dict[str, str] = None):
        self._expressions: Dict[str, List[str]] = expressions if expressions is not None else {}
        self._replacement_merge: Dict[str, str] = replacement_merge if replacement_merge is not None else {}

        for key, merge in self._replacement_merge.items():
            if merge is None:
                self._replacement_merge[key] = Expressions.DEFAULT_REPLACEMENT_MERGE
                continue

            if merge not in ReplacementMerge.__dict__:
                raise ValueError(f'Bad merge option: {merge}')

    @staticmethod
    def _parse_tsv_string(tsv_str: str) -> Dict[str, List[str]]:
        expressions: Dict[str, List[str]] = {}

        for line in tsv_str.split('\n'):
            tokens = line.split('\t')
            expressions[tokens[0]] = tokens[1:]

        return expressions

    def get(self, key: str) -> List[str]:
        expressions: Optional[List[str]] = self._expressions.get(key, [])

        if expressions is None:
            expressions = []

        return expressions

    def get_replacement_merge(self, key: str) -> str:
        return self._replacement_merge.get(key, Expressions.DEFAULT_REPLACEMENT_MERGE)

    def keys(self) -> List[str]:
        return [key for key in self._expressions]

    def items(self):
        return self._expressions.items()

    def __hash__(self):
        return hash(frozenset(self._expressions))

    def __eq__(self, other):
        if isinstance(other, Expressions):
            return self._expressions == other

        return False

    @staticmethod
    def from_tsv_str(tsv: str) -> 'Expressions':
        expressions = Expressions._parse_tsv_string(tsv)
        return Expressions(expressions)

    @staticmethod
    def from_tsv_file(tsv_file: PathLike, raise_if_not_found: bool = False) -> 'Expressions':
        tsv_file = Path(tsv_file)
        expressions: Dict[str, List[str]] = {}

        if tsv_file.exists():
            with open(tsv_file, 'r') as f:
                for line in f:
                    line: str = line.strip()

                    if not len(line) or line.startswith('#'):
                        continue

                    tokens = line.split('\t')

                    expressions[tokens[0]] = tokens[1:]
        else:
            message = f'Expressions path does not exist: {str(tsv_file)}'

            if raise_if_not_found:
                raise FileNotFoundError(message)

        return Expressions(expressions)

    @staticmethod
    def empty():
        return Expressions()

    @staticmethod
    def from_dict(expressions: Dict[str, List[str]]):
        return Expressions(expressions.copy())
