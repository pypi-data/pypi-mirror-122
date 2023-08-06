from configparser import ConfigParser

def main():
    config_parser= ConfigParser()

    config_parser.read('config.txt',encoding='utf-8')
    print(config_parser.sections())
    print(config_parser.get('feed','url'))
    print('python -m pkg: executing a package')

if __name__ == '__main__':
    main()
    