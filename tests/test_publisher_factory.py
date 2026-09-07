import importlib
import os

from app.core import config
from app.github.fake_publisher import FakeGitHubPublisher
from app.github.real_publisher import RealGitHubPublisher
import app.github.publisher_factory as publisher_factory


def test_publisher_factory_uses_fake_publisher_in_dry_run():
    original_value = os.environ.get("DRY_RUN")

    try:
        os.environ["DRY_RUN"] = "true"

        importlib.reload(config)

        publisher = publisher_factory.create_github_publisher()

        assert isinstance(
            publisher,
            FakeGitHubPublisher,
        )

    finally:
        if original_value is None:
            os.environ.pop("DRY_RUN", None)
        else:
            os.environ["DRY_RUN"] = original_value

        importlib.reload(config)


def test_publisher_factory_uses_real_publisher_when_dry_run_disabled():
    original_value = os.environ.get("DRY_RUN")
    original_token = os.environ.get("GITHUB_TOKEN")

    try:
        os.environ["DRY_RUN"] = "false"

        # The factory creates GitHubClient without making an API request,
        # so a real token is not needed for this test.
        os.environ["GITHUB_TOKEN"] = "test-token"

        importlib.reload(config)

        publisher = publisher_factory.create_github_publisher()

        assert isinstance(
            publisher,
            RealGitHubPublisher,
        )

    finally:
        if original_value is None:
            os.environ.pop("DRY_RUN", None)
        else:
            os.environ["DRY_RUN"] = original_value

        if original_token is None:
            os.environ.pop("GITHUB_TOKEN", None)
        else:
            os.environ["GITHUB_TOKEN"] = original_token

        importlib.reload(config)