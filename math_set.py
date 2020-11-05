class Set:
    def is_member(self, element):
        pass

    def intersection(self, other):
        return Intersection(self, other)

    def union(self, other):
        return Union(self, other)

    def difference(self, other):
        return Difference(self, other)

    def compelment(self):
        return Complement(self)

    def compare(self, other):
        """
        return -2 if neither is subset of the other
        return -1 if self is supset of other
        return 0 if a is equal to other
        return 1 if other is subset of self
        return 2 if it is undeterminable
        """
        return 2


class Intersection(Set):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def is_member(self, element):
        return self.a.is_member(element) and self.b.is_member(element)


class Union(Set):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def is_member(self, element):
        return self.a.is_member(element) or self.b.is_member(element)


class Difference(Set):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def is_member(self, element):
        return self.a.is_member(element) and not self.b.is_member(element)


class Complement(Set):
    def __init__(self, a):
        self.a = a

    def is_member(self, element):
        return not self.a.is_member(element)


class UniversalSet(Set):
    def is_member(self, element):
        return True

    def intersection(self, other):
        return other

    def union(self, other):
        return UniversalSet()

    def difference(self, other):
        return other.complement

    def complement(self):
        return EmptySet()


class EmptySet(Set):
    def is_member(self, element):
        return False

    def intersection(self, other):
        return EmptySet

    def union(self, other):
        return other

    def difference(self, other):
        return EmptySet

    def complement(self):
        return UniversalSet()


class RangeSet(Set):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def is_member(self, element):
        return self.lower <= element <= self.upper

    def union(self, other):
        if other is RangeSet and self.upper <= other.lower and self.lower >= self.upper:
            return RangeSet(min(self.lower, other.lower), max(self.upper, other.upper))
        return Set.union(other)
