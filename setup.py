from setuptools import setup

PROJECT_URL = "https://github.com/LudwigCRON/veristil"
REQUIRES = []

setup(
    name="veristil",
    use_scm_version={"relative_to": __file__, "write_to": "veristil/version.py"},
    url=PROJECT_URL,
    license="MIT license",
    author="Ludwig CRON",
    author_email="ludwig.cron@gmail.com",
    description="generate verilog waveform from stil test vector file",
    long_description=open("README.md").read(),
    zip_safe=False,
    classifiers=[],
    platforms="any",
    packages=["veristil"],
    include_package_data=True,
    install_requires=REQUIRES,
    setup_requires=["setuptools_scm"],
    entry_points={"console_scripts": ["veristil = veristil:main"]},
    keywords=["veristil"],
)