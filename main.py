import json
import random
import typing
from contextlib import asynccontextmanager
import asyncio
import asqlite
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from werkzeug.utils import secure_filename
from globs import images_directory
from helper import *

get_conn = asqlite.Connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with asqlite.create_pool("usage.db") as app.pool:
        yield


app = FastAPI()
# do lifespan=lifespan when ready.




# modify this table value
# data: typehint = Depends(get_particular_data("objection")



# possible better spot for it may exist.
# possibly write usage.json to a database instead for speed reasons.


with open("example_usage.json", "r") as f:
    usage_data = json.load(f)


@app.get("/")
async def welcome():
    return "Welcome to the Asuna fastapi version."
    # placeholder


@app.get("/usage")
async def get_usage():

    # load example_usage.json for rn
    return JSONResponse(usage_data)
    # use some lifetime object example jdjgapi to in this case grab the usage data


@app.get("/api/random/{image_type}")
async def get_random_image(image_type: str):
    image_type = image_type.lower()
    images = []

    # https://mystb.in/a56e9985c52d7bb3e1?lines=F1-L24
    # I forgot to add random to the route

    # in our version I am going to make a check to make sure the image_type exists first.

    # image_path = images_directory / image_type
    # Secure Path so we don't have to worry about path traversal
    image_path = images_directory / secure_filename(image_type)

    print(image_path)

    if not image_path.exists():
        return JSONResponse({"error": "Picture category not found or there are no images in this category"})
        # TODO: ADD status code that makes sense.
        # TODO: make sure it checks the amount of items in images (we want it to not be None)
    else:
        for image in image_path.iterdir():
            images.append(image)
    
    # add to usage like f"{image_type-api}" or just image_type.
    # i.e. example neko-api

    # add to usage like f"{image_type}" or just image_type.
    # ie example neko
    # ./images/{type}/{random_image}"

    # an online accquitance decided to make this ai version for some reason
    # https://mystb.in/a56e9985c52d7bb3e1?lines=F1-L28

    random_image = random.choice(images)

    # use fileResponse with the path to show this.
    return JSONResponse({"fileName": random_image, "url": f"/images/{image_type}/image/{random_image}"})


"""
get_endpoints could be better but it does do what i need it to do.

The problem is that I have no cached version of directories
filenames and such would probaly be okay being cached too
but I am thinking what if some random person
decides to add another folder and images to that folder?
hence why maybe a utility to generate something might be useful
and it could also make sure they are direct images like
/image.jpg
rather than /lol/image.jpg

basically we need to see if the files actually contain contents within the main folder
/images/{whatever} 
is what we are looking for
not /images/{whatever}/{sub}
"""


@app.get("/api/{image_type}")
async def get_random_image_info(image_type: str):
    image_type = image_type.lower()
    images = []
    image_path = images_directory / secure_filename(image_type)

    # TODO: Clean up image_type or codeql will scream.
    # image_path = images_directory / image_type
    # TODO: reimplement image_path

    # TODO: make sure image_type cannot be a full path rather just a normal str.

    if not image_path.exists():
        return JSONResponse({"error": "Picture category not found or there are no images in this category"})
        # TODO: add status code that makes sense
        # TODO: make sure it checks the amount of items in images
    else:
        for image in image_path.iterdir():
            if image.is_file():
                images.append(image.name)
    # TODO: Make sure the file we want is actually in the images/{folder}/filename.ext (like this)
    # TODO: After we are sure the files are safe then we can do random.choice on images i.e. listing images we want with iterdir and is_file()

    # add to usage like f"{image_type-api}" or just image_type.
    # i.e. example neko-api

    random_image = random.choice(images)

    return JSONResponse({"fileName": random_image, "url": f"/images/{image_type}/image/{random_image}"})

    # an online accquitance decided to make this ai version for some reason
    # https://mystb.in/a56e9985c52d7bb3e1?lines=F1-L60

cached_endpoints = GetSet({})
cached_total_images = GetSet(0)
generate_cache(cached_endpoints, cached_total_images) # We need to generate the cache on startup. 

@app.get("/api")
async def get_endpoints():
    # Begin rebuilding the cache in the background
    asyncio.create_task(generate_cache_async(cached_endpoints, cached_total_images))

    return JSONResponse(
        {"allEndpoints": list(cached_endpoints.get().keys()), "endpointInfo": cached_endpoints.get(), "totalImages": cached_total_images.get()}
    )


@app.get("/images/{image_type}/image/{image_file}")
async def serve_image(image_type: typing.Optional[str] = None, image_file: typing.Optional[str] = None):

    if not image_type:
        return JSONResponse({"error": "The file category is required"})
        # TODO: add status code that makes sense

    if not image_file:
        return JSONResponse({"error": "The file name is required"})
        # TODO: add status code that makes sense

    image_type = image_type.lower()

    # possible useful for handling the filename
    # https://mystb.in/f816711cc955a0eb81?lines=F1-L89

    # better name than just image_file.
    # we need to make sure f"images/{image_type}/image_file}" exist

    # check if file exists with pathlib
    # if file does not exist:
    # {"error": "File not found"}

    # usage normal of {image_type} like neko

    # an online aqquitance sent me this file made by ai:
    # https://mystb.in/a56e9985c52d7bb3e1?lines=F1-L94
    # use fileResponse with the path to show this.
    return FileResponse(images_directory / secure_filename(image_type) / secure_filename(image_file))


@app.get("/images")
async def missing_image_type():
    return JSONResponse({"error": "The file category is required"})
    # TODO: add status code that makes sense


# 404 response for undefined routes
# tested locally on pc and this works also includes_in_schema hides this route.
@app.get("/{full_path:path}", include_in_schema=False)
async def catch_all(full_path: str):
    return HTMLResponse(
        content="<div style='text-align:center'><h3><a href='/'>Go Home</a><br/>4owo4 page not found</div>",
        status_code=404,
    )


if __name__ == "__main__":
    base_url = "http://127.0.0.1:42069"  # Define your base URL here
    uvicorn.run("main:app", port=42069, log_level="debug")
    print(f"Running Web Server on: {base_url}")
