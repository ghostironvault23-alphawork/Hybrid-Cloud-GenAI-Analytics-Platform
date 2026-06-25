import json
import urllib.request


API_BASE = "http://localhost:8000"


def post_json(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(path: str) -> dict:
    with urllib.request.urlopen(f"{API_BASE}{path}", timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    print(get_json("/health"))
    answer = post_json(
        "/ask-ai",
        {
            "question": "Why did payment service fail?",
            "role": "Engineer",
            "user_id": "smoke-test",
        },
    )
    print(json.dumps(answer, indent=2))


if __name__ == "__main__":
    main()
