class State:
    def __init__(self):
        self.state = {}

    def add(self, key, val):
        self.state[key] = val

    def compare(self, other):
        for key in other.state:
            if key not in self.state:
                return -2
            self_set = self.state[key]
            other_set = other.state[key]
            for i in other_set:
                if i not in self_set:
                    return -2
        return 1


class Node:
    def __init__(self, section, state):
        self.section = section
        self.state = state
        self.left = None
        self.right = None


class AST:
    def __init__(self, source):
        self.source = source
        self.state = None
        self.root = None

    def compile(self):
        self.state = State()
        latest_node = None
        line_split = self.source.split(' ')
        for i in range(len(line_split)):
            current_word = line_split[i]
            if current_word == 'def':
                self.root = Node(current_word, self.state)
                i += 1
                def_name = line_split[i]
                i += 1
                def_type = line_split[i]
                def_name_node = Node(def_name, self.state)
                def_type_node = Node(def_type, self.state)
                self.root.left = def_name_node
                def_name_node.left = def_type_node

                i += 1
                if line_split[i] == '{':
                    n = Node(line_split[i], self.state)
                    latest_node = n
                    self.root.rigth = n
                else:
                    return False
            if current_word == 'let':
                let_node = Node(current_word, self.state)
                i += 1
                let_name = line_split[i]
                i += 1
                eq = line_split[i]
                if eq != '=':
                    return False
                i += 1
                let_val = line_split[i]
                name_node = Node(let_name, self.state)
                val_node = Node(let_val, self.state)
                if line_split[i + 1] == '+':
                    i += 1
                    plus = line_split[i]
                    i += 1
                    next_val = line_split[i]
                    plus_node = Node(plus, self.state)
                    next_node = Node(next_val, self.state)
                    val_node.left = plus_node
                    plus_node.left = next_node

                latest_node.left = let_node
                let_node.left = name_node
                name_node.left = val_node
                latest_node = val_node

        return True

    def run(self):
        self.handle_node(self.root)

    def handle_node(self, node):
        if node is None:
            return
        if node.section == 'let':
            if node.left.left.left is not None and node.left.left.left.section == '+':
                let_name = node.left.section
                a = node.left.left.section
                b = node.left.left.left.left.section
                a_val = self.state.get_val(a)
                b_val = self.state.get_val(b)
                self.state.add(let_name, {a_val, b_val})
            else:
                let_name = node.left.section
                val = node.left.left.section
                self.state.add(let_name, {val})

        self.handle_node(node.left)
        self.handle_node(node.right)


if __name__ == '__main__':
    end_state = State()
    end_state.add('x', {200})
    end_state.add('y', {5})
    end_state.add('h', {205})
    source = "" + \
             "def test INTEGER { " + \
             "let x = 100 " + \
             "let x = 200 " + \
             "let y = 5 " + \
             "let h = y + x " + \
             "}"
    ast = AST(source)

    if ast.compile():
        ast.run()
        ast_state = ast.state

        print(ast_state.compare(end_state))
    else:
        print('Compile error')
