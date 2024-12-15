## Description
This is a canvas course files downloader that aims to aid students backup their resources at the end of the term. It utlizes multiple libraries, mainly the CanvasAPI.

## How to setup
1. Download Dependencies using this command
```
pip install -r requirements.txt
```
2. create a .env file containing the

    2.1 canvas access token (https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312)
   
    2.2 base url ("canvas.infrastructure.com")
```
CANVAS_TOKEN=<insert token here>
API_URL=<insert base url here>
```
3. Run the code 
```
python main.py
```

## PS 
When I was almost finished coding the mini project I found out that canvas already has this feature lol. It was a good experience nontheless. If you guys want you can check it.
1. Go to "<your canvas base url .com>/epub_exports" and you will see it
