import os
try:
    os.system('cd .')
    os.system('pip install poetry')
    os.system('poetry self add poetry-plugin-shell')
    #os.system('poetry shell')
    os.system('poetry install')
    os.system('pip install --editable .')
    print('Completed')
except Exception as e:
    print(f'Failed with Exception {e}')