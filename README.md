# NLP

This project is an NLP library that provides tools for entity extraction, tokenization, and parsing. It allows users to define custom entity parsers, tokenize text based on regex patterns, and build pipelines for extracting multiple entities from text. This library is suitable for parsing and identifying structured entities like numbers, IP addresses, emails, and more.

## Features

- **Custom Entity Parsers:**
  - Base class `EntityParser` to create custom parsers.
  - `RegexEntityParser` for parsing entities based on regex patterns.
  - `CallbackEntityParser` to define parsers with a custom callback function.
  
- **Tokenization:**
  - A flexible `RegexTokenizer` for matching custom entities in text.

- **Entity Extraction Pipeline:**
  - `ExtractionPipeline` to combine multiple parsers into a sequential processing pipeline for extracting various entities from a text input.

## Installation

The library requires Python 3.9+. To install, follow these steps:

```bash
# Clone the repository
git clone https://github.com/elijahmanda/NLP.git

# Navigate to the project directory
cd nlp-library

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. **Basic Entity Parsing**

You can create a basic entity parser using the `EntityParser` class or its subclasses.

```python
from nlp.parsers import load_parser

# Load a number parser
np = load_parser("number")

# Parse numbers from text
text = "two hundred and twenty five point nine"
tokens = np(text)
for token in tokens:
    print(token.dumps())

# Output:
# {
#   "text": "two hundred and twenty five point nine",
#   "span": [0, 38],
#   "entity": "number",
#   "metadata": {
#     "number_type": "spoken",
#     "value_type": "float",
#     "value": 225.9
#   }
# }
```

### 2. **Custom Regex-Based Entity Parser**

To create a custom entity parser based on regular expressions, use the `RegexEntityParser`.

```python
from nlp.entity import RegexEntityParser

# Define patterns for custom entities (e.g., number, word)
patterns = [
    ("number", r"\d+(?:\.\d+)?"),
    ("word", r"\w+")
]

# Initialize a RegexEntityParser
parser = RegexEntityParser(patterns)

# Parse entities from text
text = "The price is 23.45 dollars."
tokens = parser(text)
for token in tokens:
    print(token.dumps())

# Output:
# {
#   "text": "23.45",
#   "span": [13, 18],
#   "entity": "number",
#   "metadata": None
# }
```

### 3. **Using the Extraction Pipeline**

The `ExtractionPipeline` allows you to combine multiple entity parsers into a single processing pipeline. This is useful for extracting various entities (e.g., numbers, IPs, and emails) from the same text.

```python
from nlp.parsers import load_parser
from nlp.entity import ExtractionPipeline

# Load individual parsers
ip = load_parser("ip")
email = load_parser("email")
np = load_parser("number")

# Create an extraction pipeline
pipeline = ExtractionPipeline([ip, email, np])

# Extract entities from text
text = "My IP is 127.0.0.1 and email is johndoe@example.com."
tokens = pipeline.extract(text)
for token in tokens:
    print(token.dumps())

# Output:
# {
#   "text": "127.0.0.1",
#   "span": [10, 19],
#   "entity": "ip_address",
#   "metadata": None
# }
# {
#   "text": "johndoe@example.com",
#   "span": [31, 50],
#   "entity": "email",
#   "metadata": None
# }
```

### 4. **Callback-Based Entity Parser**

To use a parser with a custom callback function, you can define a `CallbackEntityParser`.

```python
from nlp.entity import CallbackEntityParser

# Define a callback function for custom entity extraction
def extract_dates(text):
    # Assume we extract dates in a certain format (for demo purposes)
    return [("2024-01-01", "date", (0, 10))]

# Initialize a CallbackEntityParser
date_parser = CallbackEntityParser(callback=extract_dates)

# Parse dates from text
tokens = date_parser("2024-01-01 is the start of the new year.")
for token in tokens:
    print(token.dumps())

# Output:
# {
#   "text": "2024-01-01",
#   "span": [0, 10],
#   "entity": "date",
#   "metadata": None
# }
```

### 5. **Extracting Entities from Tokens**

To extract additional entities from existing tokens, you can use the `extract_entities_from_tokens` method.

```python
from nlp.entity import extract_entities_from_tokens

# Assume we have some tokens
tokens = [
    Token(text="My IP is", span=(0, 9)),
    Token(text="127.0.0.1", span=(10, 19), entity="ip_address"),
]

# Use a parser (e.g., email parser) to extract more entities from the tokens
new_tokens = extract_entities_from_tokens(email_parser, tokens)

for token in new_tokens:
    print(token.dumps())
```

## Conclusion

This library provides flexible tools for entity extraction and tokenization, making it easy to customize parsers and extract structured information from unstructured text. By leveraging `RegexEntityParser`, `CallbackEntityParser`, and the `ExtractionPipeline`, you can build sophisticated NLP pipelines tailored to your needs.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests with improvements or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
