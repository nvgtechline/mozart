from setuptools import setup, find_packages

setup(
    name='mozart',
    version='1.0',
    long_description='HySDS job orchestration/worker web interface',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask>=0.10.1', 'gunicorn>=19.1.1', 'gevent>=1.1.1',
                      'eventlet>=0.17.4', 'supervisor>=3.1.3',
                      'requests>=2.7.0', 'Flask-SQLAlchemy>=1.0',
                      'Flask-WTF>=0.10.0', 'Flask-DebugToolbar>=0.9.0',
                      'Flask-Login>=0.3.2', 'simpleldap>=0.8', 
                      'simplekml>=1.2.3', 'tornado>=4.0.2', 'pika>=0.9.14',
                      'pymongo>=2.7.2', 'boto>=2.38.0', 'python-dateutil',
                      'elasticsearch>=1.0.0,<2.0.0', 'pytz', 'numpy',
                      'flask-restplus>=0.9.2']
)
