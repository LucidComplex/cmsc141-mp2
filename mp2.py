import os
import sys


def main():
    try:
        file_name = sys.argv[1]
        with open(file_name) as f:
            move_list = [line.strip() for line in f]
    except IOError:
        print '\'{name}\' does not exist.'.format(name=file_name)
        return
    except IndexError:
        print 'No file name supplied.'
        return

    f = open(file_name.replace('.in', '.out'), 'w')

    for move_line in move_list:
        base = Node('CRML_')
        good = True
        for move in move_line:
            if move in base.valid_moves():
                base = base.peek(move)
            else:
                good = False
                break
        if base.is_end() and good:
            print 'OK'
            f.write('OK')
            f.write(os.linesep)
        else:
            print 'NG'
            f.write('NG')
            f.write(os.linesep)
    f.close()

"""
def create_tree():
    root = Node('LCRM_')
    frontier = []
    visited = []
    state = root.state
    for move in root.valid_moves():
        try:
            frontier.append(root.peek(move))
            visited.append(root)
            root.children.append(root.peek(move))
        except Exception:
            pass
    while len(frontier) > 0:
        node = frontier.pop(0)
        if node.is_end():
            continue
        for move in node.valid_moves():
            try:
                exists = False
                for visited_node in visited:
                    if node.equals(visited_node):
                        visited_node.children.append(node)
                        exists = True
                        break
                if not exists:
                    child = node.peek(move)
                    node.children.append(child)
                    frontier.append(child)
                    visited.append(node)
                    break
            except Exception:
                pass
    return root
"""


def validate(x, bank):
    remain = bank.replace(x, '').replace('M', '')
    if remain in ('RL', 'LR', 'CR', 'RC', 'LRC', 'LCR', 'RLC', 'RCL', 'CRL', 'CLR'):
        return False
    return True


class Node():
    state = None
    children = None

    def __init__(self, state):
        self.state = state
        self.children = []

    def valid_moves(self):
        banks = self.state.split('_')
        for bank in banks: # look for the bank with M
            if 'M' in bank:
                valid = [a for a in bank.replace('M', 'N')]
                valid = filter(lambda x: validate(x, bank), valid)
                return valid


    def peek(self, move):
        """
        Returns a node with the states changed
        """
        if move not in self.valid_moves():
            raise Exception
        state = self.state
        banks = state.split('_')
        for i in range(len(banks)):
            if 'M' in banks[i]:
                j = (i + 1) % 2
                banks[i] = banks[i].replace('M', '')
                banks[j] = banks[j] + 'M'
                break
        if move == 'N':
            return Node('_'.join(banks))
        for i in range(len(banks)):
            if move in banks[i]:
                j = (i + 1) % 2
                banks[i] = banks[i].replace(move, '')
                banks[j] = banks[j] + move
                break
        return Node('_'.join(banks))

    def is_end(self):
        state = self.state
        banks = state.split('_')
        if banks[0] == '':
            return True
        return False

    def equals(self, node):
        this_state = self.state
        node_state = node.state

        this_bank = this_state.split('_')
        node_bank = node_state.split('_')

        for x, y in zip(this_bank, node_bank):
            for letterx in x:
                if letterx not in y:
                    return False
            for lettery in y:
                if lettery not in x:
                    return False

        return True


if __name__ == '__main__':
    main()
