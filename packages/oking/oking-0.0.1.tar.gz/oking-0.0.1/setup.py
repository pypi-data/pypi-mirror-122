from setuptools import setup, find_packages

setup(
    name="oking",
    version='0.0.1',
    author="Openk Tecnologia",
    author_email="<suporte.b2c@openk.com.br>",
    description='Pacote de integração de produtos, preço, estoque e pedidos com o sistema OkVendas da Openk',
    long_description_content_type="text/markdown",
    long_description='# OKING\n\nOKVendas Integrador Genérico \n\n Realiza conexão com várias ERP\'s',
    packages=find_packages(),
    install_requires=['mysql-connector-python',
                      'schedule',
                      'requests',
                      'configparser',
                      'logger',
                      'cx-Oracle',
                      'jsonpickle'],
    keywords=['python', 'oking', 'openk', 'okvendas', 'ok'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)