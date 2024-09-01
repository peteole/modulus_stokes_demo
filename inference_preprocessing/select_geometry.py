import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib import use

def create_polygon(domain_size=(10, 10)):
    """
    Allows the user to graphically create a polygon by clicking on a window.
    The polygon is dynamically updated as points are clicked.
    Once the polygon is closed (by clicking near the starting point), the window closes and returns the selected points.

    :param domain_size: A tuple specifying the size of the domain (width, height).
    :return: A list of tuples representing the (x, y) coordinates of the selected points.
    """
    use('TkAgg')  # Use the TkAgg backend to allow interactive plotting
    # List to store the points
    points = []

    # Create figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(0, domain_size[0])
    ax.set_ylim(0, domain_size[1])

    polygon = None

    # Function to be called when the canvas is clicked
    def onclick(event):
        nonlocal polygon

        if event.inaxes is not None:
            x, y = event.xdata, event.ydata

            if points and (abs(x - points[0][0]) < 0.1 and abs(y - points[0][1]) < 0.1):
                # Close the polygon if the click is near the first point
                #points.append(points[0])  # Closing the polygon
                plt.draw()
                plt.close()  # Close the figure window when the polygon is finished
            else:
                points.append((x, y))
                plt.plot(x, y, 'ro')  # Plot the point
                if polygon:
                    polygon.set_xy(points)
                else:
                    polygon = Polygon(points, closed=False, fill=None, edgecolor='r')
                    ax.add_patch(polygon)
                plt.draw()  # Update the plot

    # Connect the click event to the handler function
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # Show the plot and wait for clicks
    plt.show()

    # Disconnect the event handler after finishing
    fig.canvas.mpl_disconnect(cid)

    return points

# Example usage:
# polygon_points = create_polygon((10, 10))
# print("Selected points:", polygon_points)