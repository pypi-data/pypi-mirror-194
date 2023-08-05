import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="mecord-cli",
    version="0.0.4",
    author="pengjun",
    author_email="mr_lonely@foxmail.com",
    description="mecord tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="http://xxx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=[],
    data_files=[
        ('widget_template', [
            'mecord/widget_template/config.json',
            'mecord/widget_template/icon.png',
            'mecord/widget_template/index.html'
            ])
    ],
    install_requires=[
        'requests',
        'uuid',
        'qrcode',
        'Image',
        'pillow',
        'protobuf',
        'psutil',
        'qrcode-terminal'

    ],
    dependency_links=[],
    entry_points={
        'console_scripts':[
            'mecord = mecord.main:main'
        ]
    },
    scripts=[
        'mecord/upload.py'
    ],
    python_requires='>=3.10.6',
)