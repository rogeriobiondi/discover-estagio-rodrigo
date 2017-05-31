#Exercise from page 69 - Python Succinctly.pdf

distance = input("What distance are you going to travel? ")
distance = int(distance)


if distance < 3:
    print("\n I suggest you to go by walking!")
elif distance<300:
    print("I suggest you driving!")
else:
    print("I suggest you to buy air tickets!")