from setuptools import setup, Extension, find_packages
setup(name='nonebot_plugin_bf1_groptools',
      requires=['requests', 're', 'nonebot2', 'nonebot.adapters.onebot'],
      install_requires=[    # 依赖列表
              'requests',
              'nonebot2>=2.0.0-beta.1',
              'nonebot-adapter-onebot<3.0.0,>=2.0.0-beta.1',
          ],
      version='0.0.13',
      description='Nonebot plugin that verifies BF1 accounts '
                  'and automatically approves group applications and changes business cards.',
      author='qienoob',
      author_email='196859929@qq.com',
        # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      # py_modules=['__init__'],  #指定目录中需要打包的py文件，注意不要.py后缀
      license="apache 3.0",
      )
