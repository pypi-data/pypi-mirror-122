# nodejsporter

#### Description
A rpm packager bot for  nodejsmodules from npmjs.org
It is a tool to create spec file and create rpm for nodejs modules.

#### Installation

1.   python3 setup.py install

#### Preparation
yum install below software before using this tool
1.  gcc
2.  gdb
3.  libstdc++-devel
4.  python3-cffi
5.  nodejs

rpm -ivh nodejs-packaging-23-1.noarch.rpm of this url:
https://gitee.com/chendong1995/nodejs-packaging?_from=gitee_search

#### Instructions

nodejsporter is a tool to create spec file and create rpm for  nodejsmodules
For more details, please use nodejsporter -h

nodejsporter <package> -s -b -d -o  nodejs-<package>.spec

#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request

#### How to create a rpm file

1.  Create spec file, nodejsporter -s module_name
2.  Get required  nodejsmodules, nodejsporter -R module_name
3.  Build and Install rpm package, nodejsporter -B module_name
4.  specify version , nodejsporter -B module_name 1.0.0
5.  For more detail, nodejsporter -h
