# PyDorea

使用 Python 连接 `DoreaDB` 服务！

安装方法：

```
pip install pydorea
```

快速连接：

```python
import pydorea as dorea
client = dorea.DoreaClient (
    ("127.0.0.1", 3451), # 服务连接信息（Web Service）
    "DOREA@TEST"         # 服务连接密码（Web Service）
)
db = client.open("pydorea") # 尝试打开某个库

db.set("foo","bar") # 将一条字符串（“bar”）插入数据库

assert db.get("foo") == "bar"

res = db.execute("info keys") # 直接运行命令

```