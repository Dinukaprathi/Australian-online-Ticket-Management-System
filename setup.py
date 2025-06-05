from setuptools import setup, find_packages

setup(
    name="aotms",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest==7.4.3",
        "python-dotenv==1.0.0",
        "email_validator==2.1.0",
        "Flask==3.0.2",
        "Flask-WTF==1.2.1",
        "Flask-Login==0.6.3",
        "Werkzeug==3.0.1"
    ],
    python_requires=">=3.8",
    author="MIT Students",
    description="Australian Open Ticket Management System",
    keywords="ticket, management, australian open",
) 