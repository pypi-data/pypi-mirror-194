from torch import nn

from hsuanwu.common.typing import *
from hsuanwu.xploit.encoder.base import BaseEncoder
from hsuanwu.xploit.utils import network_init



class CnnEncoder(BaseEncoder):
    """
    Convolutional neural network (CNN)-based encoder for processing image-based observations.

    :param observation_space: Observation space of the environment.
    :param features_dim: Number of features extracted.
    """
    def __init__(self, observation_space: Space, features_dim: int = 64) -> None:
        super().__init__(observation_space, features_dim)

        obs_shape = observation_space.shape
        assert len(obs_shape) == 3
        self.trunk = nn.Sequential(nn.Conv2d(obs_shape[0], 32, 3, stride=2), nn.ReLU(), 
                                   nn.Conv2d(32, 32, 3, stride=1), nn.ReLU(), 
                                   nn.Conv2d(32, 32, 3, stride=1), nn.ReLU(), 
                                   nn.Conv2d(32, 32, 3, stride=1), nn.ReLU())

        with torch.no_grad():
            n_flatten = self.trunk(torch.as_tensor(observation_space.sample()[None]).float()).shape[1]
        
        self.linear = nn.Linear(n_flatten, features_dim)

        self.apply(network_init)
    
    def forward(self, obs: Tensor) -> Tensor:
        obs = obs / 255.0 - 0.5
        h = self.trunk(obs)
        return self.linear(h.view(h.size()[0], -1))