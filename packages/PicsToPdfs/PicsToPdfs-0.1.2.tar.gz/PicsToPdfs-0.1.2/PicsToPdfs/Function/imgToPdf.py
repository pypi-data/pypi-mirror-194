import glob
import os
import fitz


def img2pdf_all2all(img_path, pic_name_list, pdf_path = "", communication = None):
    """
    文件夹中指定img类型图片转换为相同名称的PDF文件，保存至指定文件夹
    :param img_path: 输入图片文件夹路径
    :param pic_name_list: 图片类型的列表
    :param pdf_path: 指定PDF输出路径, 如果pdf_path为空，转化生成的PDF文件保存在原文件所在文件夹
    :return:
    """

    for root, dirs, files in os.walk(img_path):
        for file  in files:
            img = os.path.join(root, file)
            if communication:
                communication.ThreadSignal.emit(img)
                communication.PBarSignal.emit((files.index(file) + 1) / len(files))
            img_type = os.path.splitext(img)[1]
            #判断文件的后缀名是否在图片类型的列表中
            if img_type in pic_name_list:
                filename = os.path.basename(img).replace(img_type, '.pdf')
                print(filename)
                doc = fitz.open()
                imgdoc = fitz.open(img)
                pdfbytes = imgdoc.convert_to_pdf()
                imgpdf = fitz.open('pdf', pdfbytes)
                doc.insert_pdf(imgpdf)
                dirPath = os.path.split(img)[0]
                if pdf_path:
                    doc.save(pdf_path + '\\' + filename)
                else:
                    doc.save(dirPath + '\\' + filename)
                doc.close
    if communication:
        communication.ThreadSignal.emit("执行完成")


def img2pdf_all2one(img_path, pic_name_list, pdf_path, pdf_name, communication = None):
    """
    文件夹中指定img类型图片转换为一个指定名称的PDF文件，保存至指定文件夹
    :param img_path: 输入图片文件夹路径
    :param img_type: 图片类型，如jpg、png等
    :param pdf_path: 指定PDF输出路径
    :param pdf_name: 指定PDF输出文件名
    :return:
    """

    # doc = fitz.open()
    # for root, dirs, files in os.walk(img_path):
    #     for file  in files:
    #         img = os.path.join(root, file)
    # #         FileList.append(filePath)
    # # for img in FileList:
    #     # 文件后缀名
    #         img_type = os.path.splitext(img)[1]
    #         #判断文件的后缀名是否在图片类型的列表中
    #         if img_type in pic_name_list:
    #             filename = os.path.basename(img).replace(img_type, '.pdf')
    #             print(filename)
    #             doc = fitz.open()
    #             imgdoc = fitz.open(img)
    #             pdfbytes = imgdoc.convert_to_pdf()
    #             imgpdf = fitz.open('pdf', pdfbytes)
    #             doc.insert_pdf(imgpdf)
    #             dirPath = os.path.split(img)[0]
    #             if pdf_path:
    #                 doc.save(pdf_path + '\\' + filename)
    #             else:
    #                 doc.save(dirPath + '\\' + filename)
    #             doc.close

    doc = fitz.open()
    for root, dirs, files in os.walk(img_path):
        for file in files:
            img = os.path.join(root, file)
            if communication:
                communication.ThreadSignal.emit(img)
                communication.PBarSignal.emit((files.index(file) + 1)/len(files))
            img_type = os.path.splitext(img)[1]
            if img_type in pic_name_list:
                imgdoc = fitz.open(img)
                pdfbytes = imgdoc.convert_to_pdf()
                imgpdf = fitz.open('pdf', pdfbytes)
                doc.insert_pdf(imgpdf)
    if communication:
        communication.ThreadSignal.emit("执行完成")
    doc.save(os.path.join(pdf_path, pdf_name))
    doc.close


if __name__ == '__main__':
    # 图片文件夹路径
    # img_path = r"E:\00Pic/"
    # # 图片输出文件夹路径
    # pdf_path = r"E:\00Pic"
    #
    # pdf_name = "1.pdf"
    #
    # pic_name_list = ['.jpg', '.png', '.bmp', '.jpeg', '.JPG', '.PNG', '.JPEG']
    # # 指定png格式转换对应 同名的PDF文件
    # # img2pdf_all2all(img_path, pic_name_list, pdf_path)
    #
    # # 指定png格式图片 转换为 1个指定的PDF文件
    # img2pdf_all2one(img_path, pic_name_list, pdf_path, 'allpng.pdf')
    img_path = input("请输入原图片所在位置")

    # 图片输出文件夹路径
    pdf_path = input("")

    pdf_name = "1.pdf"

    pic_name_list = ['.jpg', '.png', '.bmp', '.jpeg', '.JPG', '.PNG', '.JPEG',".fit", '.tiff']
    # 指定png格式转换对应 同名的PDF文件
    # img2pdf_all2all(img_path, pic_name_list, pdf_path)

    # 指定png格式图片 转换为 1个指定的PDF文件
    img2pdf_all2one(img_path, pic_name_list, pdf_path, 'allpng.pdf')