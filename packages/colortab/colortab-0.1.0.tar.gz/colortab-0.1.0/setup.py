from setuptools import setup
setup (
    name = 'colortab' ,
    version = '0.1.0' ,
    py_modules = [ 'colortab' ],
    description='Python-Markdown MkDocs colortab',
    license="MIT",
    
    
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=['markdown', 'extensions', 'mkdocs', 'plugins'],

    
    install_requires  = [ 'markdown>=3.0' ], 
    author="beanflame",
)