import setuptools


with open('README.md', "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='SimpleBinderGTA5Package',
    version="0.2",
    author='Renich',
    description='Simple binder for GTA5 online',
    packages=['SimpleBinderGTA5Package/'],
    install_requires=['keyboard','pywin32'],
    include_package_data=True,
    python_requires='>=3.6',
)