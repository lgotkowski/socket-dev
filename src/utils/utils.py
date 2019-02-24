import pkg_resources
import json
import io
from PIL import Image


def get_from_config(key):
    file_path = pkg_resources.resource_filename("utils", "config/settings.json")

    with open(file_path, "r") as in_file:
        settings = json.load(in_file)

    return settings.get(key)


def save_as_jpg(tree):
    from nltk.draw.tree import tree_to_treesegment
    from nltk.draw.util import CanvasFrame
    from nltk.internals import find_binary


    _canvas_frame = CanvasFrame()
    widget = tree_to_treesegment(_canvas_frame.canvas(), tree)

    _canvas_frame.add_widget(widget)
    x, y, w, h = widget.bbox()
    # print_to_file uses scrollregion to set the width and height of the pdf.
    #_canvas_frame.canvas()['scrollregion'] = (0, 0, w, h)
    _canvas_frame._canvas.config(width=2000, height=2000)



    (x0, y0, w, h) = _canvas_frame.scrollregion()
    #ps = _canvas_frame._canvas.postscript(colormode='color')
    ps = _canvas_frame._canvas.postscript(
        x=x0,
        y=y0,
        width=w + 2,
        height=h + 2,
        pagewidth=w + 2,  # points = 1/72 inch
        pageheight=h + 2,  # points = 1/72 inch
        pagex=0,
        pagey=0,
    )
    # workaround for bug in Tk font handling
    #ps = ps.replace(' 0 scalefont ', ' 9 scalefont ')

    #ps = _canvas_frame._canvas.postscript(colormode='color')

    #hen = filedialog.asksaveasfilename(defaultextension='.jpg')

    im = Image.open(io.BytesIO(ps.encode('utf-8')))
    im = im.resize((w *3, h*3), Image.ANTIALIAS)
    im.save("test" + '.png', quality=100)