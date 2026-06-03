"""Unit tests for geoexposure.

Real tests are added in Step 7. This file currently asserts only that the
package imports and exposes its public API, so the test framework is wired up.
"""

import geoexposure


def test_package_imports():
    assert geoexposure.__version__ == "0.1.0"


def test_public_api_present():
    for name in geoexposure.__all__:
        assert hasattr(geoexposure, name)
