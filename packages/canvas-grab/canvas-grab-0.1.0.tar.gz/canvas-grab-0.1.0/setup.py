# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['canvas_grab',
 'canvas_grab.config',
 'canvas_grab.course_filter',
 'canvas_grab.snapshot']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.4,<7.0',
 'canvasapi>=3.0,<4.0',
 'colorama>=0.4,<0.5',
 'jupyter>=1.0,<2.0',
 'packaging>=23,<24',
 'questionary>=1.10,<2.0',
 'retrying>=1.3,<2.0',
 'termcolor>=2.2,<3.0',
 'toml>=0.10,<0.11',
 'tqdm>=4.64,<5.0']

entry_points = \
{'console_scripts': ['canvas_grab = canvas_grab.scripts.__main__:main']}

setup_kwargs = {
    'name': 'canvas-grab',
    'version': '0.1.0',
    'description': 'Downloads all Canvas files to a local directory. Provides GUI for managing the download.\x1b[',
    'long_description': '# canvas-grab\n\n**Looking for Maintainers**\n\n*As I no longer have access to Canvas systems, this project cannot be actively maintained by me. If you are interested in maintaining this project, please email me.*\n\nGrab all files on Canvas LMS to local directory.\n\n*Less is More.* In canvas_grab v2, we focus on stability and ease of use.\nNow you don\'t have to tweak dozens of configurations. We have a very\nsimple setup wizard to help you get started!\n\nFor legacy version, refer to [legacy](https://github.com/skyzh/canvas_grab/tree/legacy) branch.\n\n## Getting Started\n\n1. Install Python\n2. Download canvas_grab source code. There are typically three ways of doing this.\n   * Go to [Release Page](https://github.com/skyzh/canvas_grab/releases) and download `{version}.zip`.\n   * Or `git clone https://github.com/skyzh/canvas_grab`.\n   * Use SJTU GitLab, see [Release Page](https://git.sjtu.edu.cn/iskyzh/canvas_grab/-/tags), or\n     visit https://git.sjtu.edu.cn/iskyzh/canvas_grab\n3. Run `./canvas_grab.sh` (Linux, macOS) or `.\\canvas_grab.ps1` (Windows) in Terminal.\n   Please refer to `Build and Run from Source` for more information.\n4. Get your API key at Canvas profile and you\'re ready to go!\n5. Please don\'t modify any file inside download folder (e.g take notes, add supplementary items). They will be overwritten upon each run.\n\nYou may interrupt the downloading process at any time. The program will automatically resume from where it stopped.\n\nTo upgrade, just replace `canvas_grab` with a more recent version.\n\nIf you have any questions, feel free to file an issue [here](https://github.com/skyzh/canvas_grab/issues).\n\n## Build and Run from Source\n\nFirst of all, please install Python 3.8+, and download source code.\n\nWe have prepared a simple script to automatically install dependencies and run canvas_grab.\n\nFor macOS or Linux users, open a Terminal and run:\n\n```bash\n./canvas_grab.sh\n```\n\nFor Windows users:\n\n1. Right-click Windows icon on taskbar, and select "Run Powershell (Administrator)".\n2. Run `Set-ExecutionPolicy Unrestricted` in Powershell.\n3. If some courses in Canvas LMS have very long module names that exceed Windows limits (which will causes "No such file" error\n   when downloading), run the following command to enable long path support.\n   ```\n   Set-ItemProperty -Path \'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem\' -Name LongPathsEnabled -Type DWord -Value 1 \n   ```\n4. Open `canvas_grab` source file in file browser, Shift + Right-click on blank area, and select `Run Powershell here`.\n5. Now you can start canvas_grab with a simple command:\n    ```powershell\n    .\\canvas_grab.ps1\n    ```\n\n## Configure\n\nThe setup wizard will automatically create a configuration for you.\nYou can change `config.toml` to fit your needs. If you need to\nre-configure, run `./configure.sh` or `./configure.ps1`.\n\n## Common Issues\n\n* **Acquire API token** Access Token can be obtained at "Account - Settings - New Access Token".\n* **SJTU users** 请在[此页面](https://oc.sjtu.edu.cn/profile/settings#access_tokens_holder)内通过“创建新访问许可证”按钮生成访问令牌。\n* **An error occurred** You\'ll see "An error occurred when processing this course" if there\'s no file in a course.\n* **File not available** This file might have been included in an unpublished unit. canvas_grab cannot bypass restrictions.\n* **No module named \'canvasapi\'** You haven\'t installed the dependencies. Follow steps in "build and run from source" or download prebuilt binaries.\n* **Error when checking update** It\'s normal if you don\'t have a stable connection to GitHub. You may regularly check updates by visiting this repo.\n* **Reserved escape sequence used** please use "/" as the path seperator instead of "\\\\".\n* **Duplicated files detected** There\'re two files of same name in same folder. You should download it from Canvas yourself.\n\n## Screenshot\n\n![image](https://user-images.githubusercontent.com/4198311/108496621-4673bf00-72e5-11eb-8978-8b8bdd4efea5.png)\n\n![gui](https://user-images.githubusercontent.com/4198311/113378330-4e755300-93a9-11eb-81a9-c494a8cc7488.png)\n\n## Contributors\n\nSee [Contributors](https://github.com/skyzh/canvas_grab/graphs/contributors) list.\n[@skyzh](https://github.com/skyzh), [@danyang685](https://github.com/danyang685) are two core maintainers.\n\n## License\n\nMIT\n\nWhich means that we do not shoulder any responsibilities for, included but not limited to:\n\n1. API key leaking\n2. Users upload copyright material from website to the Internet\n',
    'author': 'Alex Chi (skyzh)',
    'author_email': 'iskyzh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
