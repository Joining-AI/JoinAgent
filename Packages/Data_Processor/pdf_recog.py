import fitz  # PyMuPDF
import os
import io
from PIL import Image, ImageOps

class PDFRecog:
    def __init__(self, tempfolder_path="tempfolder"):
        self.tempfolder_path = tempfolder_path
        if not os.path.exists(self.tempfolder_path):
            os.makedirs(self.tempfolder_path)

    def read_pdf(self, pdf_path):
        """
        读取 PDF 文件并返回页面对象的列表。
        :param pdf_path: 输入的 PDF 文件路径
        :return: 页面对象的列表
        """
        document = fitz.open(pdf_path)
        pages = [document.load_page(i) for i in range(len(document))]
        return pages

    def get_image_and_block_coordinates(self, pages):
        """
        处理页面对象，获取图像和文本块的坐标数据结构。
        :param pages: 页面对象的列表
        :return: 图像和文本块的坐标数据结构
        """
        data = []
        for page_num, page in enumerate(pages):
            page_data = {
                "images": [],
                "blocks": []
            }

            # 获取页面上的所有图像引用
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                page_data["images"].append({
                    "index": img_index,
                    "bytes": image_bytes
                })

            # 获取页面上的所有文字块
            blocks = page.get_text("blocks")
            for block_index, block in enumerate(blocks):
                bbox = block[:4]
                page_data["blocks"].append({
                    "index": block_index,
                    "bbox": bbox
                })

            data.append(page_data)
        return data

    def save_images(self, data):
        """
        根据坐标数据结构，保存处理后的图像到指定的文件夹。
        :param data: 图像和文本块的坐标数据结构
        """
        # 检查输出文件夹是否为空，如果不是，清空文件夹
        if os.listdir(self.tempfolder_path):
            for file in os.listdir(self.tempfolder_path):
                file_path = os.path.join(self.tempfolder_path, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error while cleaning up the output folder: {e}")

        for page_num, page_data in enumerate(data):
            # 保存图像
            for img_data in page_data["images"]:
                img = Image.open(io.BytesIO(img_data["bytes"]))
                img = img.convert("L")  # 转换为灰度图像
                img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化
                img.save(os.path.join(self.tempfolder_path, f"page_{page_num + 1}_img_{img_data['index'] + 1}.png"))

            # 保存文本块图像
            for block_data in page_data["blocks"]:
                pix = page.get_pixmap(clip=fitz.Rect(block_data["bbox"]))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = img.convert("L")  # 转换为灰度图像
                img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化
                img.save(os.path.join(self.tempfolder_path, f"page_{page_num + 1}_block_{block_data['index'] + 1}.png"))

    def simp_recog(self, pdf_path):
        """
        调用 read_pdf, get_image_and_block_coordinates 和 save_images 方法，
        输入 pdf_path，直接向 tempfolder_path 中传入全部 png。
        :param pdf_path: 输入的 PDF 文件路径
        """
        pages = self.read_pdf(pdf_path)
        data = self.get_image_and_block_coordinates(pages)
        self.save_images(data)
