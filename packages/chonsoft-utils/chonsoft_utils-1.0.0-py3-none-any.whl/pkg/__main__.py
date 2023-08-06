from configparser import ConfigParser
from importlib import resources

def main():
    config_parser= ConfigParser()
    
    config_parser.read_string(resources.read_text('pkg','config.txt'))
    print(config_parser.sections())
    print(config_parser.get('feed','url'))
    print('python -m pkg: executing a package')

if __name__ == '__main__':
    main()
    