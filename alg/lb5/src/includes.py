import sys
from collections import deque, defaultdict
from graphviz import Digraph

def visualize_trie(root, filename='trie'):
    """Визуализация префиксного дерева Ахо-Корасик"""
    dot = Digraph(comment='Trie')
    visited = set()
    
    def add_nodes(node):
        if node.id in visited:
            return
        visited.add(node.id)
        
        label = (
            f"ID: {node.id}\n"
            f"Output: {node.output if node.output else '∅'}\n"
            f"Fail: {node.fail.id if node.fail else '∅'}"
        )
        dot.node(str(node.id), label)
        
        for char, child in node.children.items():
            add_nodes(child)
            dot.edge(str(node.id), str(child.id), label=char)
            
        if node.fail and node.fail != node:
            dot.edge(str(node.id), str(node.fail.id), style='dashed', color='red')
    
    add_nodes(root)
    dot.render(filename, view=False, format='png', cleanup=True)
    print(f"Граф сохранен в {filename}.png")

def visualize_wildcard_automaton(root, filename='wildcard_automaton'):
    """Визуализация автомата для поиска с джокером"""
    dot = Digraph(comment='Wildcard Automaton')
    visited = set()
    
    def add_nodes(node):
        if node.id in visited:
            return
        visited.add(node.id)
        
        label = (
            f"ID: {node.id}\n"
            f"Positions: {node.positions if node.positions else '∅'}\n"
            f"Fail: {node.fail.id if node.fail else '∅'}"
        )
        dot.node(str(node.id), label, shape='rectangle')
        
        for char, child in node.children.items():
            add_nodes(child)
            dot.edge(str(node.id), str(child.id), label=char)
            
        if node.fail and node.fail != node:
            dot.edge(str(node.id), str(node.fail.id), style='dashed', color='blue')
    
    add_nodes(root)
    dot.render(filename, view=False, format='png',cleanup=True)
    print(f"Граф сохранен в {filename}.png")

# Реализация классического алгоритма Ахо-Корасик для множественного поиска
class TrieNode:
    _id = 0
    __slots__ = ['children', 'fail', 'output', 'id']
    def __init__(self):
        self.children = dict()
        self.fail = None
        self.output = set()
        self.id = TrieNode._id
        TrieNode._id += 1

    def __repr__(self):
        return f"[Trie#{self.id} ch={list(self.children.keys())} out={self.output} fail={self.fail.id if self.fail else 'root'}]"

def build_trie(patterns, debug=False):
    TrieNode._id = 0  # Сбрасываем счетчик для повторных запусков
    root = TrieNode()
    for idx, pattern in enumerate(patterns, 1):
        if debug: print(f"\nДобавление шаблона {idx}: '{pattern}'")
        node = root
        for char in pattern:
            if char not in node.children:
                node.children[char] = TrieNode()
                if debug: print(f"  Создан узел {node.children[char]}")
            node = node.children[char]
        node.output.add(idx)
        if debug: print(f"  Конец шаблона -> узел {node}")
    return root

def build_failure_links(root, debug=False):
    queue = deque()
    root.fail = root
    for child in root.children.values():
        child.fail = root
        queue.append(child)

    while queue:
        current = queue.popleft()
        if debug: print(f"\nОбработка узла {current}")

        for char, child in current.children.items():
            fail_node = current.fail
            while fail_node != root and char not in fail_node.children:
                fail_node = fail_node.fail

            child.fail = fail_node.children.get(char, root)
            child.output.update(child.fail.output)
            if debug: 
                fail_info = f"{child.fail.id}" if child.fail != root else "root"
                print(f"  Установка fail[{char}]: {child.id} → {fail_info}")
            
            queue.append(child)
    return root

def aho_corasick_search(text, patterns, debug=False):
    root = build_trie(patterns, debug)
    root = build_failure_links(root, debug)

    matches = []
    current = root
    for i, char in enumerate(text, 1):
        if debug:
            print(f"\nProcessing text char '{char}' at position {i}")
        while current != root and char not in current.children:
            if debug:
                print(f"  Following fail link from {current} to {current.fail}")
            current = current.fail
        if char in current.children:
            current = current.children[char]
            if debug:
                print(f"  Moved to node {current}")
        else:
            if debug:
                print("  No transition, stay at root")
        
        if current.output:
            if debug:
                print(f"  Output patterns: {current.output}")
            for pattern_id in current.output:
                start = i - len(patterns[pattern_id - 1]) + 1
                matches.append((start, pattern_id))
    
    print("input visual png name")
    filename = input()
    visualize_trie(root, filename)

    return sorted(matches)

