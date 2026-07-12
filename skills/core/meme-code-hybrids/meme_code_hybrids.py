"""
Meme Code Hybrids Module
Code puns, obfuscated art, educational memes, code golf, and one-liners.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class CodePun:
    """Code pun with implementation."""
    title: str
    punchline: str
    code: str
    language: str = "python"
    educational_note: str = ""


@dataclass
class ObfuscatedArt:
    """Obfuscated code art."""
    title: str
    ascii_art: str
    code: str
    description: str = ""


@dataclass
class EducationalMemeContent:
    """Educational meme content."""
    title: str
    concept: str
    code: str
    explanation: str
    joke: str
    language: str = "python"


@dataclass
class GolfSolution:
    """Code golf solution."""
    challenge: str
    code: str
    language: str = "python"
    char_count: int = 0
    explanation: str = ""


@dataclass
class OneLiner:
    """Impressive one-liner."""
    name: str
    code: str
    language: str = "python"
    output: str = ""
    explanation: str = ""


# ---------------------------------------------------------------------------
# Code Pun Generator
# ---------------------------------------------------------------------------

class CodePunGenerator:
    """Generate programming code puns."""

    PUNS = {
        "python": [
            CodePun(
                title="Python Loop-de-Loop",
                punchline="I tried to catch some fog. I mist.",
                code="fog = []\ntry:\n    fog.append('catch')\nexcept Mist as e:\n    print('I mist')",
                educational_note="Demonstrates try/except error handling",
            ),
            CodePun(
                title="The Pythonic Way",
                punchline="Why do Python programmers have low self-esteem? They're constantly comparing themselves to others.",
                code="me = 10\nothers = [1, 2, 3]\nprint(others > me)  # False, but still hurts",
                educational_note="Python comparison operators and self-worth",
            ),
        ],
        "javascript": [
            CodePun(
                title="Callback Hell",
                punchline="I asked my JavaScript friend how he was. He said 'callback later'.",
                code="function howAreYou(callback) {\n    console.log('callback later');\n    callback();\n}",
                educational_note="Callback pattern in JavaScript",
            ),
        ],
        "rust": [
            CodePun(
                title="Ownership Struggles",
                punchline="Rust programmers don't have ex's. They have borrow checkers.",
                code="fn main() {\n    let relationship = String::from('committed');\n    let you = relationship; // ownership moved!\n    // println!(relationship); // ERROR: value borrowed after move\n}",
                educational_note="Rust ownership and borrowing rules",
            ),
        ],
    }

    def generate(self, language: str = "python", theme: str = "loops") -> CodePun:
        puns = self.PUNS.get(language, self.PUNS.get("python"))
        return puns[0] if puns else CodePun("No pun found", "¯\\_(ツ)_/¯", "print('¯\\_(ツ)_/¯')")


# ---------------------------------------------------------------------------
# Obfuscated Artist
# ---------------------------------------------------------------------------

class ObfuscatedArtist:
    """Create ASCII art from code."""

    def create(self, pattern: str = "spiral", width: int = 40, height: int = 20) -> ObfuscatedArt:
        if pattern == "spiral":
            return self._create_spiral(width, height)
        elif pattern == "wave":
            return self._create_wave(width, height)
        return self._create_checkerboard(width, height)

    def _create_spiral(self, width: int, height: int) -> ObfuscatedArt:
        lines: List[str] = []
        for y in range(height):
            line = ""
            for x in range(width):
                dx = x - width // 2
                dy = y - height // 2
                dist = math.sqrt(dx * dx + dy * dy)
                angle = math.atan2(dy, dx)
                val = (dist + angle * 3) % 4
                char = " .:-=+*#%@" [int(val)]
                line += char
            lines.append(line)
        return ObfuscatedArt(
            title="ASCII Spiral",
            ascii_art="\n".join(lines),
            code="for y in range(h): for x in range(w): ...",
            description="Distance-based ASCII art spiral",
        )

    def _create_wave(self, width: int, height: int) -> ObfuscatedArt:
        lines: List[str] = []
        for y in range(height):
            line = ""
            for x in range(width):
                wave = math.sin(x * 0.2 + y * 0.5) * 3
                if abs(y - height // 2 - wave) < 1:
                    line += "#"
                else:
                    line += " "
            lines.append(line)
        return ObfuscatedArt(
            title="ASCII Wave",
            ascii_art="\n".join(lines),
            code="for y in range(h): line = ''.join('#' if ... else ' ' for x in range(w))",
        )

    def _create_checkerboard(self, width: int, height: int) -> ObfuscatedArt:
        lines = [
            "".join("█" if (x + y) % 2 == 0 else "░" for x in range(width))
            for y in range(height)
        ]
        return ObfuscatedArt(
            title="Checkerboard",
            ascii_art="\n".join(lines),
            code="''.join('█' if (x+y)%2==0 else '░' ...)",
        )


# ---------------------------------------------------------------------------
# Educational Meme
# ---------------------------------------------------------------------------

class EducationalMeme:
    """Create educational memes about programming concepts."""

    def explain(self, concept: str = "recursion", style: str = "meme") -> EducationalMemeContent:
        concepts = {
            "recursion": EducationalMemeContent(
                title="Recursion: It's All About Trust",
                concept="recursion",
                code="def trust_me(n):\n    if n <= 0:\n        return 'Base case reached!'\n    return trust_me(n - 1)  # Trust me, this works",
                explanation="Recursion is when a function calls itself until it reaches a base case.",
                joke="To understand recursion, you must first understand recursion.",
            ),
            "null_pointer": EducationalMemeContent(
                title="The Dreaded NullPointerException",
                concept="null_pointer",
                code="value = get_value()  # Might return None\nprint(value + 1)  # AttributeError: 'NoneType' has no attribute '__add__'",
                explanation="Always check for None before using a value.",
                joke="Why do programmers prefer dark mode? Because light attracts bugs.",
            ),
            "big_o": EducationalMemeContent(
                title="Big O Notation: The Dating Profile",
                concept="big_o",
                code="# O(1) - Direct message\n# O(n) - Check every profile\n# O(n^2) - Check every profile, for every profile\n# O(log n) - Binary search (divide and conquer love)",
                explanation="Big O describes how your algorithm scales.",
                joke="My love life is O(n^2) — I check everyone, for everyone.",
            ),
        }
        return concepts.get(concept, concepts["recursion"])


# ---------------------------------------------------------------------------
# Code Golfer
# ---------------------------------------------------------------------------

class CodeGolfer:
    """Minimize code for common challenges."""

    SOLUTIONS = {
        "reverse_string": {
            "python": ("s[::-1]", 8),
            "javascript": ("s.split('').reverse().join('')", 29),
            "ruby": ("s.reverse", 9),
        },
        "factorial": {
            "python": ("lambda n:1 if n<2 else n*f(n-1)", 33),
            "javascript": ("f=n=>n<2?1:n*f(n-1)", 20),
        },
        "fibonacci": {
            "python": ("f=lambda n:n if n<2 else f(n-1)+f(n-2)", 42),
        },
        "is_palindrome": {
            "python": ("lambda s:s==s[::-1]", 20),
        },
    }

    def get_solution(
        self, challenge: str, language: str = "python"
    ) -> GolfSolution:
        solutions = self.SOLUTIONS.get(challenge, {})
        sol = solutions.get(language, ("# No solution", 0))
        return GolfSolution(
            challenge=challenge,
            code=sol[0],
            language=language,
            char_count=sol[1],
        )


# ---------------------------------------------------------------------------
# One-Liner Factory
# ---------------------------------------------------------------------------

class OneLinerFactory:
    """Create impressive one-liner implementations."""

    def create(self, name: str, language: str = "python") -> OneLiner:
        oneliners = {
            "fibonacci": OneLiner(
                name="Fibonacci Sequence",
                code="[0,1,1,2,3,5,8,13][:n] if (f:=lambda n:n if n<2 else f(n-1)+f(n-2)) else []",
                language="python",
                output="[0, 1, 1, 2, 3, 5, 8, 13]",
            ),
            "palindrome": OneLiner(
                name="Palindrome Check",
                code="lambda s: s == s[::-1]",
                language="python",
                output="True",
            ),
            "sort": OneLiner(
                name="Sort List",
                code="sorted(arr, key=lambda x: x)",
                language="python",
            ),
            "flatten": OneLiner(
                name="Flatten Nested List",
                code="lambda l: [x for sub in l for x in (flatten(sub) if isinstance(sub,list) else [sub])]",
                language="python",
            ),
            "prime_check": OneLiner(
                name="Prime Number Check",
                code="lambda n: all(n%i for i in range(2,int(n**0.5)+1)) and n>1",
                language="python",
            ),
        }
        return oneliners.get(name, OneLiner(name="Unknown", code="# Not found"))


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Meme Code Hybrids Demo")
    print("=" * 60)

    print("\n[1] Code Puns")
    gen = CodePunGenerator()
    pun = gen.generate("python")
    print(f"  Title: {pun.title}")
    print(f"  Joke: {pun.punchline}")
    print(f"  Code: {pun.code[:60]}...")

    print("\n[2] ASCII Art")
    artist = ObfuscatedArtist()
    art = artist.create("spiral", 30, 15)
    print(f"  Title: {art.title}")
    print(art.ascii_art)

    print("\n[3] Educational Memes")
    meme = EducationalMeme()
    content = meme.explain("recursion")
    print(f"  Title: {content.title}")
    print(f"  Joke: {content.joke}")
    print(f"  Code: {content.code[:60]}...")

    print("\n[4] Code Golf")
    golfer = CodeGolfer()
    sol = golfer.get_solution("reverse_string", "python")
    print(f"  Challenge: {sol.challenge}")
    print(f"  Solution: {sol.code}")
    print(f"  Chars: {sol.char_count}")

    print("\n[5] One-Liners")
    factory = OneLinerFactory()
    ol = factory.create("fibonacci")
    print(f"  Name: {ol.name}")
    print(f"  Code: {ol.code[:60]}...")
    print(f"  Output: {ol.output}")

    print("\n" + "=" * 60)
    print("  Meme code hybrids demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
