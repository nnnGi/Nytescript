import os
try:
    os.system('cd .')
    os.system('pip install poetry')
    os.system('poetry self add poetry-plugin-shell')
    os.system('poetry install')
    os.system('pip install --editable .')
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Completed CLI installation')
except Exception as e:
    print(f'Failed with Exception {e}')
