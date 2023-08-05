# krdict.py

A python module which helps to query the [API](https://krdict.korean.go.kr/openApi/openApiInfo) of the
[Korean Learner's Dictionary](https://krdict.korean.go.kr/), provided by the National Institute of Korean Language.
Inspired by [krdict.js](https://github.com/Fox-Islam/krdict.js).

## Installation

To install the module via pip, run:

```
pip install krdict.py
```

To use this module, you'll need to generate an API key via [krdict](https://krdict.korean.go.kr/openApi/openApiRegister) (requires login).

## Usage
A minimal example query which assumes the `KRDICT_KEY` environment variable is set:

```python
import os
import json
import krdict

krdict.set_key(os.getenv('KRDICT_KEY'))
response = krdict.search_words(query='나무')

print(json.dumps(response, indent=2, ensure_ascii=False))
```

Assuming an error is not returned, this would print something like:

```json
{
  "data": {
    ...
    "results": [
      {
        "target_code": 32750,
        "word": "나무",
        "pronunciation": "나무",
        "link": "https://krdict.korean.go.kr/dicSearch/SearchView?ParaWordNo=32750",
        "meaning": [
          {
            "definition": "단단한 줄기에 가지와 잎이 달린, 여러 해 동안 자라는 식물.",
            "order": 1
          },
          ...
        ],
        "part_of_speech": "명사",
        "vocabulary_grade": "초급",
        "homograph_num": 0
      },
      ...
    ],
    "num_results": 10,
    "start_index": 1,
    "total_results": 53,
    "last_build_date": "20211001061204"
  },
  "request_params": {
    "q": "나무",
    "key": "YOUR_API_KEY"
  }
}
```
