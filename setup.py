import setuptools

setuptools.setup(
    name="loopdb",
    version="0.0.1",
    author="ahester57",
    description="This is my project",
    packages=[*setuptools.find_packages(), "redisconnector", "loopresources"],
)