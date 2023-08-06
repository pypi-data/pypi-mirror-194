from setuptools import setup

setup(
	name="kenu-ai",
	version="0.2.7",
	description="Python Chat AI",
	author="r4isy",
	author_email="r4isy@kenucorp.com",
	packages=["kenu_ai"],
	install_requires=[
	'googletrans==4.0.0-rc1',
	'requests',
	'kufpy'
	]
	)