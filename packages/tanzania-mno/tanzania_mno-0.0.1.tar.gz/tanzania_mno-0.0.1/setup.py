from setuptools import setup, find_packages

setup(
    packages=['tanzania_mno'],
    name="tanzania_mno",
    version="0.0.1",
    license='MIT',
    author='HERMES GIDO',
    author_email='hermessgido@gmail.com',
    description="A package for checking the Mobile Network Operator (MNO) for a given phone number in Tanzania, can also be used to validate Tanzania phone number and generate random valid phone numbers",
    install_requires=["phonenumbers"],
)
