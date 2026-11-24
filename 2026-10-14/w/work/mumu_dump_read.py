import pathlib
import struct
import sys


def inspect(path):
    data = path.read_bytes()
    unpack = lambda fmt, at: struct.unpack_from('<' + fmt, data, at)
    signature, _, count, directory = unpack('4I', 0)
    assert signature == 0x504d444d
    streams = {kind: (size, rva) for kind, size, rva in
               (unpack('3I', directory + i * 12) for i in range(count))}
    modules = []
    mod = streams[4][1]
    for i in range(unpack('I', mod)[0]):
        base, size, _, stamp, name = unpack('Q4I', mod + 4 + 108 * i)
        length, = unpack('I', name)
        full = data[name + 4:name + 4 + length].decode('utf-16le')
        modules.append((base, base + size, full, stamp))

    def resolve(addr):
        for start, end, name, _ in modules:
            if start <= addr < end:
                return f'{pathlib.PureWindowsPath(name).name}+0x{addr-start:x}'
        return ''

    e = streams[6][1]
    tid, _, code, flags, parent, address, params, _ = unpack('4I2Q2I', e)
    ctx_size, ctx = unpack('2I', e + 160)
    arch, = unpack('H', streams[7][1])
    print(f'\n{path.name} TID={tid} code={code:#010x} flags={flags} addr={address:#018x} {resolve(address)} arch={arch}')
    print('exception params:', [hex(x) for x in unpack(f'{params}Q', e + 40)])
    if arch == 9 and ctx_size >= 256:
        names = 'rax rcx rdx rbx rsp rbp rsi rdi r8 r9 r10 r11 r12 r13 r14 r15 rip'.split()
        regs = dict(zip(names, unpack('17Q', ctx + 120)))
        print('context:', ' '.join(f'{key}={value:#x}' for key, value in regs.items()))
        t = streams[3][1]
        for i in range(unpack('I', t)[0]):
            ident, _, _, _, _, start, size, rva = unpack('4I2Q2I', t + 4 + i * 48)
            if ident != tid:
                continue
            rsp = regs['rsp']
            for stack_at in range(max(start, rsp), min(start + size, rsp + 0x440) - 7, 8):
                value, = unpack('Q', rva + stack_at - start)
                match = resolve(value)
                if match:
                    print(f'sp+{stack_at-rsp:03x} {value:016x} {match}')
    print('relevant loaded modules:')
    for start, end, name, stamp in modules:
        if any(key in pathlib.PureWindowsPath(name).name.lower() for key in
               ('mumu', 'qt5', 'vitrit', 'virtrit', 'nvwgf', 'd3d', 'dxgi', 'gallium', 'vcruntime')):
            print(f'{start:016x}-{end:016x} stamp={stamp:08x} {name}')


for arg in sys.argv[1:]:
    inspect(pathlib.Path(arg))
