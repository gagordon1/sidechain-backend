from PIL import Image, ImageFont, ImageDraw 
import io

def image_to_byte_array(image: Image) -> bytes:
  # BytesIO is a fake file stored in memory
  imgByteArr = io.BytesIO()
  # image.save expects a file as a argument, passing a bytes io ins
  image.save(imgByteArr, format=image.format)
  # Turn the BytesIO object back into a bytes object
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def generate_default_image(text):
    divider = len(text)//3
    text = text[:divider] + "\n" + text[divider:2* divider] +"\n" +text[2*divider:]
    image = Image.open('DefaultSidechainImage.png', 'r') 
    draw = ImageDraw.Draw(image) 
    font = ImageFont.truetype('arial.ttf', size=40)
    draw.multiline_text((256, 256), text, fill ="black", font = font, anchor="mm") 
    return image_to_byte_array(image)


if __name__ == "__main__":
    text = "0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82"
    print(len(text))
    generate_default_image(text)