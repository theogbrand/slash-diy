```
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

provider = os.environ["PROVIDER"]

if provider == "openai":
    # OpenAI
    response = completion(model="openai/gpt-4o", messages=[{"role": "user", "content": "Hello!"}])
else:
    # Anthropic  
    response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[{"role": "user", "content": "Hello!"}])
```