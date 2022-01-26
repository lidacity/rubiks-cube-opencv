from setuptools import setup


setup(
    name="rubiks_cube_opencv",
    version="1.0.1",
    description="Parse image rubiks cube to the array of colors",
    keywords="rubiks cube opencv",
    url="https://github.com/lidacity/rubiks-cube-opencv",
    author="lidacity",
    author_email="dzmitry@lidacity.by",
    license="GPLv3",
    scripts=["usr/bin/example.py"],
    packages=["rubiks_cube_opencv"],
)
