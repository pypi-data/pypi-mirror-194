
# MOdel Test Harness (Moth)

Simple way to interrogate your AI model from a separate testing application

# Quickstart

`moth server <folder path>`

`moth client`

Simplest possible model client
```
from moth import Moth
from moth.message import ImagePromptMsg, PromptResultMsg

moth = Moth("my-ai")

@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    return PromptResultMsg(class_name="cat") # Most pictures are cat pictures 

moth.run()
```
