from setuptools import setup, find_packages

setup(
    name="causal_inference_aagm",
    version="0.0.2",
    author="Azka Rohbiya Ramadani",
    author_email="azkarohbiya@gmail.com",
    description="PropensityScoreMatch is a class for matching propensity score and treatment effect",
    url="https://github.com/azuka31/Tsel-AAGM",
    packages=find_packages(),
    long_description=open('README.md').read(),
    install_requires=[
        "numpy>=1.23.5",
        "pandas==1.5.2",
        "scipy==1.10.0",
        "matplotlib==3.5.1",
        "seaborn==0.11.2",
        "sklearn==1.0.2",
        "statsmodels==0.13.2",
        "scikit-learn>=0.22.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
