import setuptools

# with open("README.md", "rb") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="zh-ito-yolov5",
    version="1.0.0.0",
    author="z_road",
    author_email="489469935@qq.com",
    description="AI detection",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/z-zroud/CardScript",
    packages=setuptools.find_packages(),
    # packages=['perso_lib'],
    package_data={

        '':['models/*',
            'utils/*'],
    },
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)