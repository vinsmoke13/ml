import numpy as np
import cv2 as cv

class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv.imshow(self.windowname, self.dests[0])
        cv.imshow(self.windowname+": Mask",self.dests[1])
    def on_mouse(self, event, x, y, flags, param):
        pt = (x,y)
        if event == cv.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv.EVENT_LBUTTONUP:
            self.prev_pt = None
        if self.prev_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv.line(dst,self.prev_pt, pt, color, 2)
            self.dirty = True
            self.prev_pt = pt
            self.show()

if __name__ == '__main__':

    print("f - Inpaint using FMM")
    print("n - Inpaint using NS technique")
    print("r - Reset the inpaint mask")
    print("ESC - EXIT")

    img = cv.imread("desert.jpg", cv.IMREAD_COLOR)

    if img is None:
        print('Failed to load image file: {}'.format(args["image"]))
        exit(0)

    img_mask = img.copy()
    inpaintMask = np.zeros(img.shape[:2], np.uint8)
    sketch = Sketcher('image', [img_mask, inpaintMask], lambda: ((255, 255, 255), 255))

    while True:
        ch = cv.waitKey(0)
        if ch == 27:
            break
        if ch == ord('f'):
            res = cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv.INPAINT_TELEA)
            cv.imshow("Inpaint output using FMM", res)
        if ch == ord('n'):
            res = cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv.INPAINT_NS)
            cv.imshow("Inpaint output using NS", res)
        if ch == ord('r'):
            img_mask[:] = img
            inpaintMask[:] = 0
            sketch.show()

    cv.destroyAllWindows()