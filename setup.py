from setuptools import setup, find_packages

setup(
    name="StoneCharioteerBot",
    version="0.1dev",
    description=("A telegram bot with plugins.")
    long_description=open("README.md").read(),
    license="MIT",
    author="Vinay Keerthi",
    author_email="ktvkvinaykeerthi@gmail.com",
    keywords="telegram bot plugins",
    url="https://vinay87.github.io/stonecharioteerbot",
    project_urls={
        "Bug Tracker": "https://github.com/vinay87/stonecharioteerbot/issues",
        "Source Code": "https://github.com/vinay87/stonecharioteerbot",
        "Bug Tracker": "https://vinay87.github.io/stonecharioteerbot",
    },
    scripts=["launch_stonecharioteer_bot.py"],
    packages=find_packages(),
    requires=["APScheduler","requests","asyncio","python-telegram-bot","nltk","arrow","celery","sqlalchemy","redis"]
)