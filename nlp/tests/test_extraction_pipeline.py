from nlp.parsers import load_parser
from nlp.entity import ExtractionPipeline
import pprint

parser_names = ["event", "gpe", "email", "ip", "uri", "number", "symbol"]
parsers = []

for name in parser_names:
    print(name)
    kwargs = {}
    if name == "gpe":
        kwargs = {"sub_entities": ["nationality"]}
    parser = load_parser(name)(**kwargs)
    parsers.append(parser)
print(parsers)
pipeline = ExtractionPipeline(parsers)

text = "That American dude has 150 billion Zimbabwean Dollars cash! And he spent it all on Christmas Carol! My email is elijahmandajc@gmail.com and you can find me on https://github.com/elijahmanda. Can you imagine i setup a server on localhost:8080!"
tokens = pipeline.extract(text)
tokens = [token.to_dict() for token in tokens]
pprint.pprint(tokens, sort_dicts=False)
