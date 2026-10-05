"""Runs the sentiment analyzer on 5 examples against the live Claude API.

Requires ANTHROPIC_API_KEY in .env. Run: python test.py
"""

import json
import sys

from sentiment import SentimentError, analyze_sentiment

EXAMPLES = [
    ("I absolutely love this phone, the battery lasts forever!", "positive"),
    ("The service was terrible and the food arrived cold.", "negative"),
    ("The meeting is scheduled for 3 PM on Tuesday.", "neutral"),
    ("Best vacation ever! The staff went above and beyond.", "positive"),
    ("I waited two hours and nobody helped me. Never coming back.", "negative"),
]


def check_shape(result: dict) -> None:
    assert set(result) == {"sentiment", "confidence_score", "brief_reason"}, result
    assert result["sentiment"] in {"positive", "negative", "neutral"}
    assert 0.0 <= result["confidence_score"] <= 1.0
    assert isinstance(result["brief_reason"], str) and result["brief_reason"]


def test_empty_input() -> bool:
    try:
        analyze_sentiment("   ")
    except SentimentError:
        print("[PASS] empty input raises SentimentError")
        return True
    print("[FAIL] empty input did not raise")
    return False


def main() -> int:
    passed = int(test_empty_input())
    total = 1

    for i, (text, expected) in enumerate(EXAMPLES, 1):
        total += 1
        print(f"\n--- Example {i}: {text}")
        try:
            result = analyze_sentiment(text)
            check_shape(result)
        except SentimentError as e:
            print(f"[FAIL] API error: {e}")
            continue
        except AssertionError as e:
            print(f"[FAIL] bad response shape: {e}")
            continue

        print(json.dumps(result, indent=2))
        if result["sentiment"] == expected:
            print(f"[PASS] expected {expected}")
            passed += 1
        else:
            print(f"[FAIL] expected {expected}, got {result['sentiment']}")

    print(f"\n{passed}/{total} tests passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
