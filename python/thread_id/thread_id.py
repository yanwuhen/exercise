# encoding: utf-8
import ctypes
for id in [186, 224, 178]:
	tid = ctypes.CDLL('libc.so.6').syscall(id)  #syscall系统调用

