import PyPDF2
import PyPDF3
import requests
import pandas as pd
import io
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()

    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    lines = str(content).split("\n")
    return lines


userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
            "Chrome/84.0.4147.125 Safari/537.36"
header = {
    'User-Agent': userAgent
}


def m1():
    url = 'http://www.csindex.com.cn/uploads/indices/detail/files/zh_CN/399995factsheet.pdf?t=1625981913'
    res = requests.get(url, stream=True, headers=header)

    print(res.content)
    # document = Document(io.BytesIO(res.content))
    pdf_reader = PyPDF3.PdfFileReader(io.BytesIO(res.content)) 
    pdf_reader.getPage(0)
    text = pdf_reader.getPage(0).extractText()
    abc = text.split('\n')
    print(abc[52])
    #read_pdf(io.BytesIO(res.content))
    pass









def parse(DataIO, save_path):
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(DataIO)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，没有默认为空
    doc.initialize()
    # 检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)

        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages()获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接收该页面的LTPage对象
            layout = device.get_result()
            # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
            # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
            # 想要获取文本就得获取对象的text属性
            for x in layout:
                try:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        with open('%s' % (save_path), 'a') as f:
                            result = x.get_text()
                            print(result)
                            f.write(result + "\n")
                except:
                    print("Failed")


def m2(pdf):
    # print(type(fp))

    # 创建一个与文档关联的解释器
    parser = PDFParser(pdf)

    # PDF 文档的对象
    doc = PDFDocument()

    # 连接解释器与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 初始化文档
    doc.initialize("")

    # 创建PDF资源管理器
    resource = PDFResourceManager()

    # 参数分析器
    laparam = LAParams()

    # 创建一个聚合器
    device = PDFPageAggregator(resource, laparams=laparam)

    # 页面解释器
    interpreter = PDFPageInterpreter(resource, device)

    # 使用文档对象得到页面的集合
    for page in doc.get_pages():
        # 使用页面解释器来读取
        interpreter.process_page(page)

        # 使用聚合器获得内容
        layout = device.get_result()

        for out in layout:

            if hasattr(out, "get_text"):
                print(out.get_text())




if __name__ == '__main__':
    m1()

    # with open(r'D:\Downloads\399986factsheet.pdf', 'rb') as pdf_html:
    #     m = read_pdf(pdf_html)
    #     print(m)

