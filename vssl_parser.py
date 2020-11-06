from typing import Dict

from math_set import Set, RangeSet, Union, Intersection, Difference, Complement, UniversalSet, EmptySet


class State:
    def __init__(self, state: Dict[str, Set]):
        self.state = state

    def add_variable(self, name, value):
        self.state[name] = value

    def compare_to(self, other):
        for k, v in self.state.items():
            cmp = v.compare(other[k])
            if cmp == -2:
                return -2
            elif cmp == 1:
                return -2
            elif cmp == 2:
                return 2
        else:
            return -1

    def minimum(self, other):
        min_state = {}
        for k, v in self.state.items():
            min_state[k] = v.intersection(other[k])
        return min_state

    def maximum(self, other):
        max_state = {}
        for k, v in other.items():
            max_state[k] = v.union(self.state[k])
        return max_state


if __name__ == '__main__':
    state1 = {'a': RangeSet(1, 1), 'b': RangeSet(1, 3), 'c': RangeSet(3, 3)}
    state2 = {'a': RangeSet(1, 3), 'b': RangeSet(1, 3), 'c': RangeSet(1, 3), 'd': RangeSet(3, 3)}

    pre_state = State(state1)
    post_state = State(state2)

    res1 = pre_state.compare_to(post_state.state)
    res2 = post_state.compare_to(pre_state.state)

    print(f'res1 {res1}')
    print(f'res2 {res2}')
