"""Test for PEP 562 backport."""
import unittest
import warnings


class TestPep562(unittest.TestCase):
    """Tests for the PEP 562 package."""

    def test_overrides(self):
        """Test overrides."""

        from . import overridden

        # Capture overridden `__dir__` results
        self.assertEqual(['__version__', 'version'], dir(overridden))

        # Capture a successful attribute access
        self.assertEqual((1, 0, 0), overridden.__version__)

        # Capture the overridden deprecation
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            version = overridden.version
            # Verify some things
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))
            self.assertEqual(overridden.__version__, version)

        # Capture a failed attribute access
        with self.assertRaises(AttributeError):
            overridden.not_here

    def test_no_overrides(self):
        """Test no overrides."""

        from . import not_overridden

        # Capture `__dir__` results
        self.assertNotEqual(['__version__'], dir(not_overridden))
        self.assertTrue('__version__' in dir(not_overridden))

        # Capture a successful attribute access
        self.assertEqual((1, 0, 0), not_overridden.__version__)

        # Capture a failed attribute access
        with self.assertRaises(AttributeError):
            not_overridden.not_here
