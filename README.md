UZIP软件的解压功能的Python复写，个人学习Python期间的练手程序。

### 实现功能
1. 进行解压操作：直接拖入压缩文件或压缩文件所在的文件夹
2. 解压时按密码使用次数降序测试压缩包密码 
3. 支持zip、rar、7z分卷压缩包的解压（支持仅拖入部分分卷包来解压整个分卷压缩包）
4. 解压后自动处理套娃文件夹、套娃压缩包 
5. 解压时跳过指定后缀的文件 
6. 进行解压密码测试：同解压操作 
7. 添加解压密码字典：手工输入、读取剪切板添加 
8. 导出解压密码字典（可附带使用次数） 
9. 查看解压、密码测试的历史记录 
10. 简单的设置选项（删除原文件、仅解压压缩包）
11. 解压以及测试密码时显示进度

### 运行截图
![主页面](https://githubfast.com/PPJUST/OnlyUnzip/blob/main/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE/%E4%B8%BB%E9%A1%B5%E9%9D%A2.png)
![密码页](https://githubfast.com/PPJUST/OnlyUnzip/blob/main/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE/%E5%AF%86%E7%A0%81%E9%A1%B5.png)
![设置页](https://githubfast.com/PPJUST/OnlyUnzip/blob/main/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE/%E8%AE%BE%E7%BD%AE%E9%A1%B5.png)
![测试密码时](https://githubfast.com/PPJUST/OnlyUnzip/blob/main/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE/%E6%B5%8B%E8%AF%95%E5%AF%86%E7%A0%81%E6%97%B6.png)
![解压时](https://githubfast.com/PPJUST/OnlyUnzip/blob/main/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE/%E8%A7%A3%E5%8E%8B%E6%97%B6.png)
![完成全部解压](https://githubfast.com/PPJUST/OnlyUnzip/blob/main/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE/%E5%AE%8C%E6%88%90%E5%85%A8%E9%83%A8%E8%A7%A3%E5%8E%8B.png)

### 其他说明
1. 处理套娃文件夹的逻辑：类似于bandzip。存在多级文件夹且每级文件夹中只有一个文件夹时，递归路径直到找到最深一级的有多个文件/文件夹或仅有单个文件的文件夹
2. 处理套娃压缩包的逻辑：将解压后的文件/文件夹再次执行解压
3. 识别压缩包的方法：使用filetype库+指定文件名后缀，exe文件不会被认定为压缩包

### 存在的问题
1. 在解压exe文件时，可能无法正确测试压缩包的密码
2. 在解压exe文件时，如果exe压缩包已损坏，可能无法正确判断是文件损坏或没有找到对应密码

### 计划
1. 多线程测试密码
2. 优化处理套娃压缩包的逻辑
