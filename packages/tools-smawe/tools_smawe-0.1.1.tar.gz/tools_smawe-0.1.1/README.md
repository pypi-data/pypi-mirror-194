## 核心功能

> 提供了一个rename()函数, 对目录中的文件进行重命名  
格式为第xxx章  
第某某章必须在一亿章以下  
例如:  
    &ensp;&ensp;&ensp;&ensp;第一百章.txt -> 第100章.txt   
    &ensp;&ensp;&ensp;&ensp;第两千零一章.txt -> 第2001章.txt

---

### **核心函数**

- text_conversion(s):  
    功能: 文本转换  
    描述: 如果s为空, 则返回0.  
    参数s: str
    返回值: 整数
    列如:  
        &ensp;&ensp;&ensp;&ensp;两千零一 -> 2001  
        &ensp;&ensp;&ensp;&ensp;十万零一百 -> 100100

---

**可以自行使用text_conversion函数进行扩展**

#### 示例

    >>> from tools_smawe import text_conversion
    >>> print(text_conversion("两千"))
    2000
    >>> print(text_conversion("两千万零一"))
    20000001