from setuptools import setup, find_packages


def requirements():
	requirements_list = list()
	with open('requirements.txt') as pc_requirements:
		for install in pc_requirements:
			requirements_list.append(
				install.strip()
			)
	return requirements_list


setup(
	name='asyncqiwi',
	version='0.1.0',
	description='Qiwi API and QIWI p2p API',
	packages=find_packages(),
	author='VoXDoX',
	author_email='1voxdox1@gmail.com',
	keywords=['qiwi', 'p2p qiwi', 'qiwi-api', 'aioqiwi'],
	zip_safe=False,
    install_requires=requirements(),
	project_urls={
		"Документация": "https://t.me/AsyncQiwi",
		"Телега": "https://t.me/end_soft",
	},
	python_requires=">=3.7"
)
