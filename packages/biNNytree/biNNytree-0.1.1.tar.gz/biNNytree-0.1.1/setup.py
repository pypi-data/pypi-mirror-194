from setuptools import setup, find_packages


VERSION = '0.1.1'
DESCRIPTION = 'Binary Tree Beauty Printer'

LONG_DESCRIPTION = "This package allows to print Binary Tree beautifully." \
                   "To use you need to follow this steps:" \
                   "1. from BinaryTree.tree import *" \
                   "2. Set root: root = Node(1)" \
                   "3. Use this: " \
                   "while True:" \
                   "    value = int(input('Enter a number to add to the binary tree (0 to stop): ').lower())" \
                   "    if value == 0:" \
                   "        break" \
                   "    insert_node(root, value)" \
                   "OR: insert_node(root, 2)," \
                   "    insert_node(root, 4)," \
                   "    insert_node(root, value))"


# Setting up

setup(
    name="biNNytree",
    version=VERSION,
    author="Abraham",
    author_email="ibrohimjon.ismoilov.007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Tree', 'Binary', 'Binary Tree', 'Beauty print', 'Beauty Binary Tree'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
