import shortscale
import timeit

NUM = 740_991_777

store = []

def setup():
  store.clear()

def call():
  store.append(shortscale.shortscale(NUM))

def report(calls:int, time:float):
  print(f'{calls:10d} calls, {len(store[-1])*len(store):10d} bytes, {time * 1_000_000_000 / calls:>8.0f} ns/call')

t = timeit.Timer('call()', 'setup()', globals=globals())

def bench_shortscale():
    t.autorange(report)


if __name__ == '__main__':
    bench_shortscale()