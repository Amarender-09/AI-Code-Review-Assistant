import importlib
import os

from app.core import config
from app.github.fake_publisher import FakeGitHubPublisher
from app.github.real_publisher import RealGitHubPublisher
import app.github.publisher_factory as publisher_factory


def main():

    # -----------------------------
    # Test DRY_RUN = True
    # -----------------------------

    os.environ["DRY_RUN"] = "true"

    importlib.reload(config)

    publisher = publisher_factory.create_github_publisher()

    print(
        "DRY_RUN=true:",
        type(publisher).__name__,
    )

    assert isinstance(
        publisher,
        FakeGitHubPublisher,
    )

    # -----------------------------
    # Test DRY_RUN = False
    # -----------------------------

    os.environ["DRY_RUN"] = "false"

    importlib.reload(config)

    publisher = publisher_factory.create_github_publisher()

    print(
        "DRY_RUN=false:",
        type(publisher).__name__,
    )

    assert isinstance(
        publisher,
        RealGitHubPublisher,
    )

    print("\nPublisher factory test passed.")


if __name__ == "__main__":
    main()