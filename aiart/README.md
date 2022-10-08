# AI绘画

生成AI画作，基于文心大模型

## 使用

```
指令：
    ai画 ?[风格] [prompt]：生成指定风格和内容的画作
    风格可选：
        卡通（默认）、古风、油画、水彩画、二次元、浮世绘、蒸汽波艺术、
        low poly、像素风格、概念艺术、未来主义、赛博朋克、写实风格、
        洛丽塔风格、巴洛克风格、超现实主义
    示例：
        ai画 卡通 少女，赛博朋克，未来感，高清，3d，cg感，
        精致面容，cg感，唯美，毛发细致，蓝色头发，上半身立绘
```

请在[文心大模型API](https://wenxin.baidu.com/moduleApi/key)获取`API_KEY`与`SECRET_KEY`，并在`__init__.py`中修改：
```python
# 通过 https://wenxin.baidu.com/moduleApi/key 获取
API_KEY = ""
SECRET_KEY = ""
```

