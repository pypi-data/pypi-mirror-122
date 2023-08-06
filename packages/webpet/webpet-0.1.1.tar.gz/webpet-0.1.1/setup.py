import webpet
import setuptools


def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
  name = 'webpet',
  packages = ['webpet'],
  version = webpet.__version__,
  license='MIT',
  description = 'My simple async web framework',
  long_description_content_type='text/markdown',
  long_description=readme(),
  author = 'Aleksandr Lenets (aka momoru_kun)',
  author_email = 'wowgonit@gmail.com',
  url = 'https://github.com/momoru-kun/webpet',
  keywords = ['web', 'http', 'async', 'framework'],
  install_requires=[
          'jinja2==3.0.2',
          'aiofiles==0.7.0'
      ],
  python_requies=">=3.7",
  classifiers=[
    'Environment :: Web Environment',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)