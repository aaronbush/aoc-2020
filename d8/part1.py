import sys
from typing import Iterable, List, Callable
from dataclasses import dataclass


@dataclass
class Instruction:
    op_code: str
    argument: int
    has_run: bool = False


@dataclass
class Registers:
    acc1: int = 0


def parse_instructions(filename: str) -> Iterable[Instruction]:
    with open(filename) as f:
        for l in f:
            yield(Instruction(l[:3], int(l[4:])))


def acc_op(registers: Registers, instruction: Instruction) -> int:
    registers.acc1 += instruction.argument
    instruction.has_run = True
    return 1


def jmp_op(registers: Registers, instruction: Instruction) -> int:
    instruction.has_run = True
    return instruction.argument


def no_op(registers: Registers, instruction: Instruction) -> int:
    instruction.has_run = True
    return 1

# TODO: look into typing-extensions/Protocol/__call__ PEP 544?


def run_until(instructions: List[Instruction], registers: Registers, condition: Callable[[Instruction], bool]) -> Instruction:
    i_ptr = 0
    # prev_instr = None
    while True:
        inst = instructions[i_ptr]
        if condition(inst):
            # print(f'stopping at: {inst} prev: {prev_instr}')
            break
        i_ptr += op_code_handlers[inst.op_code](registers, inst)
        # print(f'Ran: {inst}, Advance to: {i_ptr}, Registers: {registers}')
        prev_instr = inst


op_code_handlers = {'nop': no_op,    'acc': acc_op,    'jmp': jmp_op, }


def main(filename: str):
    instructions = list(parse_instructions(filename))
    registers = Registers()
    run_until(instructions, registers, lambda instr: instr.has_run == True)
    print(f'Registers: {registers}')


if __name__ == "__main__":
    main(sys.argv[1])
