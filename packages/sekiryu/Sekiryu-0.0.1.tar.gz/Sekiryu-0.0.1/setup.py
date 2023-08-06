import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="Sekiryu",
	version="0.0.1",
	scripts=['server.py','ghidrai.py', 'idai.py', 'binjai.py'],
	author="20urc3",
	author_email="s0urc3.1er@gmail.com",
	description="Automatic decompalition enhanced with ChatGPT",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/20urc3/Sekiryu",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		],
	)
