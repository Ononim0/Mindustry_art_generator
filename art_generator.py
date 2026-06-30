import zlib
from PIL import Image, ImageChops

img = "oct.png"
name = "generated"
fill = False


def autocrop_image(image):
    bg_color = image.getpixel((0, 0))
    bg_image = Image.new(image.mode, image.size, bg_color)
    diff = ImageChops.difference(image, bg_image)
    
    bbox = diff.getbbox()
    
    if bbox:

        return image.crop(bbox)
    else:

        return image
    
def process_image(image_path, fill):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    img = autocrop_image(img)
    pixels = img.load()
    width, height = img.size
    img_list = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            hex_color = [r, g, b, a]
            if hex_color == [0, 0, 0, 0] and fill == False:
                continue
            img_list.append([x, y, hex_color])

    return img_list, width, height

def illuminator_configurator (img_list):
    data = []
    for i in img_list:
        q = 0
        data.append(q.to_bytes(1, "big"))
        data.append(i[0].to_bytes(2, "big"))
        data.append(i[1].to_bytes(2, "big"))
        q = 1
        data.append(q.to_bytes(1, "big"))
        for q in i[2]:
            data.append(q.to_bytes(1, "big"))
        q = 0
        data.append(q.to_bytes(1, "big"))
    return(data)

def outspect_msch(img, name, fill):
    data = []
    img_list, width, height = process_image(img, fill)
    
    data.append(width.to_bytes(2, "big"))
    data.append(height.to_bytes(2, "big"))

    q = 4
    data.append(q.to_bytes(1, "big"))

    data.append(q.to_bytes(2, "big"))
    data.append("name".encode())

    data.append(len(name).to_bytes(2, "big"))
    data.append(name.encode())

    q = 10
    data.append(q.to_bytes(2, "big"))
    data.append("contentMap".encode())

    q = 2
    data.append(q.to_bytes(2, "big"))   
    data.append("{}".encode())

    q = 11
    data.append(q.to_bytes(2, "big"))
    data.append("description".encode())

    q = 0
    data.append(q.to_bytes(2, "big"))

    q = 6
    data.append(q.to_bytes(2, "big"))
    data.append("labels".encode())

    q = 2
    data.append(q.to_bytes(2, "big"))
    data.append("[]".encode())

    q = 1
    data.append(q.to_bytes(1, "big"))

    q = 11
    data.append(q.to_bytes(2, "big"))
    data.append("illuminator".encode())

    q = len(img_list)
    data.append(q.to_bytes(4, "big"))

    data = b"".join(data + illuminator_configurator(img_list))
    z_data = zlib.compress(data)

    with open(f"shematick/{name}.msch", "wb") as f:
        f.write("msch".encode('utf-8'))
        f.write(bytes([1]))
        f.write(z_data)



if __name__ == "__main__":
    outspect_msch(img, name, fill)