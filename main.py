from fastapi import FastAPI
from typing import Optional
from fastapi.responses import HTMLResponse,RedirectResponse,StreamingResponse
import embodier
from response import Response
import io

description = """

## Embodier API helps you to generate unique awesome avatars 🥶 

## Repsonse
Generated image available in following formats
- PNG
- JPG 
- Base64 string

## Uses
Embodier is a Python package/API that allows you to specify pictures for new profiles for newly registered users in any project.

## Generated sample images
![generatedimg](https://user-images.githubusercontent.com/40172813/125158557-9a494c80-e18f-11eb-956a-d49f42a6a6db.png)
![New Project (3)](https://user-images.githubusercontent.com/40172813/125189848-d5af4e00-e257-11eb-8b22-acc3b7b0c0f9.png)



"""


obj = embodier.AvatarGenerator()
tags_metadata = [
    {
        "name": "Block Image",
        "description": "Image having blocks, which will create unique shape",
    },
    {
        "name": "Text Image",
        "description": "Image having text with unique background color"
    }
]
app = FastAPI(docs_url="/",title="Embodier",
    description=description,
    version="1.0.9",
    terms_of_service="https://pypi.org/project/embodier/1.0.9/",
    contact={
        "name": "Prathamesh Patkar",
        "url": "https://pypi.org/project/embodier/",
        "email": "2000prath@gmail.com",
    },
    license_info={
        "name": "MIT License (MIT)"
    },
    openapi_tags=tags_metadata,
    )

@app.get("/api/BlockAvatar",response_class=HTMLResponse, tags=['Block Image'])
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


@app.get("/api/TextAvatar",response_class=HTMLResponse, tags=['Text Image'])
async def TextAvatar(background_color:Optional[str] = None,text:Optional[str]=None,download:Optional[str]=None,base64:Optional[str]=None):
    background_color_ = '#808080'
    text_ = ""

    if background_color:
        background_color_ = background_color
    if text:
        text_ = text
    else:
        return Response.json(False, "Cannot create avatar without text, Please fill the text field. E.g: text=PE")
    
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