import logging
import random

import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

from simulation.forest_map import ForestMap
from simulation.fire_brigades.fire_brigade import FireBrigade
from simulation.fire_brigades.fire_brigade_state import FireBrigadeState
from simulation.fire_situation.fire_situation import FireSituation
from simulation.fire_situation.fire_situation_state import FireSituationState

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    map = ForestMap.from_conf("simulation/configurations/mapConfigMockup.json")
    fire_brigades = FireBrigade.from_conf("simulation/configurations/mapConfigMockup.json")

    # sectors_to_extinguish = list(FireSituation)
    fire_situations = 0
    num_fire_brigades_available = len(fire_brigades)

    for row in map.sectors:
        for column in row:
            # print(column.sector_id)
            print(column)

    x_start = random.randint(1, len(map.sectors)-1)
    y_start = random.randint(1, len(map.sectors[1])-1)

    print(f"Starting position: {x_start}, {y_start}")
    sector = map.sectors[x_start][y_start]
    sector.burn_level = 1

    # main simulation
    for i in range(300):
        old_sectors = map.sectors
        for row in old_sectors:
            for current_sector in row:
                if current_sector is None:
                    continue
                if current_sector.sector_type == 6:
                    continue

                # simulate fire extinguishing
                if current_sector.burn_level > 0:
                    extinguish = 0
                    for fire_brigade in fire_brigades:
                        # TODO: TUTAJ IF: jeśli fire_brigade jest w danym sektorze
                        if fire_brigade.state == FireBrigadeState.AVAILABLE or fire_brigade.state == FireBrigadeState.EXTINGUISHING:
                            extinguish = extinguish + random.uniform(0.001, 0.01)
                            break
                        fire_brigade.move()
                    map.sectors[current_sector.row][current_sector.column].extinguish_level += extinguish

                if current_sector.burn_level > 0 and current_sector.burn_level < 100 and current_sector.extinguish_level < current_sector.burn_level:
                    # additional_burn = random.uniform(0.001, 0.05)
                    additional_burn = random.uniform(1, 5)
                    map.sectors[current_sector.row][current_sector.column].burn_level += additional_burn
                    map.sectors[current_sector.row][current_sector.column].burn_level = min(100, map.sectors[
                        current_sector.row][current_sector.column].burn_level)

                elif current_sector.burn_level < 100 and current_sector.extinguish_level < 50:
                    neighbors = map.get_adjacent_sectors(current_sector, old_sectors)
                    neighbor_fire = False
                    for neighbor in neighbors:
                        if neighbor is None:
                            continue
                        if neighbor.burn_level > 20 and neighbor.burn_level > neighbor.extinguish_level:
                            neighbor_fire = True
                            break

                    if neighbor_fire:
                        additional_burn = random.uniform(0.1, 2)
                        map.sectors[current_sector.row][current_sector.column].burn_level += additional_burn
                        map.sectors[current_sector.row][current_sector.column].burn_level = min(100, map.sectors[
                            current_sector.row][current_sector.column].burn_level)
                        
                # if current_sector.burn_level > 20 and current_sector.sector_id not in sectors_to_extinguish:
                #     sectors_to_extinguish.append(FireSituation(
                #         fire_situations,
                #         FireSituationState.ACTIVE,
                #         None,
                #         current_sector.sector_id,
                #         current_sector.burn_level,
                #         0,
                #         timestamp=time.time()
                #         )
                #     )
                #     fire_situations += 1
                #     print(f"New fire situation: {current_sector.sector_id}, {current_sector.burn_level}")
                #

                print(f"Current sector: {current_sector.row}, {current_sector.column}, burn level: {current_sector.burn_level}")
        
        # if FireSituationState.ACTIVE in sectors_to_extinguish: #TODO: think about better condition
        #     # TODO: implement sending fire brigades
        #     for fire_situation in sectors_to_extinguish:
        #         if fire_situation.state == FireSituationState.ACTIVE:
        #             sector_situation = map.get_sector(fire_situation.sector_id)
        #             if num_fire_brigades_available != 0:
        #                 for fire_brigade in fire_brigades:
        #                     print(fire_brigade.fire_brigade_id, fire_brigade.state)
        #                     print(fire_brigade.state == FireBrigadeState.AVAILABLE)
        #                     if fire_brigade.state == FireBrigadeState.AVAILABLE:
        #                         # print(fire_brigade.destination)
        #                         fire_situation.fire_brigade_id = fire_brigade.fire_brigade_id
        #                         fire_situation.state = FireSituationState.BRIGADE_COMING
        #                         print(map.get_sector_location(sector_situation))
        #                         fire_brigade.move(map.get_sector_location(sector_situation))
        #                         print("Fire brigade is sent")
        #                         num_fire_brigades_available -= 1
        #                         break
        #             else:
        #                 print("No fire brigades available")
        #                 break

        # break
        if i % 10 == 0:
            visualize_fire(map)

        if i == 100:
            map.sectors[1][1].extinguish_level = 100



def visualize_fire(map: ForestMap):
    fire_sectors = np.zeros((map.height, map.width))
    print("TEST")

    for row in map.sectors:
        for column in row:
            if column is None:
                continue
            if column.burn_level > column.extinguish_level:
                fire_sectors[column.row][column.column] = column.burn_level
            else:
                fire_sectors[column.row][column.column] = -column.extinguish_level


    # Plot the heatmap
    plt.imshow(fire_sectors, cmap='bwr', interpolation='nearest', vmin=-100, vmax=100)


    plt.savefig('plot.png')

    plot = cv2.imread('plot.png')
    cv2.imshow('image', plot)
  
    # vmin = -100
    # vmax = 100
    # normalized_values = (fire_sectors - vmin) / (vmax - vmin)
    # normalized_values = np.clip(normalized_values, 0, 1)
    # normalized_values = cv2.normalize(fire_sectors, None, 0.0, 1.0, cv2.NORM_MINMAX)

    # heatmap = np.uint8(normalized_values * 255)
    # heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_AUTUMN)
    # heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_SUMMER)
    # window_size = (500, 500)
    # cv2.namedWindow('Heatmap', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Heatmap', window_size)
    # cv2.imshow('Heatmap', heatmap)

    cv2.waitKey(1000)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()