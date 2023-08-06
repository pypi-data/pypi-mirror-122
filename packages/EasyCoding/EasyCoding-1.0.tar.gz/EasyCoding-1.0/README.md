#### Easycoding 精简代码集

Python的常用代码太多、不好调用？

原始with open语句写法:

    with open("文件名称","w") as w:
        w.write(要写入的内容、变量名称)
导入easycoding后:

    ec.proFile("文件名称", "w", "内容")

pygame播放音乐原始写法:

    pygame.load(文件路径)
    pygame.play(1, 0)

导入easycoding后:

    ec.musicPlay("play", 文件名)

帮助文档正在编写