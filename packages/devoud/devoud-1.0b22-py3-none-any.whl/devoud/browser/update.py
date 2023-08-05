from devoud.browser import *
from devoud.browser.filesystem import FileSystem


def _versions(package_name):
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


def update(package='devoud'):
    print(r'''   __  ______  ____  ___  ____________
  / / / / __ \/ __ \/   |/_  __/ ____/
 / / / / /_/ / / / / /| | / / / __/   
/ /_/ / ____/ /_/ / ___ |/ / / /___   
\____/_/   /_____/_/  |_/_/ /_____/''')
    current_version = None
    server_version = None
    if input('[Обновление]: Проверить доступные обновления? [Y/N]: ').lower() == 'y':
        print('/' * 20)
        print('|')
        print('|---->', package)
        current_version = version(package)
        server_version = _versions(package)[0]
        if current_version == server_version:
            print(f'|   |--> У вас установлена последняя версия({current_version}), обновление не требуется')
        else:
            print('|   |--> Текущая версия:', current_version)
            print('|   |--> Последняя версия на сервере:', server_version)
    print('|')
    print('\\' * 20)
    if current_version == server_version:
        print('[Обновление]: Обновлять нечего')
        return sys.exit()
    if input('[Обновление]: Обновить программу до актуальной версии с сервера? [Y/N]: ').lower() == 'y':
        os.system(f'pip3 install {package} --upgrade')
        FileSystem.create_launch_shortcut()
        print('[Обновление]: Операция завершена!')
        return sys.exit()
    else:
        print('[Обновление]: Операция отменена')
        return sys.exit()


if __name__ == '__main__':
    update()
