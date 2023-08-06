import setuptools
setuptools.setup(

    name='zuss',
    version='2.1.0',
    description="ZD USB Shifter SDK",
    long_description="Control USB Shifter via python SDK, send serial commands via COM connection.",
    # long_description_content_type='text/markdown',
    author='zhengkunli',
    author_email="1st.melchior@gmail.com",
    python_requires= '>=3.8.0',
    url='https://github.com/Klareliebe7/zuss',
    packages=setuptools.find_packages(),
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires= ["serial","argparse","colorama" ],
    license='MIT',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]

)