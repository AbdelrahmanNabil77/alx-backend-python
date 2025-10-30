# Unit Testing: `test_utils.py`

This project contains unit tests for the `access_nested_map` function defined in `utils.py`. It is part of the `0x03-Unittests_and_integration_tests` module of the ALX Backend Python curriculum.

## 📁 Directory Structure

alx-backend-python/
└── 0x03-Unittests_and_integration_tests/
├── utils.py
├── test_utils.py
└── pycache/

alx-backend-python/
└── 0x03-Unittests_and_integration_tests/
    ├── utils.py
    ├── test_utils.py
    └── __pycache__/


## 🧪 Purpose

- To test the behavior of the `access_nested_map` function using the `unittest` framework and `parameterized` library.
- To cover:
  - Valid nested key access.
  - Exceptions raised when keys are missing (`KeyError`).

## ✅ Tests Included

### `test_access_nested_map`
Checks if `access_nested_map` correctly returns the value from nested maps.

**Example Cases:**
- `({"a": 1}, ("a",)) → 1`
- `({"a": {"b": 2}}, ("a", "b")) → 2`

### `test_access_nested_map_exception`
Ensures that a `KeyError` is raised when a key in the path is missing.

**Example Cases:**
- `({}, ("a",)) → KeyError: 'a'`
- `({"a": {"b": 2}}, ("a", "c")) → KeyError: 'c'`

## 🧰 How to Run the Tests

From the `0x03-Unittests_and_integration_tests` directory:

```bash
# Using unittest discovery
python -m unittest test_utils.py

# Or run directly
python test_utils.py
```

## 🧩 Dependenciesencies
- Python 3.7+
- `parameterized` package
- Install via pip if not available:

```bash
pip install parameterized
```
## 📎 Related Files
- `utils.py`: Contains the access_nested_map function.
- `test_utils.py`: Contains all unit tests.