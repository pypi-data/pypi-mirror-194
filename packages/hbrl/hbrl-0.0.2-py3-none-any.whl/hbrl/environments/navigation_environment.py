import abc
import importlib
import random
from typing import Union
from scipy.spatial import distance
from skimage.draw import line_aa
import numpy as np
from gym.spaces import Box, Discrete
from environment import Environment
from hbrl.environments import MapsIndex
from enum import Enum

from hbrl.environments.goal_reaching_environment import GoalReachingEnv


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    START = 2
    TERMINAL = 3


class Colors(Enum):
    EMPTY = [250, 250, 250]
    WALL = [50, 54, 51]
    START = [213, 219, 214]
    TERMINAL = [73, 179, 101]
    TILE_BORDER = [50, 54, 51]
    AGENT = [0, 0, 255]
    GOAL = [255, 0, 0]


class NavigationEnv(Environment, abc.ABC):

    """
    An environment where the agent navigate inside a maze.
    It will load a map and is able to render image that show a maze representation.
    """

    name = "Default navigation environment"

    def __init__(self, map_tag: MapsIndex, state_space: Union[Box, Discrete], action_space: Union[Box, Discrete],
                 reset_anywhere=False):

        self.maze_map = np.array(importlib.import_module("hbrl.environments.maps." + map_tag.value).maze_array)
        self.height, self.width = self.maze_map.shape
        self.agent_state = None
        self.reset_anywhere = reset_anywhere

        high = np.array([self.width, self.height]) / 2
        low = - high

        self.state_space = Box(low=np.concatenate((low, state_space.low)),
                               high=np.concatenate((high, state_space.high)))
        self.action_space = action_space

        super().__init__(state_space, action_space)

    def get_state_from_coordinates(self, x, y, uniformly_sampled=True):
        """
        Return a numpy array (state) that belongs to X and Y coordinates in the grid.
        If uniformly_sampled == True, the result state is a state uniformly sampled in the area
        covered by tile at coordinate x, y.
        """
        assert self.is_valid_coordinates(x, y)
        x_value = x + .5 - self.width / 2
        y_value = - (y + .5 - self.height / 2)
        if uniformly_sampled:
            noise = np.random.uniform(-0.5, 0.5, (2,))
        else:
            noise = np.zeros(2)
        return np.asarray([x_value, y_value]) + noise

    def get_coordinates(self, state):
        """
        return the coordinates of the tile where the given state is inside.
        """
        return round(state[0].item() -.5 + self.width / 2), round(- state[1].item() - .5 + self.height / 2)

    def is_valid_coordinates(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_valid_state(self, state):
        return self.state_space.contains(state.astype(self.state_space.dtype))

    def reachable(self, state):
        return self.is_valid_state(state) and self.get_tile_type(*self.get_coordinates(state)) != TileType.WALL

    def get_tile_type(self, x: int, y: int) -> TileType:
        assert self.is_valid_coordinates(x, y)
        return TileType(self.maze_map[y][x].item())

    def is_terminal_tile(self, x: int, y: int) -> bool:
        assert self.is_valid_coordinates(x, y)
        return self.get_tile_type(x, y) == TileType.TERMINAL

    @abc.abstractmethod
    def step(self, action):
        pass

    def reset(self):
        if self.reset_anywhere:
            self.agent_state = self.sample_reachable_state()
        else:
            start_tile = np.flip(random.choice(np.argwhere(self.maze_map == 2)))
            self.agent_state = self.get_state_from_coordinates(*start_tile, uniformly_sampled=False)
        return self.agent_state

    """
    Rendering functions
    """
    def get_color(self, x, y, ignore_agent=False, ignore_terminals=False):
        agent_x, agent_y = self.get_coordinates(self.agent_state)
        if (agent_x, agent_y) == (x, y) and not ignore_agent:
            return Colors.AGENT.value
        else:
            tile_type = self.get_tile_type(x, y)
            if tile_type == TileType.START:
                return Colors.START.value
            elif tile_type == TileType.WALL:
                return Colors.WALL.value
            elif tile_type == TileType.EMPTY:
                return Colors.EMPTY.value
            elif tile_type == TileType.TERMINAL:
                return Colors.EMPTY.value if ignore_terminals else Colors.TERMINAL.value
            else:
                raise AttributeError("Unknown tile type")

    def set_tile_color(self, image_array: np.ndarray, x, y, color, tile_size=10, border_size=0) -> np.ndarray:
        """
        Set a tile color with the given color in the given image as a numpy array of pixels
        :param image_array: The image where the tile should be set
        :param x: X coordinate of the tile to set
        :param y: Y coordinate of the tile to set
        :param color: new color of the tile : numpy array [Red, Green, Blue]
        :param tile_size: size of the tile in pixels
        :param border_size: size of the tile's border in pixels
        :return: The new image
        """
        tile_img = np.zeros(shape=(tile_size, tile_size, 3), dtype=np.uint8)

        if border_size > 0:
            tile_img[:, :, :] = Colors.TILE_BORDER.value
            tile_img[border_size:-border_size, border_size:-border_size, :] = color
        else:
            tile_img[:, :, :] = color

        y_min = y * tile_size
        y_max = (y + 1) * tile_size
        x_min = x * tile_size
        x_max = (x + 1) * tile_size
        image_array[y_min:y_max, x_min:x_max, :] = tile_img
        return image_array

    def get_environment_background(self, tile_size=10, ignore_rewards=False) -> np.ndarray:
        """
        Return an image (as a numpy array of pixels) of the environment background.
        :return: environment background -> np.ndarray
        """
        # Compute the total grid size
        width_px = self.width * tile_size
        height_px = self.height * tile_size

        img = np.zeros(shape=(height_px, width_px, 3), dtype=np.uint8)

        # Render the grid
        for y in range(self.height):
            for x in range(self.width):
                cell_color = self.get_color(x, y, ignore_agent=True, ignore_terminals=ignore_rewards)
                img = self.set_tile_color(img, x, y, cell_color)
        return img

    def get_oracle(self) -> list:
        """
        Return an oracle as a list of every reachable states inside the environment.
        """
        reachable_coordinates = np.argwhere(self.maze_map != 1).tolist()
        return [self.get_state_from_coordinates(x, y) for x, y in reachable_coordinates]

    def sample_reachable_state(self):
        start_tile = np.flip(random.choice(np.argwhere(self.maze_map != 1)))
        return self.get_state_from_coordinates(*start_tile)

    def render(self, ignore_agent=False, ignore_rewards=False):
        """
        Render the whole-grid human view
        """
        if self.agent_state is None:
            self.reset()
        img = self.get_environment_background(ignore_rewards=ignore_rewards)
        if not ignore_agent:
            self.place_point(img, self.agent_state, Colors.AGENT.value)
        return img

    def place_point(self, image: np.ndarray, state, color: Union[np.ndarray, list], width=5):
        """
        Modify the input image
        param image: Initial image that will be modified.
        param x: x coordinate in the state space of the point to place.
        param y: y coordinate in the state space of the point to place.
        param color: Color to give to the pixels that compose the point.
        param width: Width of the circle (in pixels).
        """
        if isinstance(color, list):
            color = np.array(color)

        center_x, center_y = self.get_coordinates(state)
        center_x = (center_x + 0.5) / self.width
        center_y = (center_y + 0.5) / self.height
        center_y, center_x = (image.shape[:2] * np.array([center_y, center_x])).astype(int)

        # Imagine a square of size width * width, with the coordinates computed above as a center. Iterate through
        # each pixel inside this square to
        radius = round(width / 2) + 1
        for i in range(center_x - radius, center_x + radius):
            for j in range(center_y - radius, center_y + radius):
                if distance.euclidean((i + 0.5, j + 0.5), (center_x, center_y)) < radius:
                    image[j, i] = color

        return image

    def place_edge(self, image: np.ndarray, state_1, state_2, color: Union[np.ndarray, list]):
        """
        Modify the input image
        param image: Initial image that will be modified.
        param x: x coordinate in the state space of the point to place.
        param y: y coordinate in the state space of the point to place.
        param color: Color to give to the pixels that compose the point.
        param width: Width of the circle (in pixels).
        """

        color = np.array(color) if isinstance(color, list) else color
        center_x_1, center_y_1 = self.get_coordinates(state_1)
        center_x_1 = (center_x_1 + 0.5) / self.width
        center_y_1 = (center_y_1 + 0.5) / self.height
        center_y_1, center_x_1 = (image.shape[:2] * np.array([center_y_1, center_x_1])).astype(int)

        center_x_2, center_y_2 = self.get_coordinates(state_2)
        center_x_2 = (center_x_2 + 0.5) / self.width
        center_y_2 = (center_y_2 + 0.5) / self.height
        center_y_2, center_x_2 = (image.shape[:2] * np.array([center_y_2, center_x_2])).astype(int)

        rr, cc, val = line_aa(center_y_1, center_x_1, center_y_2, center_x_2)
        old = image[rr, cc]
        extended_val = np.tile(val, (3, 1)).T
        image[rr, cc] = (1 - extended_val) * old + extended_val * color

        return image


class GoalReachingNavEnv(GoalReachingEnv, NavigationEnv):

    """
    This environment wrap an hbrl.environment.NavigationEnvironment instance to make it goal-conditioned.
    at each reset, a goal is sampled from reachable states in the NavigationEnvironment map, and the reward depends if
    the sampled goal has been reached or not.
    """

    name = "GoalReachingNavEnv Default"

    def __init__(self, wrapped_environment, goal_space: Union[None, Box, Discrete]=None, sparse_reward=True):
        assert isinstance(wrapped_environment, NavigationEnv)
        GoalReachingEnv.__init__(self, wrapped_environment, goal_space, sparse_reward)

    """
    Rendering functions
    """

    def render(self, ignore_agent=False, ignore_goal=False):
        """
        Render the whole-grid human view
        """
        image = self.wrapped_environment.render(ignore_agent=ignore_agent, ignore_rewards=True)
        if not ignore_goal:
            self.place_point(image, self.agent_state, Colors.GOAL.value)
        return image