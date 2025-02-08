import PIL.Image,fitz,io
import streamlit as st
import time
def PTLI(pdf_file):
    PDF=fitz.open(stream=pdf_file.read(),filetype='pdf')
    images=[]
    for i in range(PDF.page_count):
        page=PDF.load_page(i)
        zoomx=2.0
        zoomy=2.0
        Matrix=fitz.Matrix(zoomx,zoomy).prerotate(0)
        pix=page.get_pixmap(matrix=Matrix,alpha=False)
        img=PIL.Image.open(io.BytesIO(pix.tobytes("png")))
        img=img.convert('RGB') if img.mode != 'RGB' else img
        images.append(img)
    return images
def CI(image,quality):#Compress Image
    ImgByteArr=io.BytesIO()
    image.save(ImgByteArr,format='JPEG',quality=quality)
    return ImgByteArr.getvalue()
def ECS(images,quality):#Estimate compressed size
    SampleSize=0
    for img in images:
        width,height=img.size
        CroppedImg=img.crop((0,0,width//2,height//2))
        CompressedSample=CI(CroppedImg,quality=quality)
        EstimatedFullImageSize=len(CompressedSample)*4
        SampleSize+=EstimatedFullImageSize
    return SampleSize
def ITP(images):#Image To PDF
    pdfbytesarr=io.BytesIO()
    images[0].save(pdfbytesarr,format='PDF',save_all=True,append_images=images[1:])
    return pdfbytesarr.getvalue()
def BTM(precision:int,value)->tuple:#B to MB
        value/=1024*1024
        return round(value,precision)
def CP(images,quality):#compression pro
    CompressedImages=[]
    progress_bar=st.progress(0)
    totalimages=len(images)
    totalsize=0
    for i,img in enumerate(images):
        CompressedImg=CI(img,quality)
        CompressedImages.append(CompressedImg)
        totalsize+=len(CompressedImg)
        progress=int(((i+1)/totalimages)*100)
        progress_bar.progress(progress)
        time.sleep(0.4)
    return (CompressedImages,totalsize)
def CPV(images,quality):#compression preview
    compressed_images_preview=[PIL.Image.open(io.BytesIO(CI(img,quality))) for img in images[:3]]
    st.image(compressed_images_preview,caption=[f'預覽p.{i+1}' for i in range(len(compressed_images_preview))],use_container_width=True)