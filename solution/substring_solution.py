# -*- coding: utf-8 -*-
from Pyro4 import expose
import time

MASK64 = (1 << 64) - 1
ALPHABET = "abcd"


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        (length, pattern, mode) = self.read_input()
        positions = length - len(pattern) + 1

        start = time.time()
        if mode == "seq":
            workers_used = 1
            count = Solver.count_in_range(pattern, 0, positions)
        else:
            workers_used = len(self.workers)
            print("Workers %d" % workers_used)
            mapped = []
            for i in xrange(0, workers_used):
                frm = positions * i // workers_used
                to = positions * (i + 1) // workers_used
                mapped.append(self.workers[i].mymap(pattern, frm, to))
            count = self.myreduce(mapped)
        elapsed = time.time() - start

        self.write_output(count, elapsed, workers_used, mode)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(pattern, frm, to):
        return Solver.count_in_range(pattern, frm, to)

    @staticmethod
    @expose
    def myreduce(mapped):
        total = 0
        for part in mapped:
            total += part.value
        return total

    @staticmethod
    def char_at(index):
        # Детермінований текст: однаковий на всіх вузлах, тож по мережі передаються лише межі
        x = (index * 0x9E3779B97F4A7C15) & MASK64
        x ^= x >> 31
        x = (x * 0xBF58476D1CE4E5B9) & MASK64
        x ^= x >> 29
        return ALPHABET[x % len(ALPHABET)]

    @staticmethod
    def prefix_function(pattern):
        pi = [0] * len(pattern)
        k = 0
        for i in xrange(1, len(pattern)):
            while k > 0 and pattern[k] != pattern[i]:
                k = pi[k - 1]
            if pattern[k] == pattern[i]:
                k += 1
            pi[i] = k
        return pi

    @staticmethod
    def count_in_range(pattern, frm, to):
        # Кількість входжень pattern, що починаються в позиціях [frm, to), алгоритм КМП
        m = len(pattern)
        pi = Solver.prefix_function(pattern)
        count = 0
        k = 0
        for i in xrange(frm, to + m - 1):
            c = Solver.char_at(i)
            while k > 0 and pattern[k] != c:
                k = pi[k - 1]
            if pattern[k] == c:
                k += 1
            if k == m:
                count += 1
                k = pi[k - 1]
        return count

    def read_input(self):
        f = open(self.input_file_name, 'r')
        length = int(f.readline())
        pattern = f.readline().strip()
        mode = f.readline().strip() or "par"
        f.close()
        return length, pattern, mode

    def write_output(self, count, elapsed, workers, mode):
        f = open(self.output_file_name, 'w')
        f.write("mode=%s workers=%d count=%d time=%.3f\n" % (mode, workers, count, elapsed))
        f.close()
        print("output done")
