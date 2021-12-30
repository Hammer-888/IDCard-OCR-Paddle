# IDCard-OCR-Paddle
Postprocessing for Paddle OCR
## 背景
笔者就业于某制造业公司，普工招聘小程序每日需要大量调用身份证OCR服务，所以快捷的开发一个OCR服务，减少三方OCR调用的频率，一定程度上减少API的调用费用。
## 使用方法
```
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple paddleocr
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple paddlepaddle
```
## 总结
个人实测PaddleOCR的身份证后处理结果，与阿里的OCR返回结果相比，以姓名和身份证ID为对照条件下，在4200张环境干扰很强的身份证照片中驱动82.8%的一致结果，个人感觉还是比较满意的，对于返回的错误结果将二次调用第三方OCR API。
博客地址：https://zhuanlan.zhihu.com/p/450444018
