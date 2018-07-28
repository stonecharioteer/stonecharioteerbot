from distutils import setup

setup(
    name="StoneCharioteerBot",
    version="0.1dev",
    long_description=open("README.md").read(),
    author="Vinay Keerthi",
    author_email="ktvkvinaykeerthi@gmail.com",
    packages="stonecharioteerbot",
    requires=["APScheduler","requests","asyncio","python-telegram-bot","nltk","arrow","celery","sqlalchemy","redis"]
)