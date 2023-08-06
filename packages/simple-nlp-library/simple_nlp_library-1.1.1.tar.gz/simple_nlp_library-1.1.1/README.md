# simple_nlp_library
Simple NLP library

## usage

### installation
```
python3 -m pip install --upgrade simple_nlp_library
```

### api

#### semantic_tokens

```python
preprocessing.semantic_tokens('The quick brown fox jumps over the lazy dog')
```

#### cosine_similarity
```python
metrics.cosine_similarity([1.0, 1.0, 1.0], [4.0, 4.0, 4.0])
```

#### inserting_distance
```python
metrics.inserting_distance('simple', 'simpler')
```

#### inserting_similarity
```python
metrics.inserting_similarity('simple', 'simpler')
```
