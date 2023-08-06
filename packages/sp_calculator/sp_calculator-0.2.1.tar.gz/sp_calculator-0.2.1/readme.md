A simple calculator package

Setting up a virtual development environment:

1. navigate to project root dir
2. . ./env/bin/activate

To download new packages activate virtual env and run:

1. python3 ./env/bin/pip3 install {package_name}

To run tests activate virtual env and run:

1. pytest

To lock dependencies activate virtual env and run:
python3 ./env/bin/pip3 freeze > requirements.txt
