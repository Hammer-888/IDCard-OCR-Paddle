from paddleocr import PaddleOCR
from common import IdCardStraight

# 初始化ocr模型和后处理模型
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
postprocessing = IdCardStraight

# 定义文件路径
img_path = "D:xx.jpeg"

# 获取模型检测结果
result = ocr.ocr(img_path, cls=True)

# 将检测到的文字放到一个列表中
txts = [line[1][0] for line in result]

# 将结果送入到后处理模型中
id_result = postprocessing.run(txts)
