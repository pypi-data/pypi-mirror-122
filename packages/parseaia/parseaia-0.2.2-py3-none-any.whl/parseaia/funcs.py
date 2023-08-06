import os

def listBlocks(block):
    gathered_blocks = [block]
    if "next" in block.__dict__:
        if "next" in block.__dict__:
            gathered_blocks += listBlocks(block.next)
    if "statements" in block.__dict__:
        for state in block.statements:
            if "next" in state.__dict__:
                gathered_blocks += listBlocks(state.next)
    if "values" in block.__dict__:
        for val in block.values:
            gathered_blocks += listBlocks(val)
    return gathered_blocks

def deletedir(fp):
    for file in os.listdir(fp):
        if os.path.isdir(f"{fp}/{file}"):
            deletedir(f"{fp}/{file}")
        else:
            os.remove(f"{fp}/{file}")
    os.rmdir(fp)