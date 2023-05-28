import matplotlib.pyplot as plt

class PulseDetector:

    def __init__(self, data):
        self.data = data

    def calculate_average(self):
        total = sum(self.data)
        count = len(self.data)
        average = total / count
        return average

    def show(self):
        print(self.calculate_average())
        x = range(len(self.data))  # X-axis values (indices of the list)
        y = self.data              # Y-axis values (the list of values)

        # Create a line graph
        plt.plot(x, y)

        # Set labels and title
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Graph of Values')

        # Display the graph
        plt.show(block=True)