from setuptools import setup, find_packages

setup(
    name='transformer-hacker',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # 依赖列表，例如：'requests>=2.23.0'
    ],
    entry_points={
        'console_scripts': [
            'your-command=your_module:main',
        ],
    },
    author='CC11001100',
    author_email='CC11001100@qq.com',
    description='transformer相关漏洞武器化，方便利用漏洞。',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/llm-sec/transformer-hacker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)