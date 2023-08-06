# Software 3.0 - Promptware


## Install

#### For common users 
```shell
pip install promptware
```



#### For developers

```shell
git clone https://github.com/ExpressAI/Promptware.git
cd Promptware

# Install the required dependencies and dev dependencies
pip install -e .
```




## Quick Example

```shell
export OS_API_KEY=YOUR_OPENAI_KEY
```

```python
from promptware import install
software = install("sentiment_classifier")
label = software.execute({"text": "I love this movie"})
```

or 

```python
import promptware as pop
software = pop.install("sentiment_classifier")
label = software.execute({"text": "I love this movie"})
```




or install a software locally

```python
from promptware import install
software = install("./softwares/sentiment_classifier")
label = software.execute({"text": "I love this movie"})
```



it also supports subconfig:

```python
from promptware import install
software = install("./softwares/machine_translation", "enzh")
software = install("./softwares/machine_translation", "zhen")
```
See more in this [example](./softwares/machine_translation)


## Add More Softwares

Here is one [example](./softwares/sentiment_classifier), where you need to create two files:
* `sentiment_classifier`: declare different configs of the software
* `sentiment_classifier_test`: a test file for your defined software

you can run the test file with following script:

```shell
python -m unittest softwares.sentiment_classifier.sentiment_classifier_test
```




## Schema of Promptware

```python
@dataclass
class Promptware:
    # Name
    name: str
    # Describe what the promptware is designed for
    description: str
    # Instruction text of promptware
    instruction: str | Callable[[Any], str]
    # Demonstration of promptware
    demonstration: Optional[list[str]]
    # Prompt template defines how a user's input will be formatted
    prompt_template: Callable[[Any], str]
    # The most appropriate tasks that the promptware could be applied to
    task: TaskType
```

