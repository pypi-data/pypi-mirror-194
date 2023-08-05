import toml
def get_version():
    with open('pyproject.toml') as f:
        content=toml.load(f)    
    return content['project']['version']

__version__=get_version()

def get_docs():
    return {
    'pypi':'https://pypi.org/project/torchaction/',
    'github':'https://github.com/TaoChenyue/pytorch-action'
}

__doc__=get_docs()