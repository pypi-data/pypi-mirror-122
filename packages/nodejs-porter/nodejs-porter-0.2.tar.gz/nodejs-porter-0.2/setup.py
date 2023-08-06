#!/usr/bin/python3
"""
setup file for pyporter
"""
# ******************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2020-2020. All rights reserved.
# licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# Author: sunchendong
# Create: 2020-07-31
# Description: provide a tool to package nodejs module automatically
# ******************************************************************************/


import setuptools

setuptools.setup(
    name='nodejs-porter',
    version='0.2',
    url='https://gitee.com/openeuler/nodejsporter',
    author='Chendong Sun',
    author_email='sunchend@outlook.com',
    description="A rpm packager bot for nodejs modules from npmjs.org",
    license="Mulan PSL v2",
    classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    long_description=open('README.md').read(),
    scripts=['nodejsporter'],
)

