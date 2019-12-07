class Intcode:
    ADD_OPERATOR = 1
    END_OPERATOR = 99
    INPUT_OPERATOR = 3
    OUTPUT_OPERATOR = 4
    MULTIPLY_OPERATOR = 2

    def __init__(self):
        pass

    def program(self, state):
        result_state = list(state)
        self.perform_instructions(result_state, 0)
        return result_state

    def perform_instructions(self,state, index):
        instruction = state[index]
        while instruction != Intcode.END_OPERATOR:
            index = self.perform_instruction(instruction, state, index)
            instruction = state[index]
        return state

    def perform_instruction(self, instruction, state, index):
        return self.build_instruction(instruction).operate(state, index)

    def build_instruction(self, instruction):
        i = int(str(instruction)[-1])
        if i == Intcode.ADD_OPERATOR:
            return AddInstruction()
        elif i == Intcode.INPUT_OPERATOR:
            return InputInstruction()
        elif i == Intcode.OUTPUT_OPERATOR:
            return OutputInstruction()
        elif i == Intcode.MULTIPLY_OPERATOR:
            return MultiplyInstruction()
class Parameter:
    def __init__(self, value, mode="position"):
        self.value = value
        self.mode = mode

class Instruction:
    def operate(self, program, index):
        return index

    def get_parameter_value(self, parameter, program):
        if parameter.mode == "position":
            return program[parameter.value]
        else:
            return parameter.value

    def get_parameters(self, program, index):
        instruction = str(program[index]).zfill(5)
        mode = "position"
        if instruction[2] == "1":
            mode = "immediate"
        first = Parameter(program[index + 1], mode)
        mode = "position"
        if instruction[1] == "1":
            mode = "immediate"
        second = Parameter(program[index + 2], mode)
        return first, second


class AddInstruction(Instruction):
    def operate(self, program, index):
        first,second = self.get_parameters(program, index)

        first_value = self.get_parameter_value(first, program)
        second_value = self.get_parameter_value(second, program)
        result = self.calculate(first_value, second_value)
        result_index = program[index+3]
        program[result_index] = result
        return index + 4

    def calculate(self, first, second):
        return first + second

class MultiplyInstruction(AddInstruction):
    def calculate(self, first, second):
        return first * second

class InputInstruction(Instruction):
    def operate(self, program, index):
        param = program[index+1]
        program[param] = 1 # hard coded as one
        return index + 2

class OutputInstruction(Instruction):
    def operate(self, program, index):
        param = self.get_parameters(program, index)
        print self.get_parameter_value(param[0], program)
        return index + 2

    def print_out(self, param, program, index):
        if param.mode == "immediate":
            print param


if __name__ == '__main__':
    f = open("input.txt")
    state = [ int(pos) for pos in f.readline().split(",")]
    f.close()
    intcode = Intcode()
    intcode.program(state)