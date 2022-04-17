import sys
from time import sleep as s

class progressBar():
    BAR_LENGTH = 20
    previousFinalString = ""
    def display(self, currentValue, targetValue):
        barStart = "["
        barEnd = "]"
        completeBars = int(round((self.BAR_LENGTH - len(barStart) - len(barEnd)) * (currentValue / targetValue))) * "#"
        emptyBars = int(round((self.BAR_LENGTH - len(barStart) - len(barEnd)) * (1 - (currentValue / targetValue)))) * " "
        spacer = " "
        fraction = str(currentValue) + "/" + str(targetValue)
        finalString = barStart + completeBars + emptyBars + barEnd + spacer + fraction
        self.previousFinalString = finalString
        sys.stdout.write(finalString + "\r")

    def finish(self):
        sys.stdout.write(self.previousFinalString + "\n")


# def main():
#     progObject = progressBar()
#     for i in range(1, 1001):
#         progObject.display(i, 1000)
#         s(0.01)

# # def display(currentValue, targetValue):
    
# #     LENGTH = 40
# #     filledBars = int(round(LENGTH * (currentValue / targetValue))) * "#"
# #     emptyBars = int(round(LENGTH * (1 - (currentValue / targetValue)))) * " "
# #     totalString = "[" + filledBars + emptyBars + "]"
# #     sys.stdout.write(totalString + "\r")

# # def main():
# #     for i in range(0, 11):
# #         display(i, 10)
# #         s(0.1)
# #     print("\nDone!")



# if __name__ == '__main__':
#     main()