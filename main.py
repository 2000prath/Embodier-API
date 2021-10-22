from fastapi import FastAPI
from typing import Optional
from fastapi.responses import HTMLResponse,RedirectResponse,StreamingResponse
import embodier
import io


app = FastAPI(docs_url="/",title="Embodier",
    description="It generates the unique avatar, which save image into PNG, JPG, or Base64 string. you can use this package to give avatar to newly registered users on your application.",
    version="1.0.6",
    terms_of_service="https://github.com/2000prath/embodier/",
    contact={
        "name": "Prathamesh Patkar",
        "url": "https://pypi.org/project/embodier/",
        "email": "2000prath@gmail.com",
    },
    license_info={
        "name": "MIT License (MIT)"
    })
obj = embodier.AvatarGenerator()

@app.get("/api/BlockAvatar",response_class=HTMLResponse)
async def blockAvatar(background_color:Optional[str] = None,border:Optional[str]=None,border_width: Optional[int] = None,boxes: Optional[int] = None,pixels: Optional[int] = None,download:Optional[str]=None,base64:Optional[str]=None):
    background_color_ = 'lightgrey'
    border_ = True
    border_width_ = 25
    boxes_ = 5
    pixels_ = 300
    if background_color:
        background_color_ = background_color
    if border == 'false':
        border_ = False
    if border == 'true':
        border_ = True
    if border_width:
        border_width_ = border_width
    if boxes:
        boxes_ = boxes
    if pixels: 
        pixels_ = pixels
    
    img = obj.BlockAvatar(xy_axis=boxes_,pixels=pixels_,background_color=background_color_,border=border_,border_width=border_width_) 
    
    if download == "true" and base64 == None:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        buffered.getvalue()
        return StreamingResponse(io.BytesIO(buffered.getvalue()), media_type="image/png")
    if base64 == "true" and download == None :
        return obj.toBase64(img).decode('utf-8')

    string = obj.toBase64(img).decode("utf-8") 
    html ="""
    <div>
        <img src='data:image/png;base64, """+str(string)+""" ' alt='Auto generated image by embodier package' title="https://github.com/2000prath" />
        </div>
    """
    return html


@app.get("/api/TextAvatar",response_class=HTMLResponse)
async def TextAvatar(background_color:Optional[str] = None,text:Optional[str]=None,download:Optional[str]=None,base64:Optional[str]=None):
    background_color_ = '#808080'
    text_ = ""

    if background_color:
        background_color_ = background_color
    if text:
        text_ = text
    else:
        return "{'error':'Cannot create image without text','solution':'Please provide text in query string e.g: ?text=PE'}"
    
    
    img = obj.TextAvatar(text=text_,background_color=background_color_) 
    
    if download == "true" and base64 == None:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        buffered.getvalue()
        return StreamingResponse(io.BytesIO(buffered.getvalue()), media_type="image/png")
    if base64 == "true" and download == None :
        return obj.toBase64(img).decode('utf-8')

    string = obj.toBase64(img).decode("utf-8") 
    html ="""
    <div>
        <img src='data:image/png;base64, """+str(string)+""" ' alt='Auto generated image by embodier package' title="https://github.com/2000prath" />
        </div>
    """
    return html