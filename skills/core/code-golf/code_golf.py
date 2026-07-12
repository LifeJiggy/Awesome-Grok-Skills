"""
Code Golf Module
Language tricks, common patterns, and minimal solutions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class GolfSolution:
    """Code golf solution."""
    challenge: str
    code: str
    language: str
    char_count: int = 0
    explanation: str = ""


@dataclass
class LanguageTrick:
    """Language-specific golf trick."""
    name: str
    description: str
    example: str
    chars_saved: int = 0


@dataclass
class ChallengeDefinition:
    """Code golf challenge definition."""
    name: str
    description: str
    input_format: str = ""
    output_format: str = ""
    examples: List[Dict[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Golf Solver
# ---------------------------------------------------------------------------

class GolfSolver:
    """Solve code golf challenges."""

    SOLUTIONS: Dict[str, Dict[str, str]] = {
        "fizzbuzz": {
            "python": "for i in range(1,101):print('Fizz'*(i%3<1)+'Buzz'*(i%5<1)or i)",
            "javascript": "for(i=1;i<=100;i++)console.log(i%15?i%3?i%5?i:'Buzz':'Fizz':'FizzBuzz')",
            "ruby": "100.times{|i|puts i%15<1?'FizzBuzz':i%3<1?'Fizz':i%5<1?'Buzz':i+1}",
        },
        "reverse_string": {
            "python": "s[::-1]",
            "javascript": "[...s].reverse().join('')",
            "ruby": "s.reverse",
            "bash": "rev",
        },
        "fibonacci": {
            "python": "f=lambda n:n if n<2 else f(n-1)+f(n-2)",
            "javascript": "f=n=>n<2?n:f(n-1)+f(n-2)",
        },
        "is_palindrome": {
            "python": "lambda s:s==s[::-1]",
            "javascript": "s=>[...s].reverse().join('')==s",
        },
        "sort_numbers": {
            "python": "lambda l:sorted(l)",
            "javascript": "a=>a.sort((a,b)=>a-b)",
        },
        "factorial": {
            "python": "f=lambda n:n<2 or n*f(n-1)",
            "javascript": "f=n=>n<2?1:n*f(n-1)",
        },
        "is_prime": {
            "python": "lambda n:n>1 and all(n%i for i in range(2,int(n**.5)+1))",
            "javascript": "n=>{for(i=2;i*i<=n;i++)if(n%i<1)return!1;return n>1}",
        },
        "binary_search": {
            "python": "f=lambda a,t,l=0,h=None:h is None and f(a,t,0,len(a)-1) or l>h?-1:(m:=l+h>>1,a[m]==t and m or(a[m]<t and f(a,t,m+1,h)or f(a,t,l,m-1)))",
        },
        "matrix_transpose": {
            "python": "lambda m: list(map(list,zip(*m)))",
        },
    }

    def solve(
        self,
        challenge: str,
        language: str = "python",
        **kwargs,
    ) -> GolfSolution:
        solutions = self.SOLUTIONS.get(challenge, {})
        code = solutions.get(language, f"# No {language} solution for {challenge}")
        return GolfSolution(
            challenge=challenge,
            code=code,
            language=language,
            char_count=len(code),
        )

    def get_shortest(
        self, challenge: str
    ) -> GolfSolution:
        solutions = self.SOLUTIONS.get(challenge, {})
        shortest = min(solutions.items(), key=lambda x: len(x[1])) if solutions else ("none", "# No solutions")
        return GolfSolution(
            challenge=challenge,
            code=shortest[1],
            language=shortest[0],
            char_count=len(shortest[1]),
        )


# ---------------------------------------------------------------------------
# Language Tricks
# ---------------------------------------------------------------------------

class LanguageTricks:
    """Language-specific code golf tricks."""

    TRICKS: Dict[str, List[LanguageTrick]] = {
        "python": [
            LanguageTrick("Slice Reverse", "Reverse string with slice", "s[::-1]", 15),
            LanguageTrick("Walrus Operator", "Assign and test in one expression", "(n:=x+1)", 5),
            LanguageTrick("List Repeat", "Repeat list element", "[0]*n", 3),
            LanguageTrick("Any/All", "Conditional logic", "any(c for c in s)", 10),
            LanguageTrick("Join", "List to string", "''.join(l)", 5),
            LanguageTrick("Map Lambda", "Apply function to list", "map(f,l)", 5),
            LanguageTrick("Zip Unzip", "Transpose matrix", "zip(*m)", 3),
            LanguageTrick("Conditional Expr", "Inline if-else", "x if c else y", 10),
            LanguageTrick("Abs Difference", "Absolute difference", "abs(a-b)", 5),
            LanguageTrick("Min/Max Clamp", "Clamp value", "min(h,max(l,x))", 8),
        ],
        "javascript": [
            LanguageTrick("Double Not", "Boolean to number", "+!0", 3),
            LanguageTrick("Bitwise OR", "Floor number", "n|0", 2),
            LanguageTrick("Arrow Function", "Short function", "x=>x*2", 10),
            LanguageTrick("Spread Reverse", "Reverse array", "[...a].reverse()", 10),
            LanguageTrick("Template Literals", "String interpolation", "`${x}`", 3),
            LanguageTrick("Comma Operator", "Execute multiple", "a=1,b=2", 5),
            LanguageTrick("Short Bool", "True/False", "!0/!1", 2),
        ],
        "ruby": [
            LanguageTrick("Flip Flop", "Range inclusion", "(1..10).include?(n)", 10),
            LanguageTrick("Times Block", "Repeat N times", "n.times{|i|}", 5),
            LanguageTrick("Grep", "Filter array", "a.grep(/pattern/)", 8),
        ],
    }

    def get_tricks(self, language: str) -> List[LanguageTrick]:
        return self.TRICKS.get(language, [])

    def get_all_tricks(self) -> Dict[str, List[LanguageTrick]]:
        return self.TRICKS


# ---------------------------------------------------------------------------
# Char Counter
# ---------------------------------------------------------------------------

class CharCounter:
    """Count characters in code golf solutions."""

    def count(self, code: str) -> int:
        return len(code)

    def count_no_whitespace(self, code: str) -> int:
        return len(code.replace(" ", "").replace("\n", ""))

    def compare(self, solutions: List[str]) -> Dict[str, int]:
        return {f"solution_{i}": len(s) for i, s in enumerate(solutions)}


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Code Golf Demo")
    print("=" * 60)

    print("\n[1] FizzBuzz")
    solver = GolfSolver()
    fb = solver.solve("fizzbuzz", "python")
    print(f"  Python: {fb.code}")
    print(f"  Chars: {fb.char_count}")

    print("\n[2] Reverse String")
    rev = solver.solve("reverse_string", "python")
    print(f"  Python: {rev.code} ({rev.char_count} chars)")
    rev_js = solver.solve("reverse_string", "javascript")
    print(f"  JS: {rev_js.code} ({rev_js.char_count} chars)")

    print("\n[3] Fibonacci")
    fib = solver.solve("fibonacci", "python")
    print(f"  Python: {fib.code} ({fib.char_count} chars)")

    print("\n[4] Is Palindrome")
    pal = solver.solve("is_palindrome", "python")
    print(f"  Python: {pal.code} ({pal.char_count} chars)")

    print("\n[5] Shortest Solution")
    shortest = solver.get_shortest("reverse_string")
    print(f"  Winner: {shortest.language} with {shortest.code} ({shortest.char_count} chars)")

    print("\n[6] Language Tricks")
    tricks = LanguageTricks()
    py_tricks = tricks.get_tricks("python")
    for t in py_tricks[:5]:
        print(f"  {t.name}: {t.example} (saves ~{t.chars_saved} chars)")

    print("\n[7] Character Counting")
    counter = CharCounter()
    print(f"  Count: {counter.count('s[::-1]')}")
    print(f"  No whitespace: {counter.count_no_whitespace('s [ : : - 1 ]')}")

    print("\n" + "=" * 60)
    print("  Code golf demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
