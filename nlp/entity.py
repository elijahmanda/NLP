
from nlp.tokens import Token
from nlp.utils.sequences import missing_indexes
from nlp.tokenizers import RegexTokenizer


def _sort_key(token):
    return token.span[0]


def _return_none(_):
    return None


class EntityParser:
    """
    Base class for entity parsers.
 parser.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __call__(self, text):
        """Extract entities from text.

        Args:
            text: The input text.

        Returns:
            List of Tokens representing the entities found in the text.

        """
        return [Token(text, span=(0, len(text)))]

    def parse_tokenize(self, text):
        """Tokenizes the given text and extracts entities.

        Args:
            text: The input text.

        Returns:
            A list of tokens representing the entities found in the text.

        """
        if text.isspace():
            return [Token(text, span=(0, len(text)))]

        tokens = self(text)
        if not tokens:
            return [Token(text, span=(0, len(text)))]

        # Sort tokens by start position
        tokens.sort(key=_sort_key)

        # Fill in missing tokens
        missing_spans = missing_indexes(
            [token.span for token in tokens], len(text))
        for start, end in missing_spans:
            tokens.append(Token(text[start:end], span=(start, end)))

        # Sort tokens by start position again
        tokens.sort(key=_sort_key)

        return tokens


class RegexEntityParser(EntityParser):

    def __init__(self, patterns, metadata_func=None, flags=None):
        self.patterns = list(patterns)
        self.metadata_func = metadata_func
        if not metadata_func:
            self.metadata_func = _return_none
        self.tokenizer = RegexTokenizer()
        self.tokenizer.set_patterns(patterns, False)
        self.tokenizer.compile(flags)

    def __call__(self, text):
        tokens = []
        parsed = self.tokenizer.tokenize(text)
        for token in parsed:
            tokens.append(Token(
                text=token[0],
                span=token[2],
                entity=token[1],
                metadata=self.metadata_func(token)
            ))
        return tokens


class CallbackEntityParser(EntityParser):

    def __init__(self, callback, metadata_func=None):
        self.callback = callback
        self.metadata_func = metadata_func
        if not metadata_func:
            self.metadata_func = _return_none

    def __call__(self, text):
        tokens = []
        parsed = self.callback(text)
        if not parsed:
            return []
        for token in parsed:
            tokens.append(Token(
                text=token[0],
                span=token[2],
                entity=token[1],
                metadata=self.metadata_func(token)
            ))
        return tokens


def extract_entities_from_tokens(parser, tokens):
    new_tokens = []

    for token in tokens:

        if token.entity or not token.text.strip():
            new_tokens.append(token)
            continue
        entity_tokens = parser.parse_tokenize(token.text)
        dstart = token.span[0]
        for entity_token in entity_tokens:

            new_token = Token(
                text=entity_token.text,
                span=(
                    entity_token.span[0] + dstart,
                    entity_token.span[1] + dstart,
                ),
                entity=entity_token.entity,
                metadata=entity_token.metadata,
            )
            new_tokens.append(new_token)
    new_tokens.sort(key=_sort_key)
    return new_tokens


class ExtractionPipeline:

    def __init__(self, extractors):
        self._extractors = list(extractors)

    def _get_args(self, item):
        if isinstance(item, EntityParser):
            extractor, kwargs = item, {}
        else:
            extractor, kwargs = item
        return extractor, kwargs

    def __call__(self, text):
        return self.extract(text)

    def extract(self, text):
        tokens = []
        for i, item in enumerate(self._extractors):
            extractor, _ = self._get_args(item)
            if i == 0:
                tokens = extractor.parse_tokenize(text)

                continue
            tokens = extract_entities_from_tokens(extractor, tokens)

        return tokens
