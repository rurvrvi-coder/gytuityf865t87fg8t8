import sys
import os

sys.path.insert(0, r'C:\Users\user\MediaGet2\python\Lib\site-packages')
import pip._internal as pip_internal

os.chdir(r"C:\Users\user\Desktop\AhmetzyanovDN\tg bot")

pip_internal.main(['install', 'python-telegram-bot==13.15'])
pip_internal.main(['install', 'python-dotenv==1.0.0'])
pip_internal.main(['install', 'schedule==0.6'])

print("Все зависимости установлены!")