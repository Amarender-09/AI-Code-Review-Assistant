from app.reviewers.fake_provider import FakeAIProvider


def main():

    provider = FakeAIProvider()

    response = provider.generate_review(
        "Review this Python code for security problems."
    )

    print("AI response:")
    print(response)


if __name__ == "__main__":
    main()