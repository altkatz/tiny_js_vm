import sys

# name, arguments, stack effect
BYTECODES = [
    ("LOAD_CONST", 1, +1),
    ("STORE_NAME", 1, 0),
    ("DISCARD_TOP", 0, -1),
    ("RETURN_NULL", 0, 0),
]

BYTECODE_NAMES = []
BYTECODE_NUM_ARGS = []
BYTECODE_STACK_EFFECT = []
module = sys.modules[__name__]
for i, (bc_name, num_args, stack_effect) in enumerate(BYTECODES):
    setattr(module, bc_name, i)
    BYTECODE_NAMES.append(bc_name)
    BYTECODE_NUM_ARGS.append(num_args)
    BYTECODE_STACK_EFFECT.append(stack_effect)
del i, bc_name, num_args, stack_effect, module