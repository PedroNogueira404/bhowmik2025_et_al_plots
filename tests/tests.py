import matplotlib.pyplot as plt

# Create a figure and axes
fig, ax = plt.subplots()

# Plot some data
ax.plot([1, 2, 3], [4, 5, 6], color='white') # Plot in white for contrast

# Set axis limits larger than the data range
ax.set_xlim(0, 5)
ax.set_ylim(3, 7)

# Set the background color of the figure and axes to black
# fig.set_facecolor('black')
ax.set_facecolor('black')

# You might want to change tick and label colors for visibility
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_xlabel('X-axis', color='white')
ax.set_ylabel('Y-axis', color='white')
ax.set_title('Plot with Black Background', color='white')

# Display the plot
plt.show()
