"""
Meta related things.

Get the version (PEP 440).

Version structure which is sorted for comparisons `v1 > v2` etc.
  (major, minor, micro, release type, pre-release build, post-release build)
Release types are named is such a way they are comparable with ease.

- pre-releases will have a pre-release build number greater than 0
- post-release is only applied if post-release build is greater than 0
- development branches can be applied to any build. `DEV` is sorted before the current version and
  after the previous version. It also comes before prereleases.
- `DEV` is currently always appended to the end of the release string and given the build of 0.
  If needed, you can specify the optional dev build at the end `Pep440Version(1, 2, 3, DEV, 0, 0, dev=1)`.

Acceptable version releases:

```
Pep440Version(1, 0, 0, FINAL, 0, 0)      1.0
Pep440Version(1, 2, 0, FINAL, 0, 0)      1.2
Pep440Version(1, 2, 3, FINAL, 0, 0)      1.2.3
Pep440Version(1, 2, 0, ALPHA, 4, 0)      1.2a4
Pep440Version(1, 2, 0, BETA, 4, 0)       1.2b4
Pep440Version(1, 2, 0, RC, 4, 0)         1.2rc4
Pep440Version(1, 2, 0, BETA, 1, 1)       1.2b1.post1
Pep440Version(1, 2, 0, FINAL, 0, 1)      1.2.post1
Pep440Version(1, 2, 3, DEV_ALPHA, 1, 0)  1.2.3a1.dev0
Pep440Version(1, 2, 3, DEV, 0, 0)        1.2.3.dev0
Pep440Version(1, 2, 3, DEV, 0, 1)        1.2.3.post1.dev0
Pep440Version(1, 2, 3, DEV_BETA, 2, 1)   1.2.3b2.post1.dev0
Pep440Version(1, 2, 3, DEV, 0, 1, dev=1) 1.2.3.post1.dev1
```

"""
from collections import namedtuple

DEV = 0
DEV_ALPHA = 1
DEV_BETA = 2
DEV_RC = 3
ALPHA = 4
BETA = 5
RC = 6
FINAL = 7

PRE_REL = (DEV_ALPHA, DEV_BETA, DEV_RC, ALPHA, BETA, RC)
REL_MAP = {DEV_ALPHA: "a", DEV_BETA: "b", DEV_RC: "rc", DEV: "", ALPHA: "a", BETA: "b", RC: "rc", FINAL: ""}
DEV_STATUS = {
    DEV: '2 - Pre-Alpha',
    DEV_ALPHA: '2 - Pre-Alpha',
    DEV_BETA: '2 - Pre-Alpha',
    DEV_RC: '2 - Pre-Alpha',
    ALPHA: '3 - Alpha',
    BETA: '4 - Beta',
    RC: '4 - Beta',
    FINAL: '5 - Production/Stable'
}


class Pep440Version(namedtuple('Pep440Version', ['major', 'minor', 'micro', 'release', 'pre', 'post', 'dev'])):
    """Pep440 version."""

    def __new__(cls, major, minor, micro, release, pre, post, *, dev=0):  # pragma: no cover
        """Validate version info."""

        # Ensure all parts are positive integers.
        for value in (major, minor, micro, release, pre, post):
            if not (isinstance(value, int) and value >= 0):
                raise ValueError("All version parts should be integers.")
        # Should be a valid release.
        if not (release in REL_MAP):
            raise ValueError("The value '{}' does not indicate a valid release type.".format(release))
        # Pre-release releases should have a pre-release value.
        if not (pre > 0 if release in PRE_REL else pre == 0):
            raise ValueError("Prereleases should have a value greater than '0'.")
        # Don't allow development build numbers on non-development builds.
        if release >= ALPHA and dev:
            raise ValueError("Cannot specify a dev version on non-development builds.")

        return super(Pep440Version, cls).__new__(cls, major, minor, micro, release, pre, post, dev)

    def _is_pre(self):
        """Is prerelease."""

        return self.release in PRE_REL

    def _is_dev(self):
        """Is development."""

        return self.release < ALPHA

    def _is_post(self):
        """Is post."""

        return self.post > 0

    def _get_dev_status(self):  # pragma: no cover
        """Get development status string."""

        return DEV_STATUS[self.release]

    def _get_canonical(self):  # pragma: no cover
        """Get the canonical output string."""

        # Assemble major, minor, micro version and append `pre`, `post`, or `dev` if needed..
        if self.minor == 0:
            ver = '{}.{}'.format(self.major, self.minor)
        else:
            ver = '{}.{}.{}'.format(self.major, self.minor, self.micro)
        if self._is_pre():
            ver += '{}{}'.format(REL_MAP[self.release], self.pre)
        if self._is_post():
            ver += '.post{}'.format(self.post)
        if self._is_dev():
            ver += '.dev{}'.format(self.dev)

        return ver


__version_info__ = Pep440Version(1, 0, 0, BETA, 1, 0)
__version__ = __version_info__._get_canonical()
