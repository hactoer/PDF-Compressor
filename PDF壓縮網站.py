import PIL.Image,fitz,io
import streamlit as st
import time
def PTLI(pdf_file):#PDF->list of Image
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

def sponser():
    sponsers=[
        {
            'name':None,
            'image_url':None,
            'description':None,
            'link':None
        }
]
    st.markdown('---')
def PEND():# proenterprise name display
    st.markdown(
        """
        <style>
        .custom-title{
            position: absolute;
            top: 1px;
            left 500px;
            font-size: 24px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="custom-title">ProgrammerPython00</div>',unsafe_allow_html=True)
def home():
    st.title("PDF 壓縮器")
    uploadfile=st.file_uploader("上傳PDF檔案",type='pdf')
    if uploadfile is not None:
        st.write(f'上傳的檔案:{uploadfile.name}')
        images=PTLI(uploadfile)
        quality=st.slider("選擇想要的質量*質量越低壓縮越多*",1,50,25)
        estimatized_size=ECS(images,quality)
        st.write(f'**估計壓縮後大小**:{BTM(2,estimatized_size)}MB')
        if st.button("顯示預覽(前三頁)"):
            st.session_state.show_preview=True
            if st.session_state.show_preview:
                st.subheader("**預覽**")
                CPV(images,quality)
                if st.button("關閉?"):
                    st.session_state.show_preview=False
        elif st.button("<進行壓縮>"):
            st.session_state.show_preview=False
            CompressedImages=[PIL.Image.open(io.BytesIO(data)) for data in CP(images,quality)] 
            CompressedPdfBytes=ITP(CompressedImages)
            CompressedSize_mb=BTM(2,len(bytes(CompressedPdfBytes)))
            st.write(f'**壓縮檔案大小為:**{CompressedSize_mb}MB')
            st.download_button(
                label='下載壓縮PDF',
                data=ITP(CompressedImages),
                file_name=f'壓縮{uploadfile.name}',
                mime='application/pdf'
            )
def more():
    st.sidebar.title("更多")
    c=st.sidebar.selectbox("",['首頁','關於網頁','回饋','聯絡我們'])
    if c=='首頁':
        home()
    if c=="關於網頁":
        st.write('歡迎大家使用PDF壓縮工具')
        st.write('本網頁由ProgrammerPython00開發')
        st.write("版本號:1.02.1.250206")
    elif c=='回饋':
        st.write("回饋表單:")
        form_url_embed='<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSeRjS9dlayW4dobwNPXW1fmCe7tUauKw4xgWObbTpY6ORE3Ig/viewform?embedded=true" width="640" height="656" frameborder="0" marginheight="0" marginwidth="0">載入中…</iframe>'
        st.markdown(form_url_embed,unsafe_allow_html=True)
    elif c=='聯絡我們':
        st.write("有任何問題，很歡迎聯絡我們")
        st.markdown('[ProgrammerPython00@gmail.com](mailto:ProgrammerPython00@gmail.com)')
def main(): 
    st.set_page_config(
        page_title='PDF壓縮器',
        page_icon='💾',
        layout='centered'
        
    )
    more()
    PEND()
    
if __name__=="__main__":
    main()
