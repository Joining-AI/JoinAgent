import json

class Node:
    def __init__(self, name, node_type, level, state=None, path=None):
        self.name = name
        self.type = node_type
        self.level = level
        self.state = state
        self.children = []
        self.path = path

class Retriever:
    def __init__(self, llm, parser, tree_path='mathlib_tree.json'):
        self.llm = llm
        self.parser = parser
        self.tree_path = tree_path
        with open(self.tree_path, 'r', encoding='utf-8') as f:
            self.target_tree = json.load(f)

    def find_node(self, node, name, level):
        if node['name'] == name and node['level'] == level:
            return node
        for child in node.get('children', []):
            result = self.find_node(child, name, level)
            if result:
                return result
        return None

    def get_children_names(self, node):
        return [child['name'] for child in node.get('children', [])]

    def create_search_tree(self):
        return Node(self.target_tree['name'], self.target_tree['type'], self.target_tree['level'], path="")

    def search_and_update(self, search_node, target_node, theorem, current_level=0):
        if search_node.state is not None:
            return

        children_names = self.get_children_names(target_node)
        
        if not children_names:
            search_node.state = 'active' if search_node.type == 'lean' else 'dead'
            return

        question = f'请你告诉我这行lean4语句 {theorem} 的证明和下面的哪些Mathlib库部分最相关: {children_names}，以list格式返回'
        answer = self.llm.ask(question)
        answer_list = self.parser.parse_list(answer)

        if not answer_list:
            search_node.state = 'active' if search_node.type == 'lean' else 'dead'
            return

        for child_name in answer_list:
            child_target_node = self.find_node(self.target_tree, child_name, current_level + 1)
            if child_target_node:
                child_path = f"{search_node.path}/{child_name}" if search_node.path else child_name
                child_search_node = Node(child_name, child_target_node['type'], current_level + 1, path=child_path)
                search_node.children.append(child_search_node)
                self.search_and_update(child_search_node, child_target_node, theorem, current_level + 1)

    def get_active_nodes(self, node, active_nodes=None):
        if active_nodes is None:
            active_nodes = []
        
        if node.state == 'active':
            active_nodes.append(node)
        
        for child in node.children:
            self.get_active_nodes(child, active_nodes)
        
        return active_nodes

    def retrieve(self, lean_statement):
        search_tree = self.create_search_tree()
        self.search_and_update(search_tree, self.target_tree, lean_statement)
        active_nodes = self.get_active_nodes(search_tree)
        return active_nodes, search_tree