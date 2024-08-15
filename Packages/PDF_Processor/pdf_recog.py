import fitz  # PyMuPDF
import os
import io
from PIL import Image

class PDFRecog:
    def __init__(self, tempfolder_path="tempfolder"):
        self.tempfolder_path = tempfolder_path
        if not os.path.exists(self.tempfolder_path):
            os.makedirs(self.tempfolder_path)

    def read_pdf(self, pdf_path):
        return fitz.open(pdf_path)

    def get_image_and_block_coordinates(self, document):
        data = []
        for page_num in range(len(document)):
            page = document[page_num]
            page_data = {
                "images": [],
                "blocks": []
            }

            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = document.extract_image(xref)
                image_bytes = base_image["image"]
                page_data["images"].append({
                    "index": img_index,
                    "bytes": image_bytes
                })

            blocks = page.get_text("blocks")
            for block_index, block in enumerate(blocks):
                bbox = block[:4]
                page_data["blocks"].append({
                    "index": block_index,
                    "bbox": bbox
                })

            data.append(page_data)
        return data

    def save_images(self, data, document, binarize=False, dpi=300):
        for file in os.listdir(self.tempfolder_path):
            file_path = os.path.join(self.tempfolder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error while cleaning up the output folder: {e}")

        for page_num, page_data in enumerate(data):
            page = document[page_num]
            
            for img_data in page_data["images"]:
                img = Image.open(io.BytesIO(img_data["bytes"]))
                img = img.convert("L")  # 转换为灰度图像
                
                # 提高分辨率
                original_size = img.size
                new_size = (int(original_size[0] * dpi / 72), int(original_size[1] * dpi / 72))
                img = img.resize(new_size, Image.LANCZOS)
                
                if binarize:
                    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化
                
                img.save(os.path.join(self.tempfolder_path, f"page_{page_num + 1}_img_{img_data['index'] + 1}.png"), dpi=(dpi, dpi))

            for block_data in page_data["blocks"]:
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72), clip=fitz.Rect(block_data["bbox"]))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = img.convert("L")  # 转换为灰度图像
                
                if binarize:
                    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化
                
                img.save(os.path.join(self.tempfolder_path, f"page_{page_num + 1}_block_{block_data['index'] + 1}.png"), dpi=(dpi, dpi))

    def simp_recog(self, pdf_path, binarize=False, dpi=300):
        """
        调用 read_pdf, get_image_and_block_coordinates 和 save_images 方法，
        输入 pdf_path，直接向 tempfolder_path 中传入全部 png。
        :param pdf_path: 输入的 PDF 文件路径
        :param binarize: 是否进行二值化处理，默认为 False
        :param dpi: 输出图像的 DPI，默认为 300
        """
        document = self.read_pdf(pdf_path)
        data = self.get_image_and_block_coordinates(document)
        self.save_images(data, document, binarize, dpi)
        document.close()  # 关闭文档
