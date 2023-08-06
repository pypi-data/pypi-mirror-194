# flake8: noqa
import sys

if sys.version_info >= (3, 6) and __name__ == "formant.sdk.cloud.v2":
    from .client import Client

    sys.modules.update({"formant.sdk.cloud.v2.client": Client})
