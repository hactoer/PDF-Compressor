from Compressor import *
import INIT
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
            position: relatively;
            top: 10px;
            left: 500px;
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: rgba(255,255,255,0.8);
            padding: 5px 10px;
            border-radius: 5px;
            display: inline-block;
        }
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
            CompressedImages=[PIL.Image.open(io.BytesIO(data)) for data in CP(images,quality)[0]] 
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
        st.write(f"版本號:{INIT.version}")
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
    PEND()
    more()
if __name__=="__main__":
    main()