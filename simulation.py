import logging
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt

from simulation.forest_map import ForestMap

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    map = ForestMap.from_conf("simulation/configurations/test_conf.json")

    for row in map.sectors:
        for column in row:
            print(column.sector_id)

    x_start = random.randint(0, map.width-1)
    y_start = random.randint(0, map.height-1)

    print(f"Starting position: {x_start}, {y_start}")
    sector = map.sectors[y_start][x_start]
    sector.burn_level = 1

    # main simulation
    for i in range(300):
        old_sectors = map.sectors
        for row in old_sectors:
            for current_sector in row:
                if current_sector.burn_level > 0 and current_sector.burn_level < 100 and current_sector.extinguish_level < 50:
                    additional_burn = random.uniform(0.1, 2)
                    map.sectors[current_sector.row][current_sector.column].burn_level += additional_burn

                elif current_sector.burn_level < 100 and current_sector.extinguish_level < 50:
                    neighbors = map.get_adjacent_sectors(current_sector, old_sectors)
                    neighbor_fire = False
                    for neighbor in neighbors:
                        if neighbor.burn_level > 20:
                            neighbor_fire = True
                            break

                    if neighbor_fire:
                        additional_burn = random.uniform(0.1, 2)
                        map.sectors[current_sector.row][current_sector.column].burn_level += additional_burn
        if i % 10 == 0:
            visualize_fire(map)



def visualize_fire(map: ForestMap):
    fire_sectors = np.zeros((map.height, map.width))
    print("TEST")

    for row in map.sectors:
        for column in row:
            fire_sectors[column.row][column.column] = column.burn_level


    # Plot the heatmap
    plt.imshow(fire_sectors, cmap='hot', interpolation='nearest')

    # Add colorbar
    cbar = plt.colorbar()
    cbar.set_label('Burn Level')

    # Show the plot
    plt.show()

    # # print(fire_sectors)
    # plt.imshow(fire_sectors, cmap='hot', interpolation='nearest')

    # Wyświetlenie heatmapy
    # plt.show()
    # visualize using heatmap
    # normalized_array = cv2.normalize(fire_sectors, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    #
    # Display the heatmap
    # cv2.imshow('Heatmap', normalized_array)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    main()