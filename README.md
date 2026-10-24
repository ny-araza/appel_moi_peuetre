*This project has been created as part of the 42 curriculum by ny-araza*

# DESCRIPTION
This project is about of using the function call of the Large Language Model (LLM). From a natural language query and a JSON schema defining the available function signatures, the AI ​​performs a correspondence analysis to generate a structured JSON containing the relevant functions and their extracted arguments.

## Algorithm explanation
Since the required output schema consists of three keys (prompt, name, and parameters), the algorithm is structured into two main components:

#### Function name retrieval
To completely eliminate hallucinations and restrict the LLM output strictly to valid function names, constrained logit decoding is applied:

**Logit Extraction** : Capture the model's top logits and mask non-allowed token logits by setting them to -inf.

**Vocabulary Alignment** : Encode all valid function names defined in function_definition.

**Constrained Matching** : Compare the model's highest logit predictions against the encoded valid function names, retaining the candidate with the highest logit score.

This mechanism ensures that the model can only select a function name that strictly exists within the provided function definitions.

#### Parameter Extraction
To retrieve function arguments conforming to the schema in function_calling.json, a targeted prompt instructs the model to output parameters as a JSON object (dictionary).
To optimize output length and prevent model chatter:
Forced Termination: Generation is immediately halted as soon as the model emits a closing brace '}/n'.

## Design decisions
The overall reliability of the extraction pipeline depends heavily on prompt construction:
Explicit Instructions: Eliminates ambiguity to ensure deterministic, no halucination
Immediate Semantic Alignment: Direct, structured prompt design prevents misinterpretation and reduces parsing failures during LLM execution.

## Performance analysis
<table>
    <thead>
        <th>Accuracy</th>
        <th>Speed</th>
    </thead>
    <tbody>
        <td>
            90.9%
        </td>
        <td>
            00:02:50.3
        </td>
    </tbody>
</table>

**NB:** Its depend to the performace of the PC

Evaluated on a test set of 11 prompts from the JSON file, the execution pipeline completed total generation in 2 minutes and 50 seconds, achieving a 90.9% success rate (10 out of 11 correct predictions).

**NB:** The LLM may halucinate sometimes. If the LLM can't find the function name or parameters according to the prompt, he return {} or the LLM hallucinate

## Challenges faced
The most challenging aspect of the project was designing an optimal constrained decoding strategy for function name extraction. The solution involved strict logit masking: setting all vocabulary logits to $-\infty$ while enabling only those corresponding to valid function names. This forces the LLM to output exclusively valid function names, completely eliminating hallucinations.

## Testing strategy
To validate the implementation, I defined BaseModel (pydantic) schemas for both input and output structures. Using JSON schema validation (validate_json), the pipeline strictly enforces type checking and structural compliance—raising an explicit error if a payload fails to match the expected format.

## Exemple usage
```bash
    make run
    # run with default flag --input data/input/function_calling_tests.json --functions_definition data/input/functions_definition.json --output data/output/function_calling_results.json
```

### Input function_definition example
```json
[
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {
        "type": "string"
      },
      "b": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  },
  {
    "name": "fn_greet",
    "description": "Generate a greeting message for a person by name.",
    "parameters": {
      "name": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  },
  {
    "name": "fn_check_status",
    "description": "Checks the system status based on whether the access is active.",
    "parameters": {
      "is_active": {
        "type": "bool"
      }
    },
    "returns": {
      "type": "string"
    }
  },
  {
    "name": "fn_reverse_string",
    "description": "Reverse a string and return the reversed result.",
    "parameters": {
      "s": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  },
  {
    "name": "fn_get_square_root",
    "description": "Calculate the square root of a number.",
    "parameters": {
      "a": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  },
  {
    "name": "fn_substitute_string_with_regex",
    "description": "Replace all occurrences matching a regex pattern in a string.",
    "parameters": {
      "source_string": {
        "type": "string"
      },
      "regex": {
        "type": "string"
      },
      "replacement": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  }
]
```

### Input prompt example
```json
{
    "prompt": "What is the sum of 2 and 3?"
},
{
    "prompt": "What is the sum of 265 and 345?"
},
```

### Output example 
```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 5.0
    }
  },
  {
    "prompt": "What is the sum of 265  and 345?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 265.0,
      "b": 345.0
    }
  }
]
```

# INSTRUCTIONS
```bash
    make install
    # initialize the projet and install it for the first time
```
```bash
    make run
    # Run the project with default flag
```
```bash
    make sync
    # syncronize the venv package to the uv.lock
```
```bash
    make install
    # initialize the projet and install it for the first time
```
```bash
    make lint | make lint-strict
    # Check the mypy and flake8 errors
```
```bash
    make clean
    # Delete all cache (Hugging face and uv_cache)
```
```bash
    make fclean
    # Delete all cache and delete all file installed with (make install)
```
```bash
    uv run python -m src --input <input_file.json> --functions_definition <function_definition.json> --output <output.json>
    # Run the projet with own parameters
    # Need to change the uv cache dir and the huging face cache
```
```bash
    # Before runing the uv run, run this command first
    export UV_CACHE_DIR=~/goinfre/uv_cache
    export HF_HOME=~/goinfre/home
```

# RESOURCES
### Documentation and Articles
<ul>
    <li><a href="https://blog.stephane-robert.info/docs/developper/programmation/python/json/">Module JSON:</a> Used for load and dump json file</li>
    <li><a href="https://pydantic.dev/docs/validation/2.9/api/pydantic/type_adapter">TynyAdapter</a>: Type adapters provide a flexible way to perform validation and serialization based on a Python type. </li>
    <li>Peer learning: How the LLM generate valid answer</li>
</ul>

### AI USAGE
I most use AI to refine and optimize my prompt engineering.
