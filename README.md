# 0.概述

由于现在PDF相关的第三方模块有很大的问题，对第三方模块进行重新处理，

遇到的问题包括：
1.pymuPDF模块中注释不支持中文字体的切换，导致部分中文没法正常显示。
2.pymuPDF模块中使用html格式写入文件，但是使得pdf文件太大
3.pypdf模块中注释字体大小无法改变
4.pypdf模块不同的打开方式，显示的内容不一致，
...

上面是我遇到的一些问题，所以我打算重新写PDF模块。
