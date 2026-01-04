def generator():
    print(">> GENERATOR: Starting")
    print(">> GENERATOR: Before first yield")
    yield "first"
    print(">> GENERATOR: Resumed after first yield")
    print(">> GENERATOR: Before second yield")
    yield "second"
    print(">> GENERATOR: Resumed after second yield")
    print(">> GENERATOR: Finishing")

print("=== Creating generator object ===")
gen = generator()  # Notice: Nothing prints yet!

print("\n=== Calling next(gen) for the first time ===")
value1 = next(gen)
print(f"<< MAIN: Got value: {value1}")

print("\n=== Calling next(gen) for the second time ===")
value2 = next(gen)
print(f"<< MAIN: Got value: {value2}")

print("\n=== Calling next(gen) for the third time ===")
try:
    value3 = next(gen)
    print(f"<< MAIN: Got value: {value3}")
except StopIteration:
    print("<< MAIN: Generator exhausted (StopIteration)")