# Реализация поиска с джокером
class WildcardNode:
    _id = 0
    __slots__ = ['children', 'positions', 'fail', 'id']
    def __init__(self):
        self.children = dict()
        self.positions = list()
        self.fail = None
        self.id = WildcardNode._id
        WildcardNode._id += 1

    def __repr__(self):
        return f"[Wild#{self.id} ch={list(self.children.keys())} pos={self.positions} fail={self.fail.id if self.fail else 'root'}]"

def build_wildcard_automaton(pattern, wildcard, debug=False):
    WildcardNode._id = 0  # Сбрасываем счетчик
    required = [(j, c) for j, c in enumerate(pattern) if c != wildcard]
    
    if debug:
        print("\nПостроение автомата для шаблона:")
        print(f"Шаблон: {pattern} (джокер: '{wildcard}')")
        print(f"Ключевые позиции: {required}")

    if not required:
        if debug: print("Нет ключевых символов!")
        return None

    root = WildcardNode()
    char_map = defaultdict(list)
    for j, c in required:
        char_map[c].append(j)

    for c, positions in char_map.items():
        if debug: print(f"\nДобавление символа '{c}' на позициях {positions}")
        node = root
        if c not in node.children:
            node.children[c] = WildcardNode()
            if debug: print(f"  Создан узел {node.children[c]}")
        node = node.children[c]
        node.positions.extend(positions)
        if debug: print(f"  Обновлен узел {node}")

    queue = deque()
    root.fail = root
    for child in root.children.values():
        child.fail = root
        queue.append(child)

    while queue:
        current = queue.popleft()
        if debug: print(f"\nОбработка узла {current}")

        for char, child in current.children.items():
            fail_node = current.fail
            while fail_node != root and char not in fail_node.children:
                fail_node = fail_node.fail

            child.fail = fail_node.children.get(char, root)
            if debug:
                fail_info = f"{child.fail.id}" if child.fail != root else "root"
                print(f"  Установка fail[{char}]: {child.id} → {fail_info}")
            
            queue.append(child)

    return root, len(pattern), required

def wildcard_search(text, pattern, wildcard, debug=False):
    automaton = build_wildcard_automaton(pattern, wildcard, debug)
    if not automaton: return []
    root, pat_len, required = automaton

    if debug:
        print("\nНачало поиска в тексте:")
        print(f"Текст: {text}")
        print(f"Длина шаблона: {pat_len}")
        print(f"Требуемые совпадения: {required}\n")

    current = root
    checked = set()
    result = set()

    for pos, char in enumerate(text):
        if debug: print(f"\nПозиция {pos}: символ '{char}'")

        # Переход по fail-ссылкам
        steps = 0
        while current != root and char not in current.children:
            if debug: 
                print(f"  Шаг {steps}: переход {current.id} → {current.fail.id}")
                steps += 1
            current = current.fail

        # Обработка текущего символа
        if char in current.children:
            current = current.children[char]
            if debug: print(f"  Переход в узел {current}")
        else:
            if debug: print("  Нет перехода, остаемся в root")
            current = root

        # Проверка всех возможных позиций
        temp = current
        depth = 0
        while temp != root:
            if temp.positions:
                if debug: print(f"  Глубина {depth}: узел {temp} содержит позиции {temp.positions}")
                
                for j in temp.positions:
                    start = pos - j
                    if debug: print(f"    Проверка позиции {start} (j={j})")

                    if start < 0 or start + pat_len > len(text):
                        if debug: print("      Выход за границы текста")
                        continue

                    if start in checked:
                        if debug: print("      Уже проверено")
                        continue

                    checked.add(start)
                    valid = all(text[start+jj] == cc for jj, cc in required)
                    
                    if debug:
                        substr = text[start:start+pat_len]
                        marks = "".join("ok" if text[start+jj] == cc else "false" 
                                      for jj, cc in required)
                        print(f"      Подстрока: {substr} Проверки: {marks}")

                    if valid: 
                        result.add(start + 1)
                        if debug: print("       Совпадение!")
            temp = temp.fail
            depth += 1

    print("input visual png name")
    filename = input()
    visualize_wildcard_automaton(root, filename)

    return sorted(result)