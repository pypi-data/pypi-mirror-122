from distutils.core import setup
setup(
	name = 'OpenBubi',
	packages = ['OpenBubi'],
	version = '0.1',
	license='MIT',
	description = 'Open-source module for the Hungarian bike-rental system, MOL Bubi',
	author = 'PiciAkk',
	author_email = 'marci@dbx.hu',
	url = 'https://github.com/piciakk/OpenBubi',
	download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
	keywords = ['MOL Bubi', 'MOL', 'Bubi', 'Budapest', 'Hungary', 'Magyarország', 'API', 'Module', 'Reverse-Engineering'],
	install_requires = [
		  'requests',
		  'geopy',
	  ],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
