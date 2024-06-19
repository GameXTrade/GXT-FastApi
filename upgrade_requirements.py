import subprocess

def update_requirements():
    with open('requirements.txt', 'r') as file:
        packages = file.readlines()

    updated_packages = []
    for package in packages:
        package_name = package.split('==')[0]
        result = subprocess.run(['pip', 'install', '--upgrade', package_name], capture_output=True, text=True)
        if result.returncode == 0:
            updated_packages.append(package_name)
            print(f'Successfully updated {package_name}')
        else:
            print(f'Failed to update {package_name}: {result.stderr}')

    with open('requirements.txt', 'w') as file:
        for package in updated_packages:
            result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
            file.write(result.stdout)
            break  # We only need to write once because `pip freeze` lists all packages

update_requirements()
