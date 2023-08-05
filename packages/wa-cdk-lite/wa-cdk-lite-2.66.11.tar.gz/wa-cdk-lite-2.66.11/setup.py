import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "wa-cdk-lite",
    "version": "2.66.11",
    "description": "Well Architected CDK Constructs - Lite",
    "license": "MIT-0",
    "url": "https://github.com/cre8ivelogix-inc",
    "long_description_content_type": "text/markdown",
    "author": "Muhammad S Tahir <muhammad.tahir@cre8ivelogix.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cre8ivelogix-inc/wa-cdk-lite.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "wa_cdk_lite",
        "wa_cdk_lite._jsii"
    ],
    "package_data": {
        "wa_cdk_lite._jsii": [
            "wa-cdk-lite@2.66.11.jsii.tgz"
        ],
        "wa_cdk_lite": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib==2.66.1",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.75.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
