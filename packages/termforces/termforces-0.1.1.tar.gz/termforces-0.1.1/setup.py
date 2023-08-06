import setuptools

setuptools.setup(
        name='termforces',
        version='0.1.1',
        author='thematdev',
        author_email='thematdev@thematdev.org',
        description='CLI for Codeforces',
        packages=['termforces', 'termforces.cmds'],
        scripts=['scripts/termforces'],
        install_requires=[
            'click',
            'click_shell',
            'codeforces_scraper>=0.3.0'
        ],
        zip_safe=True,
)
