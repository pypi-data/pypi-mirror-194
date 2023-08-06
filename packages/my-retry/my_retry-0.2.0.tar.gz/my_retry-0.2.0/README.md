# my_retry 0.1

# Author
yaoruiqi

# Introduction
Retry module, You can choose to raise error or return the specified parameters

# Usage
字段解释：

| 字段           | 解释            |
|----------------|----------------|
| times             | 重试次数  |
| sleep_time        | 重试间隔时间    |
| custom_return     | 自定义返回内容 当custom_return[0]为True时，返回custom_return[1]    |
| return_msg        | 重试失败后打印的字符串   |
| show_params       | 重试失败后是否打印传入的参数    |
| show_process      | 是否打印重试过程  |


使用示例：
```python
@MyRetry(times=3, custom_return=(True, False))
def test():
    a = 1 + '1'
    return a

test()

# 运行结果会返回custom_return[1]上定义的False
```
