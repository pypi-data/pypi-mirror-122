[![](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)
[![](https://img.shields.io/pypi/v/sgg.svg)](https://pypi.org/project/sgg/)

Description
===========

This is a simple tool for creating graphs from the terminal. It reads
files contaning two numeric columns and create a graph from it.

Install
=======

Just the usual python installation pattern (your python version should
be **&gt;= 3.8**)

    pip3 install --user sgg

Examples
========

Consider two files:

<div>

<span class="label">file1.txt</span>

    0 500
    1 550
    2 600
    3 650
    4 700
    5 750
    6 800
    7 850
    8 900
    9 950

</div>

<div>

<span class="label">file2.txt</span>

    0 2
    1 4
    2 8
    3 16
    4 32
    5 64
    6 128
    7 256
    8 512
    9 1024

</div>

To create a graph comparing these two files, we can use the following
command:

    sgg --title '$f(x) = x$ versus $f(x) = x^{2}$' -y '$f(x)$' -x '$x$' -s '-' ' --' -l '$f(x) = x$' '$f(x) = x^{2}$' -f file1.txt file2.txt -c 'darkorange' 'royalblue' --xmin 0  --dest out.png

**NOTE**: If you are reading this file in PyPi you will be not able to
see the png file, so go to the [github
repository](https://github.com/thiagotps/sgg) .

The result are shown below :

![](out.png)
