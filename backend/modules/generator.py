import random
from typing import List

class MisinfoGenerator:
    """Generates synthetic fake news samples for system testing and demonstration."""
    
    PATTERNS = [
        "Shocking revelation! {text} is actually a secret agenda.",
        "Sources confirm: {text}. Why is the media silent?",
        "URGENT: {text} - Proof of a massive cover-up leaked online.",
        "BREAKING: New reports suggest {text} might be part of an elaborate hoax.",
        "Everyone is talking about {text}. What they aren't telling you is the hidden truth."
    ]

    @staticmethod
    def generate(text: str) -> str:
        """Applies disinformation linguistic patterns to a real claim."""
        pattern = random.choice(MisinfoGenerator.PATTERNS)
        return pattern.format(text=text)

# Global Instance
misinfo_generator = MisinfoGenerator()
