"""Setup script for slack_bots package."""

import setup_boilerplate


class Package(setup_boilerplate.Package):
    """Package metadata."""

    name = 'slack-bots'
    description = 'Collection of simple and reusable Slack bot prototypes.'
    url = 'https://github.com/mbdevpl/slack-bots'
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities']
    keywords = ['bot', 'bots', 'chat', 'slack']


if __name__ == '__main__':
    Package.setup()
