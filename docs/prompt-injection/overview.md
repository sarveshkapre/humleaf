# Implementing Guardrails against Prompt Injection Attacks

# Table of Contents

1. [Introduction](#introduction)
2. [What is Prompt Injection?](#what-is-prompt-injection)
3. [Why Must Prompt Injection be Solved?](#why-must-prompt-injection-be-solved)
4. [Engineering: The Key to Solving Prompt Injection](#engineering-the-key-to-solving-prompt-injection)
5. [Implementing Solutions](#implementing-solutions)
    - [Intent-Based Semantic Similarity Check](#intent-based-semantic-similarity-check)
    - [Input Sanitization](#input-sanitization)
    - [Heuristics-Based Filtering](#heuristics-based-filtering)

<br />

## What is Prompt Injection?

Prompt Injection is an attack designed for language learning models (LLMs). In this attack, a malicious user manipulates the prompt, or input, to an AI model, influencing it to generate inappropriate, harmful, or misleading outputs. This manipulation could compromise the integrity of the AI model, potentially leading to misinformation, breaches of privacy, or even security threats.

<br />

## Why Must Prompt Injection be Solved?

Prompt injection attacks pose a significant threat to the integrity and security of Language Learning Models (LLMs). They can be used to trick AI models into divulging sensitive information or generating harmful outputs. This can lead to serious consequences including breaches of trust, privacy violations, and potential legal issues. As AI models are increasingly being used in various critical applications - from customer service chatbots to decision-making tools - it's paramount to protect them from such vulnerabilities. 

<br />

## Engineering: The Key to Solving Prompt Injection

Engineering solutions are crucial to counter prompt injection attacks effectively and at scale. These solutions typically involve designing and implementing algorithms, systems, or tools that can detect and prevent these attacks. 

Given the dynamic nature of AI and the ever-evolving landscape of cyber threats, it's not enough to rely on manual checks or ad-hoc solutions. These methods don't scale well and can become impractical as the volume and complexity of data processed by the AI models increase.

<br />

A well-engineered solution can:

    - Analyze large volumes of data quickly and accurately.
    - Adapt and learn from new data and evolving threats.
    - Minimize the risk of false positives and false negatives.
    - Maintain the performance and usability of the AI models.

A scalable solution is particularly important in production environments, where AI models may need to process vast amounts of data in real time. Such a solution can handle increasing workloads without a proportional increase in resources, making it efficient and cost-effective.

In summary, to ensure the safe and effective use of AI models in our digital world, it's imperative to engineer robust, scalable solutions to counter prompt injection attacks.
    
    In this guide, we detail a comprehensive, scalable solution to counter prompt injection attacks on language learning models (LLMs). Our approach can be packaged as a library or a microservice that resides between the user input and the LLM, analyzing and sanitizing the data to prevent potential injection attacks.

<br />

## Intent-Based Semantic Similarity Check
<br />

This approach revolves around comparing the LLM's output with a predefined set of typical responses for each intent. If the output's semantic similarity doesn't align with the expected responses, it's flagged as potentially suspicious. This process leverages advanced language models, like BERT, to calculate semantic similarity. 

    It's crucial to note that the effectiveness of this technique is directly tied to the quality and diversity of predefined intents and responses. Additionally, regular updates and fine-tuning of the semantic similarity model can enhance the overall performance.

This is a new approach where we use predefined intents and their typical responses for semantic similarity. It may make the system more robust against prompt injection attacks. Here's a refactored, scalable, and robust implementation of the idea:

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class IntentBasedSemanticCheck:

    def __init__(self, threshold=0.8):
        # Load a pre-trained model for semantic similarity check
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.threshold = threshold

        # Load typical responses for each intent from a file or a database
        # For example, it could look like this:
        # self.intent_responses = {
        #     "shipping times": [
        #         "Our standard shipping time is 3-5 business days.",
        #         "You can expedite shipping at checkout."
        #     ],
        #     "refund policy": [
        #         "We offer a 30-day refund policy on all our products.",
        #         "You can request a refund through your order page."
        #     ]
        # }
        self.intent_responses = self.load_intent_responses()

    def load_intent_responses(self):
        # TODO: Implement method to load intent_responses from your source
        pass

    def check_for_injection(self, intent, output):
        # If there's no predefined responses for the intent, skip the check
        if intent not in self.intent_responses:
            return False

        # Calculate the semantic similarity between the output and the typical responses
        typical_responses = self.intent_responses[intent]
        output_embedding = self.model.encode([output])[0]
        response_embeddings = self.model.encode(typical_responses)
        similarities = [self.cosine_similarity(output_embedding, response_embedding) for response_embedding in response_embeddings]

        # If the maximum similarity is below the threshold, flag it as potential injection
        if max(similarities) < self.threshold:
            return True
        else:
            return False

    @staticmethod
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
```

In this implementation, we first load a pre-trained model from the `sentence-transformers` library for semantic similarity check. We also load predefined intents and their typical responses from a source (like a file or a database). This could be replaced with a function to load this data from your specific source.

The `check_for_injection` function is used to check if the output from the model is a potential prompt injection. If there's no predefined responses for the intent, we skip the check. We calculate the semantic similarity between the model's output and the typical responses for the given intent. If the maximum similarity is below a set threshold, we flag it as a potential prompt injection.

This implementation is more robust and can be scaled to handle a large number of intents and their typical responses. The threshold can be adjusted based on your specific use case to balance between false positives and false negatives. The semantic similarity model can also be replaced with any other model that suits your use case.

    Please note that the exact performance of this approach would depend on the quality and diversity of your predefined intents and their responses. It would also depend on the performance of the semantic similarity model. Regular updates and retraining of these resources might be needed to maintain high performance.

<br />

## Input Sanitization
<br />

The goal is to cleanse user input by removing or escaping potentially harmful characters or strings. This technique is widely used in preventing SQL injection attacks. In the context of LLMs, sanitization may involve removing or escaping certain special characters or command-like strings that could be utilized for an attack. 

    It's important to balance between security and usability in this process. Over-sanitization might restrict user input and harm the usability of the system. A refined sanitization approach takes this into account and ensures the user experience is not compromised.

The code below includes advanced checks and sanitization techniques, while also preserving the natural language input as much as possible

```python
import re
from html import escape

class SecurePrompt:
    def __init__(self):
        # Add more harmful patterns as identified
        # Example: UUID pattern, sensitive keywords etc.
        self.harmful_patterns = [
            r"[0-9a-f]{32}",
            r"\b(password|token|secret)\b",
        ]

        # Known harmful symbols or sequences
        self.harmful_symbols = ["{", "}", "<", ">", "$"]

        # Precompile the regex patterns for efficiency
        self.compiled_patterns = [re.compile(pattern) for pattern in self.harmful_patterns]

    def sanitize(self, prompt):
        # HTML escape to preserve text while removing potential harmful symbols
        sanitized_prompt = escape(prompt)

        # Remove known harmful symbols
        for symbol in self.harmful_symbols:
            sanitized_prompt = sanitized_prompt.replace(symbol, "")

        return sanitized_prompt

    def validate(self, prompt):
        for compiled_pattern in self.compiled_patterns:
            if compiled_pattern.search(prompt):
                return False
        return True

    def process_prompt(self, prompt):
        sanitized_prompt = self.sanitize(prompt)
        if not self.validate(sanitized_prompt):
            raise Exception("The prompt contains harmful content.")
        return sanitized_prompt
```

- The `sanitize` method now uses HTML escaping to help preserve the original text input, while also escaping potentially harmful characters. Additionally, it removes known harmful symbols that are not handled by HTML escaping.
- The `validate` method checks the sanitized prompt against a list of precompiled regex patterns, which represent harmful patterns we want to block. The patterns are precompiled for efficiency.
- The `process_prompt` method remains the same, as it simply combines the sanitization and validation steps.

    Note that these are only basic examples of what could be done for input sanitization and validation. The actual implementation could be much more complex, depending on the specifics of your use case and the potential threats you're trying to mitigate.

<br />

## Heuristics-Based Filtering
<br />

This technique involves formulating a set of rules or patterns that are likely indicative of an injection attack. The user's input is then screened against these patterns. Any input matching a pattern is flagged as potentially malicious. 

    The process could involve examining certain keywords, phrases, or structures that might suggest an attack. Machine learning can be integrated to continually enhance and refine these rules based on incoming data. A well-maintained and frequently updated set of rules can significantly improve the accuracy and effectiveness of heuristic-based filtering.


Implementing a denylist approach combined with machine learning to flag potential prompt injection attacks can be a viable and effective option. The denylist would help to catch known harmful prompts, while the machine learning model could potentially identify new, previously unseen threats.

Here's a simple, scalable implementation:

```python
import re

class HeuristicFilter:
    def __init__(self):
        # A list of known harmful prompts
        # Example: "password", "token", "secret"
        self.denylist = ["harmful_prompt1", "harmful_prompt2"]

        # Precompile the regex patterns for efficiency
        self.denylist_patterns = [re.compile(pattern) for pattern in self.denylist]

        # TODO: Initialize machine learning model here
        # self.ml_model = load_model('ml_model.pkl')

    def filter(self, prompt):
        # Denylist check
        for pattern in self.denylist_patterns:
            if pattern.search(prompt):
                return False

        # Machine Learning model check
        # Here we assume the model returns a probability of being malicious
        # If the probability is greater than a threshold, we flag it
        # prob_malicious = self.ml_model.predict([prompt])
        # if prob_malicious > THRESHOLD:
        #     return False

        # If neither the denylist nor the ML model flagged the prompt, we consider it safe
        return True
```

In this code, we initialize the `HeuristicFilter` with a denylist of harmful prompts, and we precompile these into regex patterns for efficiency. 
In the `filter` method, we first check if the prompt matches any of the denylist patterns. If it does, we immediately return False, indicating a potentially malicious prompt.

Next, we pass the prompt to a machine learning model, which predicts the likelihood of the prompt being malicious. If this probability exceeds a certain threshold, we also return False. The machine learning model is not implemented in this example, as it would involve considerable additional code and resources.

If the prompt passes both the denylist and machine learning checks, we return True, indicating that it is likely safe. This combination of denylist and machine learning checks provides a robust, scalable solution to prompt injection attacks.

    Please note, this is a basic implementation and can be further enhanced to meet specific needs. The machine learning model needs to be trained on a dataset of normal and malicious prompts, which might be a challenging task due to the novelty of prompt injection attacks. However, with sufficient data and regular retraining, this approach could effectively identify and block new types of attacks as they emerge.