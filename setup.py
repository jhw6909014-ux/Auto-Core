from setuptools import setup, find_packages

setup(
    name="auto_core",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "google-generativeai",
        "feedparser",
        "requests",
        "python-dotenv",
        "beautifulsoup4",
        "lxml",
        "sqlite-utils",
        "APScheduler",
        "gunicorn",
        "flask",
        "python-slugify"
    ]
)
