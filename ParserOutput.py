class Entry:
    def __init__(self, index, info):
        self.index = index
        self.info = info
        self.parent = None
        self.right_sibling = None
        self.left_child = None


class ParserOutput:
    def __init__(self, grammar):
        self.current_index = 1
        self.root = Entry(self.current_index, "")
        self.grammar = grammar
        self.indexInput = 1

    def generateOutputTree(self, inputSequence):
        productionIndex = inputSequence[0]
        production = self.grammar.get_all_productions_separated()[productionIndex]
        self.root.info = production.left_hand_side
        self.current_index += 1
        self.root.left_child = self.generateNode(self.root, production.right_hand_side, inputSequence)

    def generateNode(self, parent, content, inputSequence):
        if len(content) == 0 or self.indexInput >= len(inputSequence) + 1:
            return None
        currentSymbol = content[0]
        if currentSymbol in self.grammar.terminals:
            node = Entry(self.current_index, currentSymbol)
            self.current_index += 1
            node.parent = parent
            content = content[1:]
            node.right_sibling = self.generateNode(parent, content, inputSequence)
            return node
        elif currentSymbol in self.grammar.non_terminals:
            productionIndex = inputSequence[self.indexInput]
            production = self.grammar.get_all_productions_separated()[productionIndex]
            node = Entry(self.current_index, currentSymbol)
            self.current_index += 1
            node.parent = parent
            self.indexInput += 1
            node.left_child = self.generateNode(node, production.right_hand_side, inputSequence)
            content = content[1:]
            node.right_sibling = self.generateNode(parent, content, inputSequence)
            return node
        else:
            return None

    def TreeToList(self, node, depth=0, result=None):
        if result is None:
            result = []

        if node:
            if len(result) <= depth:
                result.append([])
            result[depth].append({'index': node.index, 'info': node.info,
                                  'parent': node.parent.info if node.parent is not None else None,
                                  'right_sibling': node.right_sibling.info if node.right_sibling is not None else None})
            self.TreeToList(node.left_child, depth + 1, result)
            self.TreeToList(node.right_sibling, depth, result)

        return result

    def PrintToFile(self, filePath):
        file = open(filePath, 'w')
        for row in self.TreeToList(self.root):
            file.write(str(row) + '\n')
        file.close()
