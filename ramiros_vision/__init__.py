import ctypes
import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
lib_name = "Ramiros.dll" if os.name == "nt"else "Ramiros.so"
lib_path = os.path.join(BASE_DIR,lib_name)
#INITIALISATION VARIABLE AND COMPONENT
try:
    _lib = ctypes.CDLL(lib_path)
    _lib.ramirosOtsu.argtypes =[
        ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_ubyte)
    ]
    _lib.ramirosOtsu.restype = ctypes.c_int

    _lib.ramirosChain.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_ubyte)
    ]
    _lib.ramirosChain.restype = ctypes.c_int

except OSError:
    raise OSError(f"File C Binary ({lib_name}) Not found at the moduls! warm greating from ramiro's :)")

#EKSEKUSI PROGRAM 
def otsuRams(img_grayscale):
    img_gray = np.ascontiguousarray(img_grayscale, dtype= np.uint8)
    total_pixels = img_gray.size

    img_binary_out = np.zeros_like(img_gray)
    data_ptr= img_gray.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    out_ptr = img_binary_out.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

    threshold_value = _lib.ramirosOtsu(data_ptr, total_pixels, out_ptr)
    return threshold_value, img_binary_out

def chain_code(img_binary):
    img_bin = np.ascontiguousarray(img_binary, dtype= np.uint8)
    height,width = img_bin.shape
    output_buffer = np.zeros(width*height, dtype=np.uint8)
    data_ptr = img_bin.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    out_ptr = output_buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    length =_lib.ramirosChain(data_ptr,width,height,out_ptr)
    if length ==0:
        return[]
    return output_buffer[:length].tolist()
