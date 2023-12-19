import requests


class Ollama:

    def __init__(self, model, base_url='http://localhost:11434'):
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()

    def generate(self, prompt, **kwargs):
        endpoint = f"{self.base_url}/api/generate"

        if kwargs.get('format', 'json') != 'json':
            raise ValueError("Ollama only supports json format")

        stream = kwargs.pop('stream', False)

        data = {
            "prompt": prompt,
            "model": self.model,
            "stream": stream
        }

        data.update(kwargs)

        return self.session.post(endpoint, json=data, stream=stream)

    def chat(self, messages, **kwargs):
        endpoint = f"{self.base_url}/api/chat"

        if kwargs.get('format', 'json') != 'json':
            raise ValueError("Ollama only supports json format")

        stream = kwargs.pop('stream', False)

        data = {
            "messages": messages,
            "model": self.model,
            "stream": stream
        }

        data.update(kwargs)
        return self.session.post(endpoint, json=data, stream=stream)
