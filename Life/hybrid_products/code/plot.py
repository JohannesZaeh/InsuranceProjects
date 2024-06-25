# Johannes Zaeh, 26.05.2024
import matplotlib.pyplot as plt


'''
Function to plot an account development
'''


def plot_account(Account, plot_path):
    t = Account["t"]
    y1 = Account["traditional_part"]
    y2 = Account["fund_part"]
    y3 = Account["total"]

    plt.plot(t, y1, color='cornflowerblue')
    plt.plot(t, y3, color='limegreen')
    plt.fill_between(t, y1, y3, color='limegreen', label='Fund')
    plt.fill_between(t, y1, 0, color='cornflowerblue', label='Traditional')

    # Adding labels and legend
    plt.xlabel('t')
    plt.legend()
    plt.title('Account Evolution')

    plt.savefig(plot_path)
    plt.clf()

