import setuptools

setuptools.setup(
    name="magento_encryptor",
    author="Israël Hallé",
    author_email="israel.halle@flare.systems",
    url="https://github.com/flared/magento-encryptor-py",
    version="0.2",
    packages=["magento_encryptor",],
    license="License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    long_description=open("README.md").read(),
    install_requires=[
        "PyNaCl==1.4.0"
    ],
    python_requires='>=3.5',
)
