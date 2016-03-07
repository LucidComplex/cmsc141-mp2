import os
import sys


def main():
    try:
        with open(sys.argv[1]) as in_file:
            input_lines = [line.strip() for line in in_file]
        f = open(sys.argv[1].replace('.in', '.out'), 'w')
    except IndexError:
        print 'No filename supplied.'
        return
    except IOError:
        print 'File does not exist.'
        return
    except OSError:
        print 'Can\'t write file.'
        return
    k = 0
    for line in input_lines:
        state = 'CRLM_'
        for move in line:
            if move in valid_moves(state):
                state = cross(state, move)
                if state.split('_')[0] == '':
                    print 'OK'
                    f.write('OK')
                    f.write(os.linesep)
                continue
            else:
                print 'NG'
                f.write('NG')
                f.write(os.linesep)
                break
    f.close()


def cross(state, move):
    banks = state.split('_')
    for i, bank in enumerate(banks):
        if 'M' in bank:
            j = (i + 1) % 2
            banks[i] = bank.replace('M', '')
            banks[j] = banks[j] + 'M'
            if move != 'N':
                banks[i] = banks[i].replace(move, '')
                banks[j] = banks[j] + move
            return '_'.join(banks)


def valid_moves(state):
    banks = state.split('_')
    for bank in banks:
        if 'M' in bank: # look for the bank where bb. Comsci is
            possible_moves = tuple(move for move in bank.replace('M', 'N'))
            invalid_states = ('RC', 'CR', 'LRC', 'LCR', 'LR',
                       'RL', 'RLC', 'RCL', 'CLR', 'CRL')
            return filter(lambda x: f(x, banks, invalid_states), possible_moves)

def f(move, banks, invalid_states):
    for i, bank in enumerate(banks):
        if 'M' in bank:
            j = (i + 1) % 2
            banks[i] = bank.replace('M', '')
            banks[j] = banks[j] + 'M'
            if move != 'N':
                banks[i] = banks[i].replace(move, '')
                banks[j] = banks[j] + move
            for state in invalid_states:
                if state in banks:
                    return False
            return True

if __name__ == '__main__':
    main()
