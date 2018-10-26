"""
Meta related things.

Get the version (PEP 440).

Version structure which is sorted for comparisons `v1 > v2` etc.
  (major, minor, micro, release type, pre-release build, post-release build)
Release types are named is such a way they are comparable with ease.

- pre-releases will have a pre-release build number greater than 0
- post-release is only applied if post-release build is greater than 0
- development branches can be applied to pre, post, or final builds as development.
  (`DEV` being equivalent to a development `FINAL`). All `DEV` releases are sorted before `ALPHA`.
- `DEV` is currently always appended to the end of the release string and given the build of 0.
  As we don't manage build releases, `DEV` is more of a way to mark that the current code is in development.
  If we were doing regular builds and putting them on a server, then the build number would be more important.

Acceptable version releases:

```
(1, 0, 0, FINAL, 0, 0)     1.0
(1, 2, 0, FINAL, 0, 0)     1.2
(1, 2, 3, FINAL, 0, 0)     1.2.3
(1, 2, 0, ALPHA, 4, 0)     1.2a4
(1, 2, 0, BETA, 4, 0)      1.2b4
(1, 2, 0, RC, 4, 0)        1.2rc4
(1, 2, 0, BETA, 1, 1)      1.2b1.post1
(1, 2, 0, FINAL, 0, 1)     1.2.post1
(1, 2, 3, DEV_ALPHA, 1, 0) 1.2.3a1.dev0
(1, 2, 3, DEV, 0, 0)       1.2.3.dev0
(1, 2, 3, DEV, 0, 1)       1.2.3.post1.dev0
(1, 2, 3, DEV_BETA, 2, 1)  1.2.3b2.post1.dev0
```

"""
from collections import namedtuple

DEV_ALPHA = 0
DEV_BETA = 1
DEV_RC = 2
DEV = 3
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


class Pep440Version(namedtuple('Pep440Version', ['epoch', 'major', 'minor', 'release', 'pre', 'post'])):
    """Pep440 version."""

    def __new__(cls, epoch, major, minor, release, pre, post):
        """Validate version info."""

        # Should be a valid release.
        if not (release in REL_MAP):  # pragma: no cover
            raise ValueError("The value '{}' does not indicate a valid release type.".format(release))
        # Pre-release releases should have a pre-release value.
        if not (pre > 0 if release in PRE_REL else pre == 0):  # pragma: no cover
            raise ValueError("Prereleases should have a value greater than '0'.")

        return super(Pep440Version, cls).__new__(cls, epoch, major, minor, release, pre, post)

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

    def _get_canonical(self):
        """Get the canonical output string."""

        # Assemble epoch, major, minor version and append `pre`, `post`, or `dev` if needed..
        if self.minor == 0:
            ver = '{}.{}'.format(self.epoch, self.major)
        else:
            ver = '{}.{}.{}'.format(self.epoch, self.major, self.minor)
        if self._is_pre():
            ver += '{}{}'.format(REL_MAP[self.release], self.pre)
        if self._is_post():
            ver += '.post{}'.format(self.post)
        if self._is_dev():
            ver += '.dev0'

        return ver


#   (major, minor, micro, release type, pre-release build, post-release build, development-release)
__version_info__ = Pep440Version(1, 0, 0, BETA, 1, 0)
__version__ = __version_info__._get_canonical()
