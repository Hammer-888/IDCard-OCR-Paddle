import re
import json
import string


class IdCardStraight:
    """
    模拟阿里云身份证OCR返回结果，待改进。
    """

    def __init__(self, result):
        self.result = [
            i.replace(" ", "").translate(str.maketrans("", "", string.punctuation))
            for i in result
        ]
        self.out = {"Data": {"FrontResult": {}}}
        self.res = self.out["Data"]["FrontResult"]
        self.res["Name"] = ""
        self.res["IDNumber"] = ""
        self.res["Address"] = ""
        self.res["Gender"] = ""
        self.res["Nationality"] = ""

    def birth_no(self):
        """
        身份证号码
        """
        for i in range(len(self.result)):
            txt = self.result[i]

            # 身份证号码
            if "X" in txt or "x" in txt:
                res = re.findall("\d*[X|x]", txt)
            else:
                res = re.findall("\d{16,18}", txt)

            if len(res) > 0:
                if len(res[0]) == 18:
                    self.res["IDNumber"] = res[0].replace("号码", "")
                    self.res["Gender"] = "男" if int(res[0][16]) % 2 else "女"
                break

    def full_name(self):
        """
        身份证姓名
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if ("姓名" or "名" in txt) and len(txt) > 2:
                res = re.findall("名[\u4e00-\u9fa5]{1,4}", txt)
                if len(res) > 0:
                    self.res["Name"] = res[0].split("名")[-1]
                    self.result[i] = "temp"  # 避免身份证姓名对地址造成干扰
                    break

    def sex(self):
        """
        性别女民族汉
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if "男" in txt:
                self.res["Gender"] = "男"

            elif "女" in txt:
                self.res["Gender"] = "女"

    def national(self):
        # 性别女民族汉
        for i in range(len(self.result)):
            txt = self.result[i]
            res = re.findall(".*民族[\u4e00-\u9fa5]+", txt)

            if len(res) > 0:
                self.res["Nationality"] = res[0].split("族")[-1]
                break

    def address(self):
        """
        身份证地址
        """
        addString = []
        for i in range(len(self.result)):
            txt = self.result[i]
            txt = txt.replace("号码", "")
            if "公民" in txt:
                txt = "temp"
            # 身份证地址

            if (
                "住址" in txt
                or "址" in txt
                or "省" in txt
                or "市" in txt
                or "县" in txt
                or "街" in txt
                or "乡" in txt
                or "村" in txt
                or "镇" in txt
                or "区" in txt
                or "城" in txt
                or "组" in txt
                or "号" in txt
            ):

                if "住址" in txt or "省" in txt or "址" in txt:
                    addString.insert(0, txt.split("址")[-1])
                else:
                    addString.append(txt)

                self.result[i] = "temp"

        if len(addString) > 0:
            self.res["Address"] = "".join(addString)
        else:
            self.res["Address"] = ""

    def predict_name(self):
        """
        如果PaddleOCR返回的不是姓名xx连着的，则需要去猜测这个姓名，此处需要改进
        """
        for i in range(len(self.result)):
            txt = self.result[i]
            if self.res["Name"] == "":
                if len(txt) > 1 and len(txt) < 5:
                    if (
                        "性别" not in txt
                        and "姓名" not in txt
                        and "民族" not in txt
                        and "住址" not in txt
                        and "出生" not in txt
                        and "号码" not in txt
                        and "身份" not in txt
                    ):
                        result = re.findall("[\u4e00-\u9fa5]{2,4}", txt)
                        if len(result) > 0:
                            self.res["Name"] = result[0]
                            break

    def run(self):
        self.full_name()
        self.national()
        self.birth_no()
        self.address()
        self.predict_name()
        return json.dumps(self.out)